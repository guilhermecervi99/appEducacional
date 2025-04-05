# app/mapping.py

from transformers import pipeline
from app import config
from app.llm_integration import call_teacher_llm
import json

# Ajuste o mínimo de score que você considera relevante para uma label
MIN_SCORE_LOCAL = 0.10

# Caso queira limitar a quantidade de rótulos após filtrar por score,
# você pode definir aqui. Se não quiser limitar, pode deixar None.
TOP_N = 10

# Instancia o pipeline Zero-Shot
classifier = pipeline(
    "zero-shot-classification",
    model=config.ZERO_SHOT_MODEL
)


def zero_shot_analysis(text: str, labels: list, top_n: int = None) -> dict:
    """
    Executa a classificação Zero-Shot no texto e retorna um dicionário {rótulo: score}.

    Passos:
    1. Se text estiver vazio, retorna dict vazio.
    2. Chama o pipeline com multi_label=True (o BART-MNLI comparará cada label separadamente).
    3. Filtra as labels que tenham score >= MIN_SCORE_LOCAL.
    4. (Opcional) Se top_n estiver definido, mantém apenas as 'top_n' melhores.
    """
    if not text.strip():
        return {}

    # Executa o zero-shot
    result = classifier(
        sequences=text,
        candidate_labels=labels,
        multi_label=True,
        hypothesis_template="This text is about {}."
    )

    # "result" contém "labels" e "scores" já ordenados (scores decrescente).
    filtered_dict = {}

    # Primeiro, guardamos TODAS que passarem do threshold
    for i, lbl in enumerate(result["labels"]):
        scr = result["scores"][i]
        if scr >= MIN_SCORE_LOCAL:
            # Passou do threshold, guardamos
            filtered_dict[lbl.lower()] = float(scr)

    # Se quisermos limitar ao top_n, vamos ordenar e recortar
    if top_n is not None:
        # Ordena por score desc
        sorted_items = sorted(filtered_dict.items(), key=lambda x: x[1], reverse=True)
        # Pega top_n
        top_items = sorted_items[:top_n]
        # Converte de volta para dict
        filtered_dict = dict(top_items)

    return filtered_dict


def combine_scores(base_scores: dict, new_scores: dict, weight: float = 1.0) -> dict:
    """
    Combina dois dicionários de pontuações com a fórmula:
      score_final = (score_base + weight * score_novo) / 2

    Ou seja, se base_scores[label] = 0.5 e new_scores[label] = 1.0,
    e weight=1.0 -> score_final = (0.5 + 1.0 * 1.0) / 2 = 0.75
    """
    combined = {}
    all_keys = set(base_scores.keys()).union(new_scores.keys())
    for key in all_keys:
        combined[key] = (base_scores.get(key, 0.0) + weight * new_scores.get(key, 0.0)) / 2
    return combined


def normalize_scale(value: int) -> float:
    """
    Converte uma escala de 1 a 5 para 0 a 1.
    Exemplo: 1 -> 0.0, 5 -> 1.0.
    """
    v = max(1, min(value, 5))
    return (v - 1.0) / 4.0


def aggregate_learning_tracks(
        scores: dict,
        learning_tracks: dict,
        min_score_threshold: float = 0.05
) -> dict:
    """
    Dado um dict de scores {label: valor} e um dict de trilhas {track: [lista_labels]},
    soma os valores dos labels da trilha que estejam acima de 'min_score_threshold'.
    Exemplo:
       scores = {"programação": 0.3, "artes": 0.5, "canto": 0.1}
       learning_tracks = {"Ciências Exatas": ["programação"], "Artes": ["artes", "canto"]}
       se min_score_threshold=0.2 -> "canto" (0.1) fica de fora, somando 0 para Artes;
       resultado final = {"Ciências Exatas": 0.3, "Artes": 0.5}
    """
    track_scores = {}
    for track, label_list in learning_tracks.items():
        total = 0.0
        count = 0
        for label in label_list:
            val = scores.get(label, 0.0)
            if val >= min_score_threshold:
                total += val
                count += 1
        if count > 0:
            # Normaliza pelo número de labels para evitar viés para trilhas com mais labels
            track_scores[track] = total / count
    return track_scores


def calculate_dynamic_weights(user_data):
    """
    Calcula pesos dinâmicos com base nas características do usuário.

    Args:
        user_data: Dicionário com dados do usuário (learning_goal, hours_per_week, etc.)

    Returns:
        Dicionário com pesos para cada fonte de dados (hobbies, likert, text)
    """
    weights = {
        "hobbies": 1.0,  # Peso para atividades favoritas/hobbies
        "likert": 0.9,  # Peso para escalas Likert
        "text": 1.1  # Peso para respostas textuais
    }

    # Ajusta pesos com base no objetivo de aprendizado
    learning_goal = user_data.get("learning_goal")
    if learning_goal:
        if learning_goal == "1":  # Desenvolvimento profissional/carreira
            weights["text"] = 1.3  # Valorizar mais respostas textuais (mais reflexivas)
            weights["likert"] = 1.0  # Valorizar auto-avaliações
        elif learning_goal == "2":  # Educação formal
            weights["text"] = 1.2  # Valorizar textos
            weights["likert"] = 1.1  # Valorizar auto-avaliações
        elif learning_goal == "3":  # Interesse pessoal/hobby
            weights["hobbies"] = 1.2  # Valorizar mais hobbies existentes
        elif learning_goal == "4":  # Mudança de área
            weights["text"] = 1.3  # Valorizar textos sobre aspirações
            weights["hobbies"] = 0.8  # Menor peso para hobbies atuais
        elif learning_goal == "5":  # Resolver problema específico
            weights["text"] = 1.4  # Valorizar muito a descrição do problema

    # Ajusta pesos com base na disponibilidade de tempo
    hours_per_week = user_data.get("hours_per_week", "5")
    if hours_per_week and hours_per_week.isdigit():
        hours = int(hours_per_week)
        if hours < 3:  # Pouco tempo disponível
            weights["hobbies"] = weights["hobbies"] * 1.2  # Priorizar o que já conhece
        elif hours > 10:  # Muito tempo disponível
            weights["text"] = weights["text"] * 1.1  # Pode explorar mais áreas novas

    # Ajusta com base no estilo de aprendizado
    learning_style = user_data.get("learning_style")
    if learning_style:
        if learning_style == "1":  # Lendo textos e livros
            weights["text"] = weights["text"] * 1.1
        elif learning_style == "3":  # Fazendo exercícios práticos
            weights["hobbies"] = weights["hobbies"] * 1.1  # Priorizar áreas práticas

    return weights


def analyze_user_personality(text_responses):
    """
    Analisa as respostas textuais do usuário para identificar traços de personalidade
    relevantes para o aprendizado.

    Args:
        text_responses: String combinando todas as respostas textuais do usuário

    Returns:
        Dicionário com traços de personalidade
    """
    if not text_responses or len(text_responses) < 20:
        # Texto muito curto para análise significativa
        return {}

    prompt = """
    Analise as seguintes respostas para identificar traços de personalidade relevantes para o aprendizado.

    Respostas do usuário:
    "{}"

    Classifique os seguintes traços em uma escala de 1 a 5 (onde 1 é baixo e 5 é alto):
    1. Orientação a detalhes
    2. Pensamento analítico
    3. Criatividade
    4. Preferência por trabalho em equipe
    5. Auto-motivação

    Responda apenas com um objeto JSON no formato:
    {{
        "orientacao_detalhes": 3,
        "pensamento_analitico": 4,
        "criatividade": 2,
        "trabalho_equipe": 5,
        "auto_motivacao": 3,
        "observacoes": "Uma breve observação sobre o estilo de aprendizado ideal"
    }}
    """.format(text_responses)

    try:
        result = call_teacher_llm(prompt, temperature=0.3)

        # Extrair JSON da resposta
        if "```json" in result:
            json_text = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            json_text = result.split("```")[1].split("```")[0]
        else:
            json_text = result

        import json
        personality_traits = json.loads(json_text)
        return personality_traits
    except Exception as e:
        print(f"Erro ao analisar personalidade: {e}")
        return {}

def recommend_learning_paths(track_scores, user_personality, top_n=3):
    """
    Refina as recomendações de trilhas com base na personalidade do usuário.

    Args:
        track_scores: Dicionário com pontuações por trilha
        user_personality: Dicionário com traços de personalidade
        top_n: Número de trilhas a recomendar

    Returns:
        Lista de trilhas recomendadas
    """
    # Características que podem influenciar a adequação de certas trilhas
    detail_orientation = user_personality.get("orientacao_detalhes", 3)
    analytical_thinking = user_personality.get("pensamento_analitico", 3)
    creativity = user_personality.get("criatividade", 3)
    teamwork = user_personality.get("trabalho_equipe", 3)

    # Fatores de ajuste para cada trilha com base na personalidade
    adjustments = {
        "Ciências Exatas e Aplicadas": (analytical_thinking - 3) * 0.05,
        "Artes e Expressão": (creativity - 3) * 0.05,
        "Música e Performance": (creativity - 3) * 0.04 + (teamwork - 3) * 0.01,
        "Esportes e Atividades Físicas": (teamwork - 3) * 0.04,
        "Jogos e Cultura Geek": (analytical_thinking - 3) * 0.02 + (creativity - 3) * 0.03,
        "Ciências Biológicas": (detail_orientation - 3) * 0.04 + (analytical_thinking - 3) * 0.01,
        "Ciências Humanas": (analytical_thinking - 3) * 0.03,
        "Ciências Sociais": (teamwork - 3) * 0.03 + (analytical_thinking - 3) * 0.02,
        "Direito e Carreiras Jurídicas": (detail_orientation - 3) * 0.04 + (analytical_thinking - 3) * 0.01,
        "Negócios e Empreendedorismo": (teamwork - 3) * 0.03 + (creativity - 3) * 0.02,
        "Meio Ambiente e Sustentabilidade": (detail_orientation - 3) * 0.02 + (teamwork - 3) * 0.03,
        "Comunicação e Mídias": (creativity - 3) * 0.03 + (teamwork - 3) * 0.02,
        "Literatura e Linguagens": (creativity - 3) * 0.03 + (detail_orientation - 3) * 0.02
    }

    # Aplicar ajustes
    adjusted_scores = {}
    for track, score in track_scores.items():
        adjustment = adjustments.get(track, 0)
        adjusted_scores[track] = score + adjustment

    # Ordenar e retornar as top_n trilhas
    sorted_tracks = sorted(adjusted_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_tracks[:top_n]


def complete_user_profile(user_data, final_scores, track_scores, personality_traits):
    """
    Cria um perfil completo do usuário para armazenamento e referência futura.

    Args:
        user_data: Dados básicos do usuário
        final_scores: Pontuações finais por label
        track_scores: Pontuações por trilha de aprendizado
        personality_traits: Traços de personalidade

    Returns:
        Dicionário completo com o perfil do usuário
    """
    # Identificar os interesses principais (top 10)
    top_interests = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    top_interests_dict = {k: v for k, v in top_interests}

    # Identificar as trilhas principais (top 3)
    top_tracks = sorted(track_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tracks_dict = {k: v for k, v in top_tracks}

    # Construir o perfil completo
    profile = {
        "basic_info": {
            "age": user_data.get("age", 0),
            "learning_style": user_data.get("learning_style", ""),
            "learning_goal": user_data.get("learning_goal", ""),
            "hours_per_week": user_data.get("hours_per_week", ""),
            "registration_date": user_data.get("registration_date", "")
        },
        "personality_traits": personality_traits,
        "interests": {
            "top_interests": top_interests_dict,
            "all_scores": final_scores
        },
        "recommendations": {
            "top_tracks": top_tracks_dict,
            "primary_recommendation": top_tracks[0][0] if top_tracks else "",
            "all_track_scores": track_scores
        },
        "learning_preferences": {
            "preferred_content_types": _derive_content_preferences(user_data, personality_traits),
            "optimal_session_duration": _estimate_session_duration(user_data),
            "suggested_learning_frequency": _suggest_learning_frequency(user_data)
        }
    }

    return profile


def _derive_content_preferences(user_data, personality_traits):
    """
    Deriva as preferências por tipos de conteúdo com base no estilo de aprendizado
    e traços de personalidade.
    """
    preferences = {}

    # Valores padrão
    preferences["text"] = 0.5
    preferences["video"] = 0.5
    preferences["interactive"] = 0.5
    preferences["social"] = 0.5
    preferences["project_based"] = 0.5

    # Ajustar com base no estilo de aprendizado
    style = user_data.get("learning_style", "")
    if style == "1":  # Lendo textos e livros
        preferences["text"] = 0.9
        preferences["video"] = 0.4
    elif style == "2":  # Assistindo vídeos
        preferences["text"] = 0.3
        preferences["video"] = 0.9
    elif style == "3":  # Exercícios práticos
        preferences["interactive"] = 0.9
        preferences["project_based"] = 0.7
    elif style == "4":  # Discussão
        preferences["social"] = 0.9
        preferences["interactive"] = 0.7

    # Ajustar com base em traços de personalidade
    if personality_traits:
        detail = personality_traits.get("orientacao_detalhes", 3) / 5.0
        creativity = personality_traits.get("criatividade", 3) / 5.0
        teamwork = personality_traits.get("trabalho_equipe", 3) / 5.0

        preferences["text"] = (preferences["text"] + detail) / 2
        preferences["interactive"] = (preferences["interactive"] + creativity) / 2
        preferences["social"] = (preferences["social"] + teamwork) / 2
        preferences["project_based"] = (preferences["project_based"] + creativity) / 2

    return preferences


def _estimate_session_duration(user_data):
    """
    Estima a duração ideal de sessões de estudo com base na disponibilidade
    e objetivo do usuário.
    """
    hours = user_data.get("hours_per_week", "5")
    if not hours or not hours.isdigit():
        hours = 5
    else:
        hours = int(hours)

    goal = user_data.get("learning_goal", "")

    # Valores padrão
    sessions_per_week = 3

    # Ajustar com base no objetivo
    if goal == "1":  # Desenvolvimento profissional
        sessions_per_week = 4
    elif goal == "2":  # Educação formal
        sessions_per_week = 5
    elif goal == "3":  # Hobby
        sessions_per_week = 2
    elif goal == "5":  # Problema específico
        sessions_per_week = 3

    # Calcular duração por sessão (em minutos)
    minutes_per_session = (hours * 60) / sessions_per_week

    # Arredondar para o múltiplo de 15 mais próximo
    minutes_per_session = round(minutes_per_session / 15) * 15

    # Garantir limites razoáveis
    if minutes_per_session < 30:
        minutes_per_session = 30
    elif minutes_per_session > 120:
        minutes_per_session = 120

    return minutes_per_session


def _suggest_learning_frequency(user_data):
    """
    Sugere a frequência ideal de sessões de estudo com base na disponibilidade
    e objetivo do usuário.
    """
    hours = user_data.get("hours_per_week", "5")
    if not hours or not hours.isdigit():
        hours = 5
    else:
        hours = int(hours)

    goal = user_data.get("learning_goal", "")

    # Calcular frequência semanal ideal
    if hours <= 2:
        frequency = "1-2 vezes por semana"
    elif hours <= 5:
        frequency = "3-4 vezes por semana"
    elif hours <= 10:
        frequency = "5-6 vezes por semana"
    else:
        frequency = "Diariamente"

    # Ajustar com base no objetivo
    if goal == "1" or goal == "2":  # Carreira ou educação formal
        # Aumenta frequência para distribuir melhor o tempo
        if frequency == "1-2 vezes por semana":
            frequency = "2-3 vezes por semana"
    elif goal == "3":  # Hobby
        # Pode ser mais flexível
        if frequency == "5-6 vezes por semana":
            frequency = "3-4 vezes por semana"

    return frequency