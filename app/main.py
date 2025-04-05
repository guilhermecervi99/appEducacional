# Alterações para main.py para suportar a nova estrutura hierárquica

import os
from app import config
from app.firestore_client import get_firestore_client
from app import mapping
from app.progress_management import continue_progress_flow, dynamic_progress_flow
from app.llm_integration import call_teacher_llm, TEACHING_STYLES
import time

# Importar a nova função de setup das trilhas
from app.paths import setup_learning_paths as setup_all_areas_and_subareas

# Exemplos de descrições curtas das áreas
TRACK_DESCRIPTIONS = {
    "Ciências Exatas e Aplicadas": "Foco em Matemática, Física, Química, Computação e Engenharia.",
    "Artes e Expressão": "Explora artes visuais, design, teatro, fotografia e expressão criativa.",
    "Música e Performance": "Toca instrumentos, canta, compõe e estuda teoria musical e palcos.",
    "Esportes e Atividades Físicas": "Modalidades esportivas, fitness, saúde e bem-estar.",
    "Jogos e Cultura Geek": "Jogos, desenvolvimento, cultura pop, animes, E-sports e muito mais.",
    "Ciências Biológicas": "Biologia, ecologia, genética, microbiologia e saúde.",
    "Ciências Humanas": "Filosofia, história, antropologia, psicologia, aspectos culturais.",
    "Ciências Sociais": "Sociologia, política, economia, relações internacionais e sociedade.",
    "Direito e Carreiras Jurídicas": "Investigação, leitura, advocacia, debates, legislação.",
    "Negócios e Empreendedorismo": "Administração, marketing, finanças, empreendedorismo e inovação.",
    "Meio Ambiente e Sustentabilidade": "Ecologia, energias renováveis, conservação e práticas sustentáveis.",
    "Comunicação e Mídias": "Jornalismo, marketing digital, redes sociais, publicidade e conteúdo.",
    "Literatura e Linguagens": "Leitura, escrita criativa, linguística, tradução e análise literária.",
    "Tecnologia e Sociedade": "Ética tecnológica, impacto social da tecnologia, inclusão digital.",
    "Inovação e Criatividade": "Design thinking, resolução criativa de problemas, técnicas de ideação.",
    "Bem-estar e Desenvolvimento Pessoal": "Inteligência emocional, produtividade, comunicação não-violenta."
}


def main():
    db = get_firestore_client()

    print("========== Sistema Inteligente de Direcionamento Educacional ==========")
    print("Descubra suas áreas de interesse e comece sua jornada de aprendizado personalizada.\n")

    # Configuração inicial - coleta informações básicas
    print("=== Configuração Inicial ===")
    user_id = input("Informe seu ID de usuário (ou novo ID para cadastro): ").strip()

    user_doc = db.collection("users").document(user_id).get()
    user_data = {}

    if user_doc.exists:
        user_data = user_doc.to_dict()
        print(f"Bem-vindo(a) de volta, usuário {user_id}!")

        # Verificar se já temos uma trilha recomendada
        if "recommended_track" in user_data:
            return show_main_menu(db, user_id, user_data)
    else:
        print("Novo usuário! Vamos configurar seu perfil.")

    # Coletar informações básicas para personalização
    age_str = input("Qual a sua idade? ").strip()
    age = 14  # Valor padrão
    if age_str.isdigit():
        age = int(age_str)

    user_data["age"] = age

    # Preferência de estilo de aprendizado
    print("\n=== Estilos de Ensino ===")
    print("Escolha o estilo de ensino que mais combina com você:")

    for i, (style, desc) in enumerate(TEACHING_STYLES.items(), 1):
        print(f"{i}. {style.capitalize()} - {desc}")

    style_choice = input("\nSua escolha (número): ").strip()
    learning_style = "didático"  # Estilo padrão

    if style_choice.isdigit():
        idx = int(style_choice) - 1
        if 0 <= idx < len(TEACHING_STYLES):
            learning_style = list(TEACHING_STYLES.keys())[idx]

    user_data["learning_style"] = learning_style

    # Salvar essas informações básicas
    db.collection("users").document(user_id).set(user_data, merge=True)

    # Se não temos uma trilha, seguimos para o mapeamento
    if "recommended_track" not in user_data:
        proceed = input("\nDeseja fazer o mapeamento de interesses agora? (s/n): ").strip().lower()
        if proceed == 's':
            user_data = run_mapping_process(db, user_id, user_data)
        else:
            print("Você pode fazer o mapeamento a qualquer momento pelo menu principal.")

    # Exibir menu principal
    show_main_menu(db, user_id, user_data)


def run_mapping_process(db, user_id, user_data):
    """
    Executa o processo de mapeamento de interesses do usuário.
    Atualizado para a nova estrutura hierárquica.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        user_data: Dados do usuário já carregados

    Returns:
        Dados atualizados do usuário após o mapeamento
    """
    print("\n========== Mapeamento de Interesses ==========")
    print("Responda às perguntas para identificarmos suas áreas de interesse.\n")

    # 1) Perguntar qual grande área atrai mais (opcional), com pequena descrição:
    track_keys = list(config.LEARNING_TRACKS.keys())
    print("1) Selecione UMA grande área que mais te atrai (ou Enter para pular):\n")
    for i, tk in enumerate(track_keys, start=1):
        desc = TRACK_DESCRIPTIONS.get(tk, "")
        print(f"{i}. {tk} - {desc}")
    chosen_str = input("\nNúmero da área (ou Enter): ").strip()
    chosen_area = ""
    if chosen_str.isdigit():
        idx = int(chosen_str)
        if 1 <= idx <= len(track_keys):
            chosen_area = track_keys[idx - 1]
            print(f"Área escolhida: {chosen_area}\n")
        else:
            print("Entrada inválida. Prosseguindo sem filtrar.\n")
    else:
        print("Nenhuma área selecionada. Prosseguindo sem filtrar.\n")

    # 2) Pergunta de múltipla escolha (hobbies) - OPCIONAL
    print("2) Atividades favoritas (múltipla escolha), ou Enter para pular.\n")
    possible_hobbies = [
        "Praticar esportes",
        "Jogar videogames",
        "Ler (livros, quadrinhos, fanfics)",
        "Desenhar ou pintar",
        "Cozinhar ou confeitar",
        "Tocar instrumento musical",
        "Fazer artesanato (crochê, marcenaria, etc.)",
        "Cuidar de plantas/animais",
        "Ver vídeos sobre ciência/tecnologia"
    ]
    for i, hob in enumerate(possible_hobbies, start=1):
        print(f"{i}. {hob}")
    sel_str = input("\nDigite os números (ex: 1 3 5) ou Enter p/ pular: ").strip()

    mc_scores = {}
    if sel_str:  # só processa se o usuário digitou algo
        indices = [x for x in sel_str.replace(",", " ").split() if x.isdigit()]
        for idx_str in indices:
            i2 = int(idx_str)
            if 1 <= i2 <= len(possible_hobbies):
                key_hob = possible_hobbies[i2 - 1].lower()
                mc_scores[key_hob] = mc_scores.get(key_hob, 0) + 1.0

        # Normaliza
        if mc_scores:
            max_val = max(mc_scores.values())
            for k in mc_scores:
                mc_scores[k] /= max_val

    # 3) Perguntas de escala (Likert) [1-5], também opcionais
    print("\n3) Avalie de 1 a 5 (ou Enter para pular cada pergunta).")

    def ask_likert(question: str):
        val_str = input(question + " [1-5, ou Enter p/ pular]: ").strip()
        if val_str.isdigit():
            val_int = int(val_str)
            if 1 <= val_int <= 5:
                return mapping.normalize_scale(val_int)
        # Se entrou aqui, ou é vazio ou inválido
        return None

    likert_scores = {}
    val_prog = ask_likert("O quanto você gosta de programar no computador?")
    if val_prog is not None:
        likert_scores["programação"] = val_prog

    val_com = ask_likert("O quanto você gosta de falar em público?")
    if val_com is not None:
        likert_scores["comunicação"] = val_com

    val_art = ask_likert("O quanto você gosta de atividades artísticas?")
    if val_art is not None:
        likert_scores["artes"] = val_art

    val_esp = ask_likert("O quanto você gosta de esportes em geral?")
    if val_esp is not None:
        likert_scores["esportes"] = val_esp

    val_mus = ask_likert("O quanto você gosta de música (tocar, cantar, produzir)?")
    if val_mus is not None:
        likert_scores["música"] = val_mus

    # 4) Perguntas abertas: também opcionais
    print("\n4) Fale um pouco sobre seus interesses ou sonhos de carreira (ou Enter p/ pular):")
    text1 = input("> ").strip()
    print("\n   O que te motiva a aprender algo novo? (ou Enter p/ pular)")
    text2 = input("> ").strip()

    # 5) Estilo de aprendizado
    print("\n5) Como você prefere aprender novos conteúdos?")
    learning_styles = [
        "Lendo textos e livros",
        "Assistindo vídeos ou aulas",
        "Fazendo exercícios práticos",
        "Discutindo com outras pessoas",
        "Ensinando o conteúdo para alguém"
    ]
    for i, style in enumerate(learning_styles, start=1):
        print(f"{i}. {style}")
    preferred_style = input("Escolha (número): ").strip()
    user_data["learning_style"] = preferred_style

    # 6) Objetivos de aprendizado
    print("\n6) Qual seu principal objetivo com este aprendizado?")
    learning_goals = [
        "Desenvolvimento profissional/carreira",
        "Educação formal (escola/faculdade)",
        "Interesse pessoal/hobby",
        "Preparação para mudança de área",
        "Resolver um problema específico"
    ]
    for i, goal in enumerate(learning_goals, start=1):
        print(f"{i}. {goal}")
    learning_goal = input("Escolha (número): ").strip()
    user_data["learning_goal"] = learning_goal

    # 7) Tempo disponível
    hours_per_week = input("\n7) Quantas horas por semana você pode dedicar ao estudo? ").strip()
    user_data["hours_per_week"] = hours_per_week

    # 8) Experiência prévia
    print("\n8) Qual seu nível de experiência nas áreas que deseja estudar?")
    experience_levels = [
        "Iniciante completo (primeiro contato)",
        "Algum conhecimento básico",
        "Conhecimento intermediário",
        "Conhecimento avançado em algumas áreas",
        "Quero aprimorar conhecimentos específicos"
    ]
    for i, level in enumerate(experience_levels, start=1):
        print(f"{i}. {level}")
    experience_level = input("Escolha (número): ").strip()
    user_data["experience_level"] = experience_level

    # 9) Ritmo de aprendizado
    print("\n9) Qual ritmo de aprendizado você prefere?")
    learning_paces = [
        "Intensivo e rápido",
        "Moderado e constante",
        "Lento e aprofundado",
        "Varia conforme o assunto",
        "Não tenho preferência"
    ]
    for i, pace in enumerate(learning_paces, start=1):
        print(f"{i}. {pace}")
    learning_pace = input("Escolha (número): ").strip()
    user_data["learning_pace"] = learning_pace

    # 10) Formato de conteúdo
    print("\n10) Que tipo de conteúdo você prefere?")
    content_types = [
        "Textual (artigos, livros)",
        "Visual (vídeos, diagramas)",
        "Interativo (exercícios, jogos)",
        "Auditivo (podcasts, áudio)",
        "Prático (projetos, experimentos)"
    ]
    for i, type in enumerate(content_types, start=1):
        print(f"{i}. {type}")
    content_preference = input("Escolha (número): ").strip()
    user_data["content_preference"] = content_preference

    # 11) Desafios de aprendizado
    print("\n11) Quais são seus maiores desafios ao aprender algo novo?")
    challenges = [
        "Manter a motivação",
        "Organizar o tempo",
        "Entender conceitos complexos",
        "Aplicar na prática o que aprendi",
        "Medir meu progresso"
    ]
    for i, challenge in enumerate(challenges, start=1):
        print(f"{i}. {challenge}")
    learning_challenge = input("Escolha (número): ").strip()
    user_data["learning_challenge"] = learning_challenge

    # 12) Pergunta aberta adicional
    print(
        "\n12) Descreva uma situação em que você aprendeu algo com facilidade e prazer. O que tornou essa experiência positiva?")
    learning_experience = input("> ").strip()
    user_data["learning_experience"] = learning_experience

    candidate_labels = config.CANDIDATE_LABELS

    # 5) Zero-shot para cada texto (caso não estejam vazios)
    text1_scores = {}
    text2_scores = {}
    if text1:
        text1_scores = mapping.zero_shot_analysis(text1, candidate_labels)
    if text2:
        text2_scores = mapping.zero_shot_analysis(text2, candidate_labels)

    # Combinar respostas textuais para análise de personalidade
    text_responses = f"{text1} {text2} {learning_experience}"
    personality_traits = mapping.analyze_user_personality(text_responses)

    # Calcular pesos dinâmicos baseados nas novas informações
    dynamic_weights = mapping.calculate_dynamic_weights(user_data)

    # 6) Combinar as pontuações (texto1, texto2, MC, Likert)
    text_combined = mapping.combine_scores({}, text1_scores, weight=1.0)
    text_combined = mapping.combine_scores(text_combined, text2_scores, weight=1.0)

    final_scores = {}
    final_scores = mapping.combine_scores(final_scores, mc_scores, weight=dynamic_weights["hobbies"])
    final_scores = mapping.combine_scores(final_scores, likert_scores, weight=dynamic_weights["likert"])
    final_scores = mapping.combine_scores(final_scores, text_combined, weight=dynamic_weights["text"])

    # Agregar em trilhas (mantendo o código original)
    track_scores = mapping.aggregate_learning_tracks(final_scores, config.LEARNING_TRACKS)

    # Refinar recomendações com base nos traços de personalidade
    refined_recommendations = mapping.recommend_learning_paths(track_scores, personality_traits)
    sorted_tracks = refined_recommendations
    if not sorted_tracks:
        print("Nenhuma trilha encontrada. Fallback para 'Artes e Expressão'.")
        recommended_track = "Artes e Expressão"
    else:
        # Exibir top 3 trilhas (pode mudar para 5 se quiser)
        print("\n=== Trilhas Sugeridas (Top 3) ===")
        top_n = min(3, len(sorted_tracks))  # exibir 3 ou total
        for i, (trk, val) in enumerate(sorted_tracks[:top_n], start=1):
            print(f"{i}. {trk} => {val:.2f}")
        recommended_track = sorted_tracks[0][0]

    print(f"\nTrilha principal recomendada: {recommended_track}")

    # Confirmar escolha ou permitir alteração manual
    print("\nDeseja:")
    print("1. Aceitar a trilha recomendada")
    print("2. Escolher outra das trilhas sugeridas")
    print("3. Escolher qualquer trilha manualmente")
    choice = input("Sua escolha: ").strip()

    if choice == "2":
        # Escolher das sugeridas
        if len(sorted_tracks) > 1:
            choice_num = input(f"Escolha o número da trilha (1-{min(3, len(sorted_tracks))}): ").strip()
            if choice_num.isdigit():
                idx = int(choice_num) - 1
                if 0 <= idx < len(sorted_tracks):
                    recommended_track = sorted_tracks[idx][0]
        else:
            print("Não há outras trilhas sugeridas. Mantendo a recomendação original.")
    elif choice == "3":
        # Escolher qualquer uma
        all_tracks = list(config.LEARNING_TRACKS.keys())
        print("\nTodas as trilhas disponíveis:")
        for i, track in enumerate(all_tracks, start=1):
            print(f"{i}. {track}")

        choice_num = input(f"Escolha o número da trilha (1-{len(all_tracks)}): ").strip()
        if choice_num.isdigit():
            idx = int(choice_num) - 1
            if 0 <= idx < len(all_tracks):
                recommended_track = all_tracks[idx]
    # Criar perfil completo do usuário
    user_profile = mapping.complete_user_profile(user_data, final_scores, track_scores, personality_traits)

    # Adicionar mensagem personalizada baseada no perfil
    if personality_traits:
        print("\n=== Insights Sobre Seu Perfil de Aprendizado ===")

        # Determinar estilos de conteúdo recomendados
        learning_preferences = user_profile["learning_preferences"]
        content_preferences = learning_preferences["preferred_content_types"]

        # Encontrar as duas preferências mais altas
        sorted_prefs = sorted(content_preferences.items(), key=lambda x: x[1], reverse=True)
        top_prefs = sorted_prefs[:2]

        top_pref_1 = "textos" if top_prefs[0][0] == "text" else \
            "vídeos" if top_prefs[0][0] == "video" else \
                "exercícios interativos" if top_prefs[0][0] == "interactive" else \
                    "aprendizado social" if top_prefs[0][0] == "social" else \
                        "projetos práticos"

        top_pref_2 = "textos" if top_prefs[1][0] == "text" else \
            "vídeos" if top_prefs[1][0] == "video" else \
                "exercícios interativos" if top_prefs[1][0] == "interactive" else \
                    "aprendizado social" if top_prefs[1][0] == "social" else \
                        "projetos práticos"

        # Tempo de sessão e frequência
        session_duration = learning_preferences["optimal_session_duration"]
        frequency = learning_preferences["suggested_learning_frequency"]

        print(f"• Baseado no seu perfil, você aprende melhor com {top_pref_1} e {top_pref_2}.")
        print(f"• Duração ideal de cada sessão de estudo: {session_duration} minutos.")
        print(f"• Frequência recomendada: {frequency}.")

        # Adicionar pontos fortes baseados nos traços de personalidade
        strengths = []
        if personality_traits.get("orientacao_detalhes", 0) >= 4:
            strengths.append("atenção aos detalhes")
        if personality_traits.get("pensamento_analitico", 0) >= 4:
            strengths.append("pensamento analítico")
        if personality_traits.get("criatividade", 0) >= 4:
            strengths.append("criatividade")
        if personality_traits.get("auto_motivacao", 0) >= 4:
            strengths.append("auto-motivação")

        if strengths:
            print(f"• Seus pontos fortes: {', '.join(strengths)}.")

        # Adicionar observações gerais
        if "observacoes" in personality_traits:
            print(f"• {personality_traits['observacoes']}")

    # Preparando a estrutura de progresso hierárquica
    # Consultar o Firestore para obter as subáreas disponíveis na área recomendada
    area_ref = db.collection("learning_paths").document(recommended_track)
    area_doc = area_ref.get()

    if area_doc.exists:
        area_data = area_doc.to_dict()
        subareas = area_data.get("subareas", {}).keys()

        # Atualizar dados do usuário com a estrutura de progresso hierárquica
        user_data.update({
            "chosen_area_suggestion": chosen_area,
            "recommended_track": recommended_track,
            "final_scores": final_scores,
            "track_scores": track_scores,
            "personality_traits": personality_traits,
            "progress": {
                "area": recommended_track,
                "subareas_order": list(subareas),  # Todas as subáreas disponíveis na área
                "current": {
                    "subarea": next(iter(subareas), "") if subareas else "",
                    "level": "iniciante",
                    "module_index": 0,
                    "lesson_index": 0,
                    "step_index": 0
                }
            },
            "learning_preferences": user_profile["learning_preferences"]
        })
    else:
        # Fallback se a área não existir no Firestore
        user_data.update({
            "chosen_area_suggestion": chosen_area,
            "recommended_track": recommended_track,
            "final_scores": final_scores,
            "track_scores": track_scores,
            "personality_traits": personality_traits,
            "progress": {
                "area": recommended_track,
                "subareas_order": [],
                "current": {
                    "subarea": "",
                    "level": "iniciante",
                    "module_index": 0,
                    "lesson_index": 0,
                    "step_index": 0
                }
            },
            "learning_preferences": user_profile["learning_preferences"]
        })

    # Salvar no Firestore
    db.collection("users").document(user_id).set(user_data, merge=True)
    print("\nSeus dados e preferências foram salvos com sucesso!")

    return user_data


def show_main_menu(db, user_id, user_data):
    """
    Exibe o menu principal do sistema após o login/mapeamento.
    Atualizado para a nova estrutura hierárquica.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        user_data: Dados do usuário
    """
    recommended_track = user_data.get("recommended_track", "")

    while True:
        print("\n" + "=" * 60)
        print(f"MENU PRINCIPAL - Sistema de Direcionamento Educacional")
        print("=" * 60)

        if recommended_track:
            print(f"Área atual: {recommended_track}")

            # Mostrar subárea atual, se existir
            current_progress = user_data.get("progress", {}).get("current", {})
            current_subarea = current_progress.get("subarea", "")
            if current_subarea:
                print(f"Subárea atual: {current_subarea}")
                print(f"Nível: {current_progress.get('level', 'iniciante')}")
        else:
            print("Você ainda não tem uma área recomendada.")

        print("\nOpções:")
        print("1. Continuar aprendizado (modo linear/video-game)")
        print("2. Explorar áreas de interesse (modo dinâmico)")
        print("3. Fazer novo mapeamento de interesses")
        print("4. Alterar preferências de aprendizado")
        print("5. Ver estatísticas e progresso")
        print("6. Pedir sugestões ao professor virtual")
        print("7. Gerenciar projetos")
        print("8. Ver áreas e cursos disponíveis")
        print("9. Configurar trilhas de aprendizado (admin)")  # Nova opção para configurar trilhas
        print("0. Sair")

        choice = input("\nEscolha uma opção: ").strip()

        if choice == "1":
            if recommended_track:
                continue_progress_flow(db, user_id)
            else:
                print("Você precisa fazer o mapeamento de interesses primeiro.")
                if input("Deseja fazer o mapeamento agora? (s/n): ").lower() == 's':
                    user_data = run_mapping_process(db, user_id, user_data)
                    recommended_track = user_data.get("recommended_track", "")

        elif choice == "2":
            if recommended_track:
                dynamic_progress_flow(db, user_id)
            else:
                print("Você precisa fazer o mapeamento de interesses primeiro.")
                if input("Deseja fazer o mapeamento agora? (s/n): ").lower() == 's':
                    user_data = run_mapping_process(db, user_id, user_data)
                    recommended_track = user_data.get("recommended_track", "")

        elif choice == "3":
            user_data = run_mapping_process(db, user_id, user_data)
            recommended_track = user_data.get("recommended_track", "")

        elif choice == "4":
            update_preferences(db, user_id, user_data)
            # Recarregar dados atualizados
            user_doc = db.collection("users").document(user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()

        elif choice == "5":
            show_user_statistics(db, user_id, user_data)

        elif choice == "6":
            ask_virtual_teacher(user_data)

        elif choice == "7":
            manage_projects(db, user_id, user_data)

        elif choice == "8":
            browse_available_tracks(db, user_id)

        elif choice == "9":
            # Opção administrativa para configurar trilhas
            if input("Essa opção reconfigurará as trilhas de aprendizado. Continuar? (s/n): ").lower() == 's':
                setup_all_areas_and_subareas(db)
                print("\nTrilhas de aprendizado configuradas com sucesso!")

        elif choice == "0":
            print("Obrigado por usar o Sistema de Direcionamento Educacional. Até breve!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")


def show_user_statistics(db, user_id, user_data):
    """
    Exibe estatísticas e progresso do usuário.
    Atualizado para a nova estrutura hierárquica.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        user_data: Dados do usuário
    """
    print("\n=== Estatísticas e Progresso ===")

    recommended_track = user_data.get("recommended_track", "Não definido")
    progress = user_data.get("progress", {})
    current = progress.get("current", {})

    print(f"Área principal: {recommended_track}")

    # Exibir progresso atual detalhado
    if current:
        print("\nProgresso atual:")
        print(f"Subárea: {current.get('subarea', 'Não iniciada')}")
        print(f"Nível: {current.get('level', 'iniciante')}")
        print(f"Módulo: {current.get('module_index', 0) + 1}")
        print(f"Lição: {current.get('lesson_index', 0) + 1}")
        print(f"Passo: {current.get('step_index', 0) + 1}")

    # Exibir áreas de interesse
    final_scores = user_data.get("final_scores", {})
    if final_scores:
        print("\nPrincipais áreas de interesse:")
        sorted_interests = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (lbl, sc) in enumerate(sorted_interests[:5], start=1):
            print(f"{i}. {lbl} => {sc:.2f}")

    # Exibir projetos concluídos
    completed_projects = user_data.get("completed_projects", [])
    if completed_projects:
        print("\nProjetos concluídos:")
        for project in completed_projects[-5:]:  # Mostrar os 5 mais recentes
            print(f"• {project['title']} ({project['type']}) - Concluído em {project['completion_date']}")

    # Exibir certificações obtidas
    certifications = user_data.get("certifications", [])
    if certifications:
        print("\nCertificações obtidas:")
        for cert in certifications:
            print(f"• {cert['title']} - Obtida em {cert['date']}")

    # Exibir avaliações concluídas
    passed_assessments = user_data.get("passed_assessments", [])
    if passed_assessments:
        print("\nAvaliações concluídas:")
        for assessment in passed_assessments[-3:]:  # Mostrar as 3 mais recentes
            print(f"• {assessment['module']} - Nota: {assessment['score']}% - Data: {assessment['date']}")

    # Exibir subáreas concluídas
    completed_subareas = user_data.get("completed_subareas", [])
    if completed_subareas:
        print("\nSubáreas concluídas:")
        for subarea in completed_subareas:
            print(f"• {subarea}")

    input("\nPressione Enter para continuar...")


def update_preferences(db, user_id, user_data):
    """
    Permite ao usuário atualizar suas preferências de aprendizado.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        user_data: Dados do usuário
    """
    print("\n=== Atualizar Preferências de Aprendizado ===")

    # Exibir preferências atuais
    age = user_data.get("age", "Não definido")
    learning_style = user_data.get("learning_style", "didático")

    print(f"Preferências atuais:")
    print(f"1. Idade: {age}")
    print(f"2. Estilo de aprendizado: {learning_style}")

    # Nova opção para alterar a área atual
    print(f"3. Área atual: {user_data.get('recommended_track', 'Não definida')}")

    # Nova opção para alterar a subárea atual
    current_progress = user_data.get("progress", {}).get("current", {})
    current_subarea = current_progress.get("subarea", "Não definida")
    print(f"4. Subárea atual: {current_subarea}")

    print("5. Voltar")

    choice = input("\nO que deseja atualizar? ").strip()

    if choice == "1":
        age_str = input("Nova idade: ").strip()
        if age_str.isdigit():
            age = int(age_str)
            db.collection("users").document(user_id).update({"age": age})
            print("Idade atualizada com sucesso!")
        else:
            print("Entrada inválida.")

    elif choice == "2":
        print("\nEstilos de ensino disponíveis:")
        for i, (style, desc) in enumerate(TEACHING_STYLES.items(), 1):
            print(f"{i}. {style.capitalize()} - {desc}")

        style_choice = input("\nEscolha um estilo (número): ").strip()
        if style_choice.isdigit():
            idx = int(style_choice) - 1
            if 0 <= idx < len(TEACHING_STYLES):
                learning_style = list(TEACHING_STYLES.keys())[idx]
                db.collection("users").document(user_id).update({"learning_style": learning_style})
                print(f"\nEstilo de aprendizado alterado para '{learning_style}'.")
            else:
                print("Opção inválida.")
        else:
            print("Entrada inválida.")

    elif choice == "3":
        # Alterar área atual
        areas = list(config.LEARNING_TRACKS.keys())
        print("\nÁreas disponíveis:")
        for i, area in enumerate(areas, 1):
            print(f"{i}. {area}")

        area_choice = input("\nEscolha uma área (número): ").strip()
        if area_choice.isdigit():
            idx = int(area_choice) - 1
            if 0 <= idx < len(areas):
                new_area = areas[idx]

                # Verificar se a área existe no Firestore
                area_ref = db.collection("learning_paths").document(new_area)
                area_doc = area_ref.get()

                if area_doc.exists:
                    area_data = area_doc.to_dict()
                    subareas = area_data.get("subareas", {})

                    if subareas:
                        default_subarea = next(iter(subareas.keys()), "")

                        # Atualizar progresso do usuário
                        user_data["recommended_track"] = new_area
                        user_data["progress"] = {
                            "area": new_area,
                            "subareas_order": list(subareas.keys()),
                            "current": {
                                "subarea": default_subarea,
                                "level": "iniciante",
                                "module_index": 0,
                                "lesson_index": 0,
                                "step_index": 0
                            }
                        }

                        db.collection("users").document(user_id).set(user_data, merge=True)
                        print(f"\nÁrea alterada para '{new_area}' com sucesso!")
                    else:
                        print("\nEsta área não possui subáreas definidas ainda.")
                else:
                    print("\nEsta área ainda não foi configurada no sistema.")
            else:
                print("Opção inválida.")
        else:
            print("Entrada inválida.")

    elif choice == "4":
        # Alterar subárea atual
        area = user_data.get("recommended_track", "")
        if not area:
            print("Você precisa ter uma área definida primeiro.")
            return

        area_ref = db.collection("learning_paths").document(area)
        area_doc = area_ref.get()

        if area_doc.exists:
            area_data = area_doc.to_dict()
            subareas = area_data.get("subareas", {})

            if subareas:
                print("\nSubáreas disponíveis:")
                subareas_list = list(subareas.keys())

                for i, subarea in enumerate(subareas_list, 1):
                    print(f"{i}. {subarea}")

                subarea_choice = input("\nEscolha uma subárea (número): ").strip()
                if subarea_choice.isdigit():
                    idx = int(subarea_choice) - 1
                    if 0 <= idx < len(subareas_list):
                        new_subarea = subareas_list[idx]

                        # Atualizar progresso do usuário
                        user_data["progress"]["current"] = {
                            "subarea": new_subarea,
                            "level": "iniciante",
                            "module_index": 0,
                            "lesson_index": 0,
                            "step_index": 0
                        }

                        db.collection("users").document(user_id).set(user_data, merge=True)
                        print(f"\nSubárea alterada para '{new_subarea}' com sucesso!")
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida.")
            else:
                print("Esta área não possui subáreas definidas ainda.")
        else:
            print("Área não encontrada no sistema.")


def ask_virtual_teacher(user_data):
    """
    Permite ao usuário fazer perguntas ao professor virtual.

    Args:
        user_data: Dados do usuário para personalização
    """
    print("\n=== Professor Virtual ===")
    print("O que você gostaria de perguntar? (digite 'sair' para voltar)")

    recommended_track = user_data.get("recommended_track", "")
    current_progress = user_data.get("progress", {}).get("current", {})
    current_subarea = current_progress.get("subarea", "")

    # Determinar o contexto atual do aluno para personalizar respostas
    context = f"área de {recommended_track}"
    if current_subarea:
        context += f", subárea de {current_subarea}"

    user_age = user_data.get("age", 14)
    learning_style = user_data.get("learning_style", "didático")

    while True:
        question = input("\n> ").strip()

        if question.lower() in ['sair', 'voltar', 'exit']:
            break

        if not question:
            continue

        print("\nPensando...")
        answer = call_teacher_llm(
            f"O aluno está estudando {context} e pergunta: '{question}'. "
            f"Responda de forma adequada para um estudante de {user_age} anos, "
            f"usando linguagem clara e acessível.",
            student_age=user_age,
            subject_area=recommended_track,
            teaching_style=learning_style
        )

        print(f"\n[Professor]: {answer}")


def browse_available_tracks(db, user_id):
    """
    Permite ao usuário navegar pelas áreas e subáreas disponíveis no sistema.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
    """
    print("\n=== Áreas de Aprendizado Disponíveis ===")

    # Buscar todas as áreas
    areas_ref = db.collection("learning_paths")
    areas = list(areas_ref.stream())

    if not areas:
        print("Não há áreas configuradas no momento.")
        input("\nPressione Enter para voltar...")
        return

    while True:
        print("\nEscolha uma área para ver detalhes:")

        for i, area_doc in enumerate(areas, 1):
            area_data = area_doc.to_dict()
            area_name = area_data.get("name", "Sem nome")
            area_desc = area_data.get("description", "")[:80]

            # Mostrar informações básicas da área
            print(f"{i}. {area_name}")
            if area_desc:
                print(f"   {area_desc}")

        print("0. Voltar")

        choice = input("\nSua escolha: ").strip()

        if choice == "0":
            break

        if choice.isdigit() and 1 <= int(choice) <= len(areas):
            area_idx = int(choice) - 1
            area_data = areas[area_idx].to_dict()
            view_area_details(db, user_id, area_data)
        else:
            print("Opção inválida.")


def view_area_details(db, user_id, area_data):
    """
    Exibe detalhes de uma área específica.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        area_data: Dados da área selecionada
    """
    area_name = area_data.get("name", "Sem nome")
    area_desc = area_data.get("description", "")

    print("\n" + "=" * 60)
    print(f"DETALHES DA ÁREA: {area_name}")
    print("=" * 60)

    if area_desc:
        print(f"\nDescrição: {area_desc}")

    # Mostrar subáreas
    subareas = area_data.get("subareas", {})
    if subareas:
        print("\nSubáreas disponíveis:")
        for i, (subarea_name, subarea_data) in enumerate(subareas.items(), 1):
            subarea_desc = subarea_data.get("description", "")[:80]
            print(f"{i}. {subarea_name}")
            if subarea_desc:
                print(f"   {subarea_desc}")
    else:
        print("\nEsta área ainda não possui subáreas configuradas.")

    # Opções para o usuário
    print("\nOpções:")
    print("1. Ver subáreas em detalhes")
    print("2. Definir como área atual")
    print("0. Voltar")

    choice = input("\nSua escolha: ").strip()

    if choice == "1" and subareas:
        while True:
            print("\nEscolha uma subárea para ver detalhes:")
            for i, (subarea_name, subarea_data) in enumerate(subareas.items(), 1):
                print(f"{i}. {subarea_name}")
            print("0. Voltar")

            sub_choice = input("\nSua escolha: ").strip()

            if sub_choice == "0":
                break

            if sub_choice.isdigit() and 1 <= int(sub_choice) <= len(subareas):
                sub_idx = int(sub_choice) - 1
                subarea_name = list(subareas.keys())[sub_idx]
                subarea_data = subareas[subarea_name]
                view_subarea_details(subarea_name, subarea_data)
            else:
                print("Opção inválida.")

    elif choice == "2":
        # Definir como área atual do usuário
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            confirm = input(f"\nDefinir '{area_name}' como sua área atual? (s/n): ").lower()

            if confirm == 's':
                user_data = user_doc.to_dict()

                # Determinar uma subárea padrão
                default_subarea = ""
                if subareas:
                    default_subarea = next(iter(subareas.keys()), "")

                # Atualizar a área e progresso do usuário
                user_data["recommended_track"] = area_name
                user_data["progress"] = {
                    "area": area_name,
                    "subareas_order": list(subareas.keys()) if subareas else [],
                    "current": {
                        "subarea": default_subarea,
                        "level": "iniciante",
                        "module_index": 0,
                        "lesson_index": 0,
                        "step_index": 0
                    }
                }

                user_ref.set(user_data, merge=True)

                print(f"\nÁrea atual definida como '{area_name}'.")
                print("Você pode iniciar seu aprendizado a partir do menu principal.")
            else:
                print("\nOperação cancelada.")
        else:
            print("\nUsuário não encontrado. Faça login primeiro.")


def view_subarea_details(subarea_name, subarea_data):
    """
    Exibe detalhes de uma subárea específica.

    Args:
        subarea_name: Nome da subárea
        subarea_data: Dados da subárea
    """
    print("\n" + "=" * 60)
    print(f"SUBÁREA: {subarea_name}")
    print("=" * 60)

    description = subarea_data.get("description", "")
    if description:
        print(f"\nDescrição: {description}")

    # Mostrar tempo estimado
    est_time = subarea_data.get("estimated_time", "")
    if est_time:
        print(f"Tempo estimado: {est_time}")

    # Mostrar faixa etária recomendada
    age_range = subarea_data.get("age_range", "")
    if age_range:
        print(f"Faixa etária recomendada: {age_range}")

    # Mostrar recursos de aprendizado
    resources = subarea_data.get("references", [])
    if resources:
        print("\nRecursos recomendados:")
        for resource in resources:
            title = resource.get("title", "")
            url = resource.get("url", "")
            print(f"• {title} - {url}")

    # Mostrar níveis disponíveis
    levels = subarea_data.get("levels", {})
    if levels:
        print("\nNíveis disponíveis:")
        for level_name, level_data in levels.items():
            level_desc = level_data.get("description", "")[:80]
            print(f"• {level_name.capitalize()}: {level_desc}")

            # Mostrar objetivos de aprendizado
            learning_outcomes = level_data.get("learning_outcomes", [])
            if learning_outcomes:
                print("  Objetivos de aprendizado:")
                for outcome in learning_outcomes[:3]:  # Mostrar apenas 3 para não ficar muito extenso
                    print(f"    - {outcome}")

            # Mostrar módulos deste nível
            modules = level_data.get("modules", [])
            if modules:
                print("  Módulos:")
                for i, module in enumerate(modules, 1):
                    module_title = module.get("module_title", "Sem título")
                    print(f"    {i}. {module_title}")
                    if i >= 3:  # Limitar a 3 módulos mostrados
                        remaining = len(modules) - 3
                        if remaining > 0:
                            print(f"    ... e mais {remaining} módulo(s)")
                        break

    # Mostrar especializações, se houver
    specializations = subarea_data.get("specializations", [])
    if specializations:
        print("\nEspecializações disponíveis:")
        for spec in specializations:
            spec_name = spec.get("name", "")
            spec_desc = spec.get("description", "")[:80]
            print(f"• {spec_name}: {spec_desc}")

    # Mostrar informações de carreira
    career = subarea_data.get("career_exploration", {})
    if career:
        print("\nExploração de carreira:")
        careers = career.get("related_careers", [])
        if careers:
            print("  Carreiras relacionadas: " + ", ".join(careers[:5]))

    input("\nPressione Enter para voltar...")


def manage_projects(db, user_id, user_data):
    """
    Permite ao usuário gerenciar seus projetos em andamento e concluídos.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        user_data: Dados do usuário
    """
    # Buscar projetos do usuário
    started_projects = user_data.get("started_projects", [])
    completed_projects = user_data.get("completed_projects", [])

    while True:
        print("\n" + "=" * 60)
        print("GERENCIAMENTO DE PROJETOS")
        print("=" * 60)

        # Mostrar projetos em andamento
        active_projects = [p for p in started_projects if p["title"] not in [cp["title"] for cp in completed_projects]]
        if active_projects:
            print("\nProjetos em andamento:")
            for i, project in enumerate(active_projects, 1):
                print(f"{i}. {project['title']} ({project['type']}) - Iniciado em {project['start_date']}")
        else:
            print("\nVocê não tem projetos em andamento.")

        # Mostrar projetos concluídos
        if completed_projects:
            print("\nProjetos concluídos:")
            for i, project in enumerate(completed_projects, 1):
                print(f"{i}. {project['title']} ({project['type']}) - Concluído em {project['completion_date']}")
        else:
            print("\nVocê ainda não concluiu nenhum projeto.")

        print("\nOpções:")
        print("1. Continuar um projeto em andamento")
        print("2. Marcar um projeto como concluído")
        print("3. Ver detalhes de um projeto concluído")
        print("4. Adicionar um novo projeto pessoal")
        print("0. Voltar")

        choice = input("\nSua escolha: ").strip()

        if choice == "0":
            break

        # Implementar as opções de gerenciamento de projetos com base
        # nas funções definidas anteriormente
        # ...

    # Nota: O restante da implementação do gerenciamento de projetos seguiria
    # o mesmo padrão que já foi definido anteriormente.

if __name__ == '__main__':
    main()