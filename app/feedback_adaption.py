# feedback_adaptation.py
# Novo arquivo para implementar sistema de feedback e adaptação contínua

import time
from app.firestore_client import get_firestore_client
from app.llm_integration import call_teacher_llm
import json


def collect_feedback(db, user_id, recommended_track, session_type="study"):
    """
    Coleta feedback do usuário para refinar o sistema de recomendação.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        recommended_track: Trilha atual recomendada
        session_type: Tipo de sessão (study, assessment, etc.)

    Returns:
        Dicionário com os dados de feedback coletados
    """
    print("\n=== Feedback sobre sua Experiência ===")
    print("Sua opinião nos ajuda a melhorar as recomendações.")

    if session_type == "study":
        questions = [
            "De 1 a 5, o quão relevante foi o conteúdo para seus interesses?",
            "De 1 a 5, o quão clara foi a explicação?",
            "De 1 a 5, qual a probabilidade de você aplicar o que aprendeu?"
        ]
    elif session_type == "assessment":
        questions = [
            "De 1 a 5, o quão justo foi o nível das perguntas?",
            "De 1 a 5, o quão útil foi o feedback recebido?",
            "De 1 a 5, o quão bem as perguntas testaram seu conhecimento?"
        ]
    else:  # feedback geral
        questions = [
            "De 1 a 5, o quão relevante foi a trilha recomendada?",
            "De 1 a 5, qual seu nível de satisfação com o sistema?",
            "De 1 a 5, quão fácil foi navegar pelo sistema?"
        ]

    ratings = {}
    for i, question in enumerate(questions):
        while True:
            rating = input(f"{question} ").strip()
            if rating.isdigit() and 1 <= int(rating) <= 5:
                ratings[f"rating_{i + 1}"] = int(rating)
                break
            print("Por favor, insira um número de 1 a 5.")

    missing_topics = input("Algum tópico de interesse não foi coberto? ").strip()
    suggestions = input("Sugestões para melhorar sua experiência? ").strip()

    # Salvar no Firestore
    feedback_data = {
        "ratings": ratings,
        "missing_topics": missing_topics,
        "suggestions": suggestions,
        "timestamp": time.time(),
        "session_type": session_type,
        "recommended_track": recommended_track
    }

    db.collection("users").document(user_id).collection("feedback").add(feedback_data)
    print("Obrigado pelo feedback!")

    return feedback_data


def analyze_user_feedback(db, user_id, recent_days=30):
    """
    Analisa o feedback recente do usuário para identificar padrões e áreas de melhoria.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        recent_days: Período para considerar feedback (em dias)

    Returns:
        Dicionário com análises e sugestões
    """
    # Calcular timestamp para recent_days atrás
    cutoff_time = time.time() - (recent_days * 24 * 60 * 60)

    # Buscar feedback recente
    feedback_ref = db.collection("users").document(user_id).collection("feedback")
    feedback_docs = feedback_ref.where("timestamp", ">=", cutoff_time).stream()

    feedback_list = []
    for doc in feedback_docs:
        feedback_data = doc.to_dict()
        feedback_data["id"] = doc.id
        feedback_list.append(feedback_data)

    if not feedback_list:
        return {
            "has_feedback": False,
            "message": "Nenhum feedback encontrado no período especificado"
        }

    # Analisar ratings
    study_ratings = []
    assessment_ratings = []
    general_ratings = []

    for feedback in feedback_list:
        session_type = feedback.get("session_type", "general")
        ratings = feedback.get("ratings", {})

        avg_rating = sum(ratings.values()) / len(ratings) if ratings else 0

        if session_type == "study":
            study_ratings.append(avg_rating)
        elif session_type == "assessment":
            assessment_ratings.append(avg_rating)
        else:
            general_ratings.append(avg_rating)

    # Calcular médias
    avg_study = sum(study_ratings) / len(study_ratings) if study_ratings else 0
    avg_assessment = sum(assessment_ratings) / len(assessment_ratings) if assessment_ratings else 0
    avg_general = sum(general_ratings) / len(general_ratings) if general_ratings else 0

    # Coletar todos os comentários de texto
    all_topics = " ".join([f.get("missing_topics", "") for f in feedback_list if f.get("missing_topics")])
    all_suggestions = " ".join([f.get("suggestions", "") for f in feedback_list if f.get("suggestions")])

    # Analisar comentários de texto usando LLM
    if all_topics or all_suggestions:
        prompt = f"""
        Analise os seguintes comentários de feedback de um usuário de um sistema educacional:

        Tópicos ausentes mencionados:
        "{all_topics}"

        Sugestões de melhoria:
        "{all_suggestions}"

        Baseado nestes comentários:
        1. Identifique os 3 principais temas ou preocupações
        2. Sugira 2-3 melhorias concretas para o sistema
        3. Identifique quaisquer áreas de interesse que pareçam subrepresentadas

        Responda em formato JSON com as seguintes chaves:
        - main_themes (lista)
        - improvement_suggestions (lista)
        - missing_interests (lista)
        """

        try:
            text_analysis_result = call_teacher_llm(prompt, temperature=0.3)

            # Extrair o JSON da resposta
            if "```json" in text_analysis_result:
                json_text = text_analysis_result.split("```json")[1].split("```")[0]
            elif "```" in text_analysis_result:
                json_text = text_analysis_result.split("```")[1].split("```")[0]
            else:
                json_text = text_analysis_result

            text_analysis = json.loads(json_text)
        except Exception as e:
            text_analysis = {
                "main_themes": ["Erro ao analisar comentários"],
                "improvement_suggestions": [],
                "missing_interests": []
            }
    else:
        text_analysis = {
            "main_themes": [],
            "improvement_suggestions": [],
            "missing_interests": []
        }

    # Consolidar análise
    analysis_result = {
        "has_feedback": True,
        "feedback_count": len(feedback_list),
        "period_days": recent_days,
        "average_ratings": {
            "study_sessions": avg_study,
            "assessments": avg_assessment,
            "general": avg_general,
            "overall": (avg_study + avg_assessment + avg_general) / 3 if (
                        study_ratings or assessment_ratings or general_ratings) else 0
        },
        "satisfaction_level": _determine_satisfaction_level(avg_study, avg_assessment, avg_general),
        "text_analysis": text_analysis
    }

    return analysis_result


def _determine_satisfaction_level(avg_study, avg_assessment, avg_general):
    """
    Determina o nível de satisfação geral com base nas avaliações médias.

    Returns:
        String descrevendo o nível de satisfação
    """
    # Calcular a média geral, considerando apenas médias não-zero
    counts = 0
    total = 0

    if avg_study > 0:
        total += avg_study
        counts += 1

    if avg_assessment > 0:
        total += avg_assessment
        counts += 1

    if avg_general > 0:
        total += avg_general
        counts += 1

    overall_avg = total / counts if counts > 0 else 0

    if overall_avg >= 4.5:
        return "Excelente"
    elif overall_avg >= 4.0:
        return "Muito Bom"
    elif overall_avg >= 3.5:
        return "Bom"
    elif overall_avg >= 3.0:
        return "Satisfatório"
    elif overall_avg >= 2.0:
        return "Precisa Melhorar"
    else:
        return "Insatisfatório"


def adapt_recommendations(db, user_id, analysis_result):
    """
    Adapta as recomendações com base na análise de feedback.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        analysis_result: Resultado da análise de feedback

    Returns:
        Dicionário com as adaptações realizadas
    """
    if not analysis_result["has_feedback"]:
        return {"adapted": False, "reason": "Sem feedback suficiente para adaptação"}

    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return {"adapted": False, "reason": "Usuário não encontrado"}

    user_data = user_doc.to_dict()
    current_track = user_data.get("recommended_track", "")
    track_scores = user_data.get("track_scores", {})
    final_scores = user_data.get("final_scores", {})

    # Se não temos trilhas ou pontuações, não podemos adaptar
    if not current_track or not track_scores:
        return {"adapted": False, "reason": "Dados insuficientes para adaptação"}

    # Verificar nível de satisfação
    satisfaction = analysis_result["satisfaction_level"]
    text_analysis = analysis_result.get("text_analysis", {})
    missing_interests = text_analysis.get("missing_interests", [])

    adaptations = []

    # 1. Se satisfação é baixa, considerar mudar a trilha recomendada
    if satisfaction in ["Precisa Melhorar", "Insatisfatório"]:
        # Encontrar a segunda melhor trilha
        sorted_tracks = sorted(track_scores.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_tracks) >= 2:
            second_best_track = sorted_tracks[1][0]
            # Se a diferença não for muito grande, oferecer a alternativa
            if sorted_tracks[0][1] - sorted_tracks[1][1] < 0.2:
                adaptations.append({
                    "type": "track_change",
                    "from": current_track,
                    "to": second_best_track,
                    "reason": f"Baixa satisfação com a trilha atual ({satisfaction})"
                })

    # 2. Se há interesses ausentes mencionados, incrementar seus pesos
    if missing_interests:
        missing_interest_labels = []
        for interest in missing_interests:
            # Tentar encontrar labels relevantes para esse interesse
            prompt = f"""
            Dado o interesse mencionado "{interest}", liste 3-5 palavras-chave ou termos específicos 
            que representem melhor esse interesse no contexto de aprendizado.
            Responda apenas com as palavras-chave separadas por vírgula, sem outras explicações.
            """

            try:
                keywords_response = call_teacher_llm(prompt, temperature=0.3)
                keywords = [kw.strip().lower() for kw in keywords_response.split(",")]
                missing_interest_labels.extend(keywords)
            except:
                # Se falhar, use o próprio interesse como label
                missing_interest_labels.append(interest.lower())

        # Incrementar pontuações para esses labels
        updated_scores = final_scores.copy()
        for label in missing_interest_labels:
            if label in updated_scores:
                updated_scores[label] = updated_scores[label] * 1.5
            else:
                # Se o label não existir, adicionar com pontuação média
                updated_scores[label] = sum(updated_scores.values()) / len(updated_scores) if updated_scores else 0.5

        adaptations.append({
            "type": "interests_updated",
            "interests": missing_interest_labels,
            "reason": "Interesses mencionados em feedback que não foram adequadamente considerados"
        })

        # Atualizar os scores no perfil do usuário
        user_ref.update({"final_scores": updated_scores})

    # 3. Ajustar preferências de formato de conteúdo com base nos ratings
    ratings = analysis_result["average_ratings"]
    learning_preferences = user_data.get("learning_preferences", {})
    content_preferences = learning_preferences.get("preferred_content_types", {})

    if ratings["study_sessions"] < 3.5 and content_preferences:
        # Se avaliações de estudo são baixas, tentar diversificar formatos
        top_preference = max(content_preferences.items(), key=lambda x: x[1])[0]

        # Reduzir a preferência dominante e aumentar as outras
        updated_preferences = content_preferences.copy()
        updated_preferences[top_preference] = updated_preferences[top_preference] * 0.8

        for pref in updated_preferences:
            if pref != top_preference:
                updated_preferences[pref] = updated_preferences[pref] * 1.2

        learning_preferences["preferred_content_types"] = updated_preferences

        adaptations.append({
            "type": "content_preferences_updated",
            "reason": "Diversificação de formatos devido a avaliações baixas para sessões de estudo"
        })

        # Atualizar preferências no perfil do usuário
        user_ref.update({"learning_preferences": learning_preferences})

    # Salvar registro de adaptação
    adaptation_record = {
        "timestamp": time.time(),
        "analysis_id": user_id + "_" + str(int(time.time())),
        "adaptations": adaptations,
        "satisfaction_level": satisfaction
    }

    db.collection("users").document(user_id).collection("adaptations").add(adaptation_record)

    return {
        "adapted": len(adaptations) > 0,
        "adaptations": adaptations
    }


def suggest_improvements(db, user_id):
    """
    Sugere melhorias personalizadas para a experiência de aprendizado do usuário.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário

    Returns:
        Lista de sugestões de melhoria
    """
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return ["Usuário não encontrado."]

    user_data = user_doc.to_dict()
    learning_style = user_data.get("learning_style", "")
    learning_goal = user_data.get("learning_goal", "")
    personality_traits = user_data.get("personality_traits", {})
    learning_preferences = user_data.get("learning_preferences", {})

    # Analisar padrões de uso
    sessions_ref = db.collection("users").document(user_id).collection("sessions")
    recent_sessions = sessions_ref.order_by("timestamp", direction="DESCENDING").limit(10).stream()

    sessions_data = []
    for session in recent_sessions:
        sessions_data.append(session.to_dict())

    # Verificar se temos dados suficientes para fazer sugestões informadas
    if not sessions_data and not personality_traits:
        return ["Dados insuficientes para sugestões personalizadas."]

    # Construir prompt para o LLM
    prompt = f"""
    Com base no perfil e hábitos do usuário abaixo, sugira 3-5 melhorias específicas para 
    otimizar sua experiência de aprendizado. As sugestões devem ser concretas, acionáveis 
    e personalizadas.

    Perfil do usuário:
    - Estilo de aprendizado preferido: {learning_style}
    - Objetivo de aprendizado: {learning_goal}
    - Traços de personalidade: {personality_traits}
    - Preferências de aprendizado: {learning_preferences}

    Padrões de uso (últimas sessões):
    {sessions_data}

    Responda no formato de uma lista de sugestões específicas, cada uma com:
    1. Título da sugestão
    2. Descrição detalhada de como implementar
    3. Benefício esperado

    Responda em formato JSON.
    """

    try:
        suggestions_response = call_teacher_llm(prompt, temperature=0.7)

        # Tentar extrair o JSON
        if "```json" in suggestions_response:
            json_text = suggestions_response.split("```json")[1].split("```")[0]
        elif "```" in suggestions_response:
            json_text = suggestions_response.split("```")[1].split("```")[0]
        else:
            json_text = suggestions_response

        suggestions = json.loads(json_text)

        return suggestions
    except Exception as e:
        return [{
            "title": "Experimente diferentes formatos de conteúdo",
            "description": "Alterne entre vídeos, textos e exercícios práticos para descobrir o que funciona melhor para você.",
            "benefit": "Identificar seu estilo de aprendizado ideal pode aumentar significativamente sua retenção e engajamento."
        }]