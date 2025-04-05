# progress_management.py (atualizado para a estrutura hierárquica)

from app.llm_integration import (
    call_teacher_llm,
    generate_complete_lesson,
    generate_assessment,
    LessonContent,
    TEACHING_STYLES,
    generate_learning_pathway
)
from google.cloud.firestore_v1.base_query import FieldFilter
import time


def continue_progress_flow(db, user_id):
    """
    Gerencia o fluxo de progresso linear (estilo "video-game") para o usuário.
    Versão atualizada para a estrutura hierárquica.
    """
    user_ref = db.collection("users").document(user_id)
    user_snap = user_ref.get()
    if not user_snap.exists:
        print("Usuário não encontrado. Faça o mapeamento primeiro.")
        return

    user_data = user_snap.to_dict()

    # Obter a estrutura hierárquica atual do usuário
    progress = user_data.get("progress", {})
    area_name = progress.get("area", "")

    if not area_name:
        print("Nenhuma área definida. Faça o mapeamento primeiro.")
        return

    # Obter dados da área
    area_ref = db.collection("learning_paths").document(area_name)
    area_doc = area_ref.get()
    if not area_doc.exists:
        print(f"Área '{area_name}' não encontrada. Pode ter sido removida.")
        return

    area_data = area_doc.to_dict()

    # Obter progresso atual do usuário
    current = progress.get("current", {})
    if not current:
        # Inicializar progresso se não existir
        subarea_name = ""
        subareas = area_data.get("subareas", {})
        if subareas:
            subarea_name = next(iter(subareas.keys()), "")

        current = {
            "subarea": subarea_name,
            "level": "iniciante",
            "module_index": 0,
            "lesson_index": 0,
            "step_index": 0
        }
        progress["current"] = current
        user_data["progress"] = progress
        user_ref.set(user_data, merge=True)

    # Obter a subárea atual
    subarea_name = current.get("subarea", "")
    if not subarea_name:
        print("Nenhuma subárea selecionada.")

        # Tentar selecionar uma subárea disponível
        subareas = area_data.get("subareas", {})
        if subareas:
            print("\nSubáreas disponíveis:")
            subareas_list = list(subareas.keys())

            for i, name in enumerate(subareas_list, 1):
                desc = subareas[name].get("description", "")[:80]
                print(f"{i}. {name} - {desc}")

            choice = input("\nEscolha uma subárea (número): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(subareas_list):
                subarea_name = subareas_list[int(choice) - 1]
                current["subarea"] = subarea_name
                user_data["progress"]["current"] = current
                user_ref.set(user_data, merge=True)
                print(f"\nSubárea '{subarea_name}' selecionada!")
            else:
                print("Escolha inválida. Voltando ao menu principal.")
                return
        else:
            print("Esta área não possui subáreas configuradas ainda.")
            return

    # Obter dados da subárea
    subareas = area_data.get("subareas", {})
    if subarea_name not in subareas:
        print(f"Subárea '{subarea_name}' não encontrada na área '{area_name}'.")
        return

    subarea_data = subareas[subarea_name]

    # Obter o nível atual
    level_name = current.get("level", "iniciante")
    levels = subarea_data.get("levels", {})

    if level_name not in levels:
        # Fallback para o primeiro nível disponível
        if levels:
            level_name = next(iter(levels.keys()), "iniciante")
            current["level"] = level_name
            user_data["progress"]["current"] = current
            user_ref.set(user_data, merge=True)
        else:
            print(f"A subárea '{subarea_name}' não possui níveis configurados.")
            return

    level_data = levels[level_name]

    # Obter os dados do usuário para personalização
    user_age = user_data.get("age", 14)  # Idade padrão se não estiver definida
    learning_style = user_data.get("learning_style", "didático")

    # Assegura que temos um estilo de ensino válido
    if learning_style not in TEACHING_STYLES:
        learning_style = "didático"

    # Iniciar o loop principal de aprendizado
    while True:
        # Exibir status atual
        _print_current_status(area_name, subarea_name, level_name, current, subarea_data, level_data)

        # Verificar requisitos para o nível atual
        if not _check_level_requirements(db, user_id, current, level_data):
            if input("Voltar ao menu principal? (s/n): ").lower() == 's':
                return
            else:
                continue

        # Menu de progresso
        print("\n=== Menu de Progresso (Estilo 'Video-game') ===")
        print("1. Continuar do ponto atual")
        print("2. Repetir a aula atual")
        print("3. Mudar de nível")
        print("4. Mudar de subárea")
        print("5. Perguntar ao professor")
        print("6. Gerar aula completa sobre o tópico atual")
        print("7. Gerar avaliação sobre o tópico")
        print("8. Gerar roteiro de aprendizado personalizado")
        print("9. Alterar estilo de ensino")
        print("10. Ver projetos disponíveis")
        print("0. Sair")

        choice = input("Escolha: ").strip()

        if choice == "1":
            _continue_next_step(db, user_id, user_data, area_name, subarea_name, level_name,
                                current, subarea_data, level_data, user_age, learning_style)
        elif choice == "2":
            _repeat_current_lesson(db, user_id, current)
        elif choice == "3":
            if _change_level(db, user_id, user_data, subarea_data):
                # Recarregar dados após a mudança
                user_snap = user_ref.get()
                user_data = user_snap.to_dict()
                progress = user_data.get("progress", {})
                current = progress.get("current", {})
                level_name = current.get("level", "iniciante")
                level_data = levels.get(level_name, {})
        elif choice == "4":
            if _change_subarea(db, user_id, user_data, area_data):
                # Recarregar dados após a mudança
                user_snap = user_ref.get()
                user_data = user_snap.to_dict()
                progress = user_data.get("progress", {})
                current = progress.get("current", {})
                subarea_name = current.get("subarea", "")
                subarea_data = subareas.get(subarea_name, {})
                level_name = current.get("level", "iniciante")
                levels = subarea_data.get("levels", {})
                level_data = levels.get(level_name, {})
        elif choice == "5":
            _ask_teacher(user_age, area_name, subarea_name, level_name, current, learning_style)
        elif choice == "6":
            _generate_complete_lesson(user_age, area_name, subarea_name, level_name, current, learning_style)
        elif choice == "7":
            _generate_assessment(user_age, area_name, subarea_name, level_name, current, learning_style)
        elif choice == "8":
            _generate_learning_pathway(user_age, area_name, subarea_name, level_name, current, learning_style)
        elif choice == "9":
            learning_style = _change_teaching_style(db, user_id)
        elif choice == "10":
            _view_available_projects(db, user_id, area_name, subarea_name, level_data)
        elif choice == "0":
            print("Saindo do modo linear.")
            break
        else:
            print("Opção inválida. Tente novamente.")


def _print_current_status(area_name, subarea_name, level_name, current, subarea_data, level_data):
    """
    Exibe o status atual de progresso do usuário.

    Args:
        area_name: Nome da área atual
        subarea_name: Nome da subárea atual
        level_name: Nome do nível atual
        current: Dicionário com o progresso atual do usuário
        subarea_data: Dados da subárea atual
        level_data: Dados do nível atual
    """
    module_index = current.get("module_index", 0)
    lesson_index = current.get("lesson_index", 0)
    step_index = current.get("step_index", 0)

    # Obter informações do módulo atual
    modules = level_data.get("modules", [])

    print("\n" + "=" * 60)
    print(f"PROGRESSO ATUAL")
    print("=" * 60)

    print(f"Área: {area_name}")
    print(f"Subárea: {subarea_name}")
    print(f"Nível: {level_name.capitalize()}")

    if modules and module_index < len(modules):
        module_data = modules[module_index]
        module_title = module_data.get("module_title", "Sem título")
        print(f"Módulo: {module_title}")

        lessons = module_data.get("lessons", [])
        if lessons and lesson_index < len(lessons):
            lesson_data = lessons[lesson_index]
            lesson_title = lesson_data.get("lesson_title", "Sem título")
            print(f"Aula: {lesson_title}")

            steps = lesson_data.get("steps", [])
            if steps:
                print(f"Passo: {step_index + 1}/{len(steps)}")
            else:
                print("Esta aula não possui passos definidos.")
    else:
        print("Módulo não definido ou todos os módulos foram concluídos.")


def _check_level_requirements(db, user_id, current, level_data):
    """
    Verifica se o usuário atende aos requisitos para o nível atual.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        current: Dicionário com o progresso atual
        level_data: Dados do nível atual

    Returns:
        True se os requisitos são atendidos, False caso contrário
    """
    # Verificar se há pré-requisitos
    prerequisites = level_data.get("prerequisites", [])
    if not prerequisites:
        return True

    # Buscar dados de conclusão do usuário
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return False

    user_data = user_doc.to_dict()
    completed_items = user_data.get("completed_modules", [])
    completed_titles = [item.get("title", "") for item in completed_items]

    missing_prereqs = []
    for prereq in prerequisites:
        if prereq not in completed_titles:
            missing_prereqs.append(prereq)

    if missing_prereqs:
        print("\n⚠️ Atenção! Este nível tem pré-requisitos que você ainda não completou:")
        for prereq in missing_prereqs:
            print(f"- {prereq}")

        override = input("\nDeseja continuar mesmo assim? (s/n): ").lower()
        return override == 's'

    return True


def _continue_next_step(db, user_id, user_data, area_name, subarea_name, level_name,
                        current, subarea_data, level_data, user_age, teaching_style):
    """
    Avança para o próximo passo na sequência de aprendizado.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        user_data: Dados do usuário
        area_name: Nome da área atual
        subarea_name: Nome da subárea atual
        level_name: Nome do nível atual
        current: Dicionário com o progresso atual
        subarea_data: Dados da subárea atual
        level_data: Dados do nível atual
        user_age: Idade do usuário
        teaching_style: Estilo de ensino preferido
    """
    module_index = current.get("module_index", 0)
    lesson_index = current.get("lesson_index", 0)
    step_index = current.get("step_index", 0)

    modules = level_data.get("modules", [])

    # Verificar se há módulos disponíveis
    if not modules:
        print("\nEste nível não possui módulos configurados ainda.")

        # Verificar se há projeto final ou avaliação final
        if _check_for_final_activities(db, user_id, level_name, level_data, user_age, teaching_style):
            _register_level_completion(db, user_id, area_name, subarea_name, level_name)

            # Avançar para o próximo nível se possível
            levels = subarea_data.get("levels", {})
            level_order = _get_level_order(levels)

            current_idx = level_order.index(level_name) if level_name in level_order else -1
            if current_idx >= 0 and current_idx < len(level_order) - 1:
                next_level = level_order[current_idx + 1]
                current["level"] = next_level
                current["module_index"] = 0
                current["lesson_index"] = 0
                current["step_index"] = 0

                user_data["progress"]["current"] = current
                db.collection("users").document(user_id).set(user_data, merge=True)

                print(f"\nParabéns! Você avançou para o nível {next_level.capitalize()}!")
        return

    # Verificar se já concluiu todos os módulos
    if module_index >= len(modules):
        print("\nVocê já concluiu todos os módulos deste nível!")

        # Verificar se há projeto final ou avaliação final
        if _check_for_final_activities(db, user_id, level_name, level_data, user_age, teaching_style):
            _register_level_completion(db, user_id, area_name, subarea_name, level_name)

            # Avançar para o próximo nível se possível
            levels = subarea_data.get("levels", {})
            level_order = _get_level_order(levels)

            current_idx = level_order.index(level_name) if level_name in level_order else -1
            if current_idx >= 0 and current_idx < len(level_order) - 1:
                next_level = level_order[current_idx + 1]
                current["level"] = next_level
                current["module_index"] = 0
                current["lesson_index"] = 0
                current["step_index"] = 0

                user_data["progress"]["current"] = current
                db.collection("users").document(user_id).set(user_data, merge=True)

                print(f"\nParabéns! Você avançou para o nível {next_level.capitalize()}!")
        return

    # Obter o módulo atual
    module_data = modules[module_index]
    module_title = module_data.get("module_title", "Sem título")

    lessons = module_data.get("lessons", [])

    # Verificar se há lições disponíveis
    if not lessons:
        print(f"\nO módulo '{module_title}' não possui lições configuradas ainda.")

        # Verificar se há projeto ou avaliação do módulo
        if _check_for_module_activities(db, user_id, level_name, module_data, user_age, teaching_style):
            _register_module_completion(db, user_id, module_title)

            # Avançar para o próximo módulo
            current["module_index"] = module_index + 1
            current["lesson_index"] = 0
            current["step_index"] = 0

            user_data["progress"]["current"] = current
            db.collection("users").document(user_id).set(user_data, merge=True)

            print(f"\nParabéns! Você concluiu o módulo '{module_title}'!")
        return

    # Verificar se já concluiu todas as lições do módulo
    if lesson_index >= len(lessons):
        print(f"\nVocê já concluiu todas as lições do módulo '{module_title}'!")

        # Verificar se há projeto ou avaliação do módulo
        if _check_for_module_activities(db, user_id, level_name, module_data, user_age, teaching_style):
            _register_module_completion(db, user_id, module_title)

            # Avançar para o próximo módulo
            current["module_index"] = module_index + 1
            current["lesson_index"] = 0
            current["step_index"] = 0

            user_data["progress"]["current"] = current
            db.collection("users").document(user_id).set(user_data, merge=True)

            print(f"\nParabéns! Você concluiu o módulo '{module_title}'!")
        return

    # Obter a lição atual
    lesson_data = lessons[lesson_index]
    lesson_title = lesson_data.get("lesson_title", "Sem título")

    steps = lesson_data.get("steps", [])

    # Verificar se a lição não tem passos definidos
    if not steps:
        print(f"\nA lição '{lesson_title}' não possui passos definidos.")

        # Oferecer conteúdo gerado
        _generate_lesson_content(lesson_title, lesson_data.get("objectives", ""),
                                 user_age, area_name, subarea_name, teaching_style)

        # Verificar se há exercícios ou projeto da lição
        if _check_for_lesson_activities(db, user_id, lesson_data, user_age, teaching_style):
            _register_lesson_completion(db, user_id, lesson_title)

            # Avançar para a próxima lição
            current["lesson_index"] = lesson_index + 1
            current["step_index"] = 0

            user_data["progress"]["current"] = current
            db.collection("users").document(user_id).set(user_data, merge=True)

            print(f"\nParabéns! Você concluiu a lição '{lesson_title}'!")
        return

    # Verificar se já concluiu todos os passos da lição
    if step_index >= len(steps):
        print(f"\nVocê já concluiu todos os passos da lição '{lesson_title}'!")

        # Verificar se há exercícios ou projeto da lição
        if _check_for_lesson_activities(db, user_id, lesson_data, user_age, teaching_style):
            _register_lesson_completion(db, user_id, lesson_title)

            # Avançar para a próxima lição
            current["lesson_index"] = lesson_index + 1
            current["step_index"] = 0

            user_data["progress"]["current"] = current
            db.collection("users").document(user_id).set(user_data, merge=True)

            print(f"\nParabéns! Você concluiu a lição '{lesson_title}'!")
        return

    # Apresentar o passo atual
    step_content = steps[step_index]

    print(f"\n=== [Aula: {lesson_title} | Passo {step_index + 1}/{len(steps)}] ===")
    print("Gerando conteúdo...")

    # Gerar conteúdo para o passo atual
    context = f"Área: {area_name}, Subárea: {subarea_name}, Nível: {level_name}, Módulo: {module_title}, Lição: {lesson_title}"

    prompt = (
        f"Explique de forma didática e adequada para um estudante de {user_age} anos: {step_content}. "
        f"Contexto da aula: {context}. "
        f"Use linguagem acessível e exemplos práticos. Relacione com o dia a dia quando possível. "
        f"Mantenha o foco específico neste tópico."
    )

    explanation = call_teacher_llm(
        prompt,
        student_age=user_age,
        subject_area=area_name,
        teaching_style=teaching_style,
        knowledge_level=level_name
    )

    print(explanation)

    # Avançar para o próximo passo
    current["step_index"] = step_index + 1
    user_data["progress"]["current"] = current
    db.collection("users").document(user_id).set(user_data, merge=True)

    print(f"\n[Progresso] Passo {step_index + 1}/{len(steps)} concluído na aula '{lesson_title}'.")
    print("Use [1] para continuar ou escolha outra opção.")


def _check_for_final_activities(db, user_id, level_name, level_data, user_age, teaching_style):
    """
    Verifica e oferece atividades finais do nível (projeto final, avaliação).

    Returns:
        True se as atividades foram concluídas, False caso contrário
    """
    final_project = level_data.get("final_project", {})
    final_assessment = level_data.get("final_assessment", {})

    if not final_project and not final_assessment:
        return True

    # Oferecer projeto final, se disponível
    if final_project:
        project_title = final_project.get("title", "Projeto Final")
        project_desc = final_project.get("description", "")

        print(f"\n=== Projeto Final: {project_title} ===")
        print(f"Descrição: {project_desc}")

        do_project = input("\nDeseja iniciar este projeto final agora? (s/n): ").lower()
        if do_project == 's':
            # Gerar orientações para o projeto
            requirements = final_project.get("requirements", [])
            req_text = ", ".join(requirements) if requirements else ""

            prompt = (
                f"O aluno de {user_age} anos precisa realizar o projeto final: '{project_title}'. "
                f"Descrição: {project_desc}. "
                f"Requisitos: {req_text}. "
                f"Forneça um guia passo a passo detalhado sobre como realizar este projeto, "
                f"usando linguagem adequada para a idade do aluno."
            )

            guidance = call_teacher_llm(
                prompt,
                student_age=user_age,
                teaching_style=teaching_style,
                max_tokens=2500
            )

            print("\n" + "=" * 60)
            print(guidance)
            print("=" * 60)

            # Registrar o projeto como iniciado
            _register_project_started(db, user_id, project_title, "final")

            completed = input("\nVocê completou o projeto final? (s/n): ").lower()
            if completed == 's':
                _register_project_completed(db, user_id, project_title, "final")
                return True

    # Oferecer avaliação final, se disponível
    if final_assessment:
        assessment_title = final_assessment.get("title", "Avaliação Final")
        passing_criteria = final_assessment.get("passing_criteria", "")

        print(f"\n=== Avaliação Final: {assessment_title} ===")
        if passing_criteria:
            print(f"Critérios de aprovação: {passing_criteria}")

        do_assessment = input("\nDeseja fazer a avaliação final agora? (s/n): ").lower()
        if do_assessment == 's':
            # Gerar avaliação

            assessment_data = generate_assessment(
                topic=assessment_title,
                difficulty=level_name,
                num_questions=5,
                question_types=["múltipla escolha", "verdadeiro/falso", "dissertativa"]
            )

            score = _apply_assessment(assessment_data, user_age, teaching_style)

            # Verificar se passou
            passing_score = 70  # Valor padrão

            if score >= passing_score:
                print(f"\nParabéns! Você passou na avaliação final com {score}%!")

                # Registrar aprovação
                _register_final_assessment_passed(db, user_id, level_name, score)

                # Emitir certificação, se disponível
                certification = final_assessment.get("certification", "")
                if certification:
                    _award_certification(db, user_id, certification)

                return True
            else:
                print(f"\nVocê obteve {score}%, abaixo da nota de aprovação.")
                print("Revise o conteúdo e tente novamente quando estiver preparado.")

    return False


def _check_for_module_activities(db, user_id, level_name, module_data, user_age, teaching_style):
    """
    Verifica e oferece atividades do módulo (projeto, avaliação).

    Returns:
        True se as atividades foram concluídas, False caso contrário
    """
    module_project = module_data.get("module_project", {})
    module_assessment = module_data.get("module_assessment", {})

    if not module_project and not module_assessment:
        return True

    # Oferecer projeto do módulo, se disponível
    if module_project:
        project_title = module_project.get("title", "Projeto do Módulo")
        project_desc = module_project.get("description", "")

        print(f"\n=== Projeto do Módulo: {project_title} ===")
        print(f"Descrição: {project_desc}")

        do_project = input("\nDeseja iniciar este projeto agora? (s/n): ").lower()
        if do_project == 's':
            # Gerar orientações para o projeto
            deliverables = module_project.get("deliverables", [])
            deliv_text = ", ".join(deliverables) if deliverables else ""

            prompt = (
                f"O aluno de {user_age} anos precisa realizar o projeto: '{project_title}'. "
                f"Descrição: {project_desc}. "
                f"Entregas esperadas: {deliv_text}. "
                f"Forneça um guia passo a passo sobre como desenvolver este projeto, "
                f"usando linguagem adequada para a idade do aluno."
            )

            guidance = call_teacher_llm(
                prompt,
                student_age=user_age,
                teaching_style=teaching_style,
                max_tokens=2000
            )

            print("\n" + "=" * 60)
            print(guidance)
            print("=" * 60)

            # Registrar o projeto como iniciado
            _register_project_started(db, user_id, project_title, "module")

            completed = input("\nVocê completou o projeto do módulo? (s/n): ").lower()
            if completed == 's':
                _register_project_completed(db, user_id, project_title, "module")
                return True

    # Oferecer avaliação do módulo, se disponível
    if module_assessment:
        assessment_title = module_assessment.get("title", "Avaliação do Módulo")
        passing_score = module_assessment.get("passing_score", 70)

        print(f"\n=== Avaliação do Módulo: {assessment_title} ===")
        print(f"Nota para aprovação: {passing_score}%")

        do_assessment = input("\nDeseja fazer esta avaliação agora? (s/n): ").lower()
        if do_assessment == 's':
            # Gerar avaliação
            assessment_data = generate_assessment(
                topic=assessment_title,
                difficulty=level_name,
                num_questions=3,
                question_types=["múltipla escolha", "verdadeiro/falso"]
            )

            score = _apply_assessment(assessment_data, user_age, teaching_style)

            if score >= passing_score:
                print(f"\nParabéns! Você passou na avaliação com {score}%!")

                # Registrar aprovação
                _register_assessment_passed(db, user_id, module_data.get("module_title", ""), score)

                return True
            else:
                print(f"\nVocê obteve {score}%, abaixo da nota de aprovação de {passing_score}%.")
                print("Revise o conteúdo do módulo antes de tentar novamente.")

    return False


def _check_for_lesson_activities(db, user_id, lesson_data, user_age, teaching_style):
    """
    Verifica e oferece atividades da lição (exercícios, projeto).

    Returns:
        True se as atividades foram concluídas, False caso contrário
    """
    exercises = lesson_data.get("exercises", [])
    project = lesson_data.get("project", {})

    # Oferecer exercícios, se disponíveis
    if exercises:
        print(f"\n=== Exercícios da Aula ===")

        do_exercises = input("Deseja fazer os exercícios agora? (s/n): ").lower()
        if do_exercises == 's':
            for i, exercise in enumerate(exercises, 1):
                question = exercise.get("question", "")
                question_type = exercise.get("type", "open")
                answer = exercise.get("answer", "")

                print(f"\nExercício {i}: {question}")

                if question_type == "multiple_choice" and "options" in exercise:
                    options = exercise.get("options", [])
                    for j, option in enumerate(options):
                        print(f"  {chr(65 + j)}. {option}")

                    user_ans = input("Sua resposta (letra): ").strip().upper()
                    correct_idx = exercise.get("correct_answer", 0)
                    correct_letter = chr(65 + int(correct_idx))

                    if user_ans == correct_letter:
                        print("✓ Correto!")
                    else:
                        print(f"✗ Incorreto. A resposta correta é {correct_letter}.")

                    print(f"Explicação: {exercise.get('explanation', 'Não disponível')}")
                else:
                    user_ans = input("Sua resposta: ").strip()

                    # Gerar feedback
                    prompt = (
                        f"O aluno de {user_age} anos respondeu '{user_ans}' para a pergunta: '{question}'. "
                        f"A resposta esperada era: '{answer}'. "
                        f"Avalie a resposta do aluno de forma construtiva e educativa, "
                        f"usando linguagem apropriada para a idade."
                    )

                    feedback = call_teacher_llm(
                        prompt,
                        student_age=user_age,
                        teaching_style=teaching_style,
                        max_tokens=500
                    )

                    print(f"\nFeedback: {feedback}")

    # Oferecer projeto da lição, se disponível
    if project:
        project_title = project.get("title", "Projeto da Aula")
        project_desc = project.get("description", "")

        print(f"\n=== Projeto da Aula: {project_title} ===")
        print(f"Descrição: {project_desc}")

        do_project = input("\nDeseja iniciar este projeto agora? (s/n): ").lower()
        if do_project == 's':
            # Gerar orientações para o projeto
            prompt = (
                f"O aluno de {user_age} anos precisa realizar o projeto: '{project_title}'. "
                f"Descrição: {project_desc}. "
                f"Forneça instruções passo a passo sobre como realizar este projeto, "
                f"usando linguagem adequada para a idade do aluno."
            )

            guidance = call_teacher_llm(
                prompt,
                student_age=user_age,
                teaching_style=teaching_style,
                max_tokens=1500
            )

            print("\n" + "=" * 60)
            print(guidance)
            print("=" * 60)

            # Registrar o projeto como iniciado
            _register_project_started(db, user_id, project_title, "lesson")

            completed = input("\nVocê completou o projeto da aula? (s/n): ").lower()
            if completed == 's':
                _register_project_completed(db, user_id, project_title, "lesson")
                return True

    # Se não houver atividades ou o usuário optar por não fazê-las
    return input("\nDeseja marcar esta lição como concluída? (s/n): ").lower() == 's'


def _generate_lesson_content(lesson_title, objectives, user_age, area_name, subarea_name, teaching_style):
    """
    Gera conteúdo para uma lição que não tem passos definidos.
    """
    print(f"\nGerando conteúdo para a lição: {lesson_title}")

    prompt = (
        f"Crie um conteúdo educacional sobre '{lesson_title}' para um estudante de {user_age} anos. "
        f"Objetivos de aprendizado: {objectives}. "
        f"Área: {area_name}, Subárea: {subarea_name}. "
        f"Use linguagem acessível, exemplos práticos e relacione com o dia a dia quando possível. "
        f"O conteúdo deve ser estruturado, informativo e envolvente."
    )

    content = call_teacher_llm(
        prompt,
        student_age=user_age,
        subject_area=f"{area_name} - {subarea_name}",
        teaching_style=teaching_style,
        max_tokens=2000
    )

    print("\n" + "=" * 60)
    print(content)
    print("=" * 60)


def _repeat_current_lesson(db, user_id, current):
    """
    Reinicia a lição atual, voltando para o primeiro passo.
    """
    current["step_index"] = 0

    # Atualizar no Firestore
    user_ref = db.collection("users").document(user_id)
    user_ref.update({"progress.current": current})

    print("A lição atual foi reiniciada. Você poderá rever todos os passos novamente.")


def _change_level(db, user_id, user_data, subarea_data):
    """
    Permite ao usuário mudar para outro nível dentro da mesma subárea.

    Returns:
        True se o nível foi alterado, False caso contrário
    """
    levels = subarea_data.get("levels", {})
    if not levels:
        print("Esta subárea não possui níveis configurados.")
        return False

    print("\n=== Níveis Disponíveis ===")
    level_names = list(levels.keys())

    for i, level_name in enumerate(level_names, 1):
        level_desc = levels[level_name].get("description", "")[:80]
        print(f"{i}. {level_name.capitalize()} - {level_desc}")

    choice = input("\nEscolha um nível (número): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(level_names):
        print("Escolha inválida.")
        return False

    level_idx = int(choice) - 1
    selected_level = level_names[level_idx]

    # Atualizar o progresso do usuário
    progress = user_data.get("progress", {})
    current = progress.get("current", {})

    current["level"] = selected_level
    current["module_index"] = 0
    current["lesson_index"] = 0
    current["step_index"] = 0

    # Atualizar no Firestore
    db.collection("users").document(user_id).update({"progress.current": current})

    print(f"\nNível alterado para '{selected_level.capitalize()}'.")
    return True


def _change_subarea(db, user_id, user_data, area_data):
    """
    Permite ao usuário mudar para outra subárea dentro da mesma área.

    Returns:
        True se a subárea foi alterada, False caso contrário
    """
    subareas = area_data.get("subareas", {})
    if not subareas:
        print("Esta área não possui subáreas configuradas.")
        return False

    print("\n=== Subáreas Disponíveis ===")
    subarea_names = list(subareas.keys())

    for i, subarea_name in enumerate(subarea_names, 1):
        subarea_desc = subareas[subarea_name].get("description", "")[:80]
        print(f"{i}. {subarea_name} - {subarea_desc}")

    choice = input("\nEscolha uma subárea (número): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(subarea_names):
        print("Escolha inválida.")
        return False

    subarea_idx = int(choice) - 1
    selected_subarea = subarea_names[subarea_idx]

    # Atualizar o progresso do usuário
    progress = user_data.get("progress", {})
    current = progress.get("current", {})

    current["subarea"] = selected_subarea
    current["level"] = "iniciante"  # Volta para o nível iniciante por padrão
    current["module_index"] = 0
    current["lesson_index"] = 0
    current["step_index"] = 0

    db.collection("users").document(user_id).update({"progress.current": current})

    print(f"\nSubárea alterada para '{selected_subarea}'.")
    return True


def _ask_teacher(user_age, area_name, subarea_name, level_name, current, teaching_style):
    """
    Permite ao usuário fazer perguntas ao professor virtual.
    """
    question = input("\n[Pergunta ao professor] ").strip()

    if not question:
        print("Pergunta vazia.")
        return

    # Determinar o contexto atual
    context = f"área de {area_name}, subárea de {subarea_name}, nível {level_name}"

    print("\nPensando...")
    answer = call_teacher_llm(
        f"O aluno está estudando {context} e pergunta: '{question}'. "
        f"Responda de forma adequada para um estudante de {user_age} anos, "
        f"usando linguagem clara e exemplos relevantes.",
        student_age=user_age,
        subject_area=area_name,
        teaching_style=teaching_style
    )

    print(f"\n[Professor]: {answer}")
    input("\nPressione Enter para continuar...")


def _generate_complete_lesson(user_age, area_name, subarea_name, level_name, current, teaching_style):
    """
    Gera uma aula completa sobre o tópico atual.
    """
    # Determinar o tópico com base no contexto atual
    topic = f"{subarea_name} - {level_name}"

    print(f"\nGerando aula completa sobre '{topic}'...")

    lesson = generate_complete_lesson(
        topic=topic,
        subject_area=area_name,
        age_range=user_age,
        knowledge_level=level_name,
        teaching_style=teaching_style,
        lesson_duration_min=30
    )

    print("\n" + "=" * 80)
    print(lesson.to_text())
    print("=" * 80)

    input("\nPressione Enter para continuar...")


def _generate_assessment(user_age, area_name, subarea_name, level_name, current, teaching_style):
    """
    Gera uma avaliação sobre o tópico atual.
    """
    # Determinar o tópico com base no contexto atual
    topic = f"{subarea_name} - {level_name}"

    print(f"\nGerando avaliação sobre '{topic}'...")

    assessment = generate_assessment(
        topic=topic,
        difficulty=level_name,
        num_questions=3,
        question_types=["múltipla escolha", "verdadeiro/falso", "dissertativa"]
    )

    print(f"\n=== {assessment['title']} ===\n")

    for i, question in enumerate(assessment["questions"], 1):
        print(f"Questão {i}: {question['text']}")

        if question["type"] == "múltipla escolha":
            for j, option in enumerate(question["options"]):
                print(f"  {chr(65 + j)}. {option}")

            answer = input("\nSua resposta (letra): ").strip().upper()
            correct_idx = question["correct_answer"]
            correct_letter = chr(65 + int(correct_idx))

            if answer == correct_letter:
                print("✓ Correto!")
            else:
                print(f"✗ Incorreto. A resposta correta é {correct_letter}.")

            print(f"Explicação: {question['explanation']}\n")

        elif question["type"] == "verdadeiro/falso":
            answer = input("\nVerdadeiro ou Falso? (V/F): ").strip().upper()
            is_true = question["correct_answer"]
            correct_answer = "V" if is_true else "F"

            if answer == correct_answer:
                print("✓ Correto!")
            else:
                print(f"✗ Incorreto. A resposta correta é {correct_answer}.")

            print(f"Explicação: {question['explanation']}\n")

        elif question["type"] == "dissertativa":
            print("\nEsta é uma questão dissertativa.")
            user_answer = input("Sua resposta: ").strip()

            print("\nPontos-chave que deveriam ser abordados:")
            for point in question["key_points"]:
                print(f"- {point}")

            print(f"\nExemplo de resposta adequada:\n{question['sample_answer']}\n")

    input("\nPressione Enter para continuar...")


def _generate_learning_pathway(user_age, area_name, subarea_name, level_name, current, teaching_style):
    """
    Gera um roteiro de aprendizado personalizado.
    """
    # Determinar o tópico com base no contexto atual
    topic = f"{subarea_name} ({area_name})"

    print(f"\nGerando roteiro de aprendizado para '{topic}'...")

    duration_weeks = 4
    try:
        duration_str = input("Duração desejada em semanas [padrão: 4]: ").strip()
        if duration_str.isdigit():
            duration_weeks = int(duration_str)
    except:
        pass

    hours_per_week = 3
    try:
        hours_str = input("Horas de estudo por semana [padrão: 3]: ").strip()
        if hours_str.isdigit():
            hours_per_week = int(hours_str)
    except:
        pass

    print("\nGerando roteiro personalizado...")

    pathway = generate_learning_pathway(
        topic=topic,
        duration_weeks=duration_weeks,
        hours_per_week=hours_per_week,
        initial_level=level_name,
        target_level="avançado"
    )

    print(f"\n=== ROTEIRO DE APRENDIZADO: {pathway['title']} ===\n")
    print(pathway['description'])
    print("\nPLANO SEMANAL:")

    for week in pathway['weekly_plan']:
        print(f"\nSEMANA {week['week']}: {week['focus']}")
        print("Objetivos:")
        for obj in week['objectives']:
            print(f"- {obj}")

        print("Atividades:")
        for activity in week['activities']:
            print(f"• {activity['title']} ({activity['duration_minutes']} min)")
            print(f"  {activity['description']}")
            if activity.get('resources'):
                print("  Recursos:")
                for resource in activity['resources']:
                    print(f"  - {resource}")

        print(f"Avaliação: {week['assessment']}")

    print(f"\nPROJETO FINAL: {pathway['final_project']}")

    print("\nRECURSOS ADICIONAIS:")
    for resource in pathway['additional_resources']:
        print(f"- {resource}")

    input("\nPressione Enter para continuar...")


def _change_teaching_style(db, user_id):
    """
    Permite ao usuário alterar o estilo de ensino.

    Returns:
        O novo estilo de ensino selecionado
    """
    print("\n=== Estilos de Ensino Disponíveis ===")
    for i, (style, desc) in enumerate(TEACHING_STYLES.items(), 1):
        print(f"{i}. {style.capitalize()} - {desc}")

    style_choice = input("\nEscolha um estilo (número): ").strip()
    if style_choice.isdigit():
        idx = int(style_choice) - 1
        if 0 <= idx < len(TEACHING_STYLES):
            learning_style = list(TEACHING_STYLES.keys())[idx]

            # Salvar preferência no perfil do usuário
            db.collection("users").document(user_id).update({"learning_style": learning_style})

            print(f"\nEstilo de ensino alterado para '{learning_style}'.")
            return learning_style

    print("Escolha inválida. Mantendo o estilo atual.")
    return "didático"  # Estilo padrão


def _view_available_projects(db, user_id, area_name, subarea_name, level_data):
    """
    Permite ao usuário ver os projetos disponíveis no nível atual.
    """
    projects = []

    # Verificar se há projeto final no nível
    final_project = level_data.get("final_project", {})
    if final_project:
        project_title = final_project.get("title", "")
        if project_title:
            projects.append({
                "title": project_title,
                "description": final_project.get("description", ""),
                "type": "final",
                "source": "level"
            })

    # Verificar projetos em módulos
    modules = level_data.get("modules", [])
    for module in modules:
        module_title = module.get("module_title", "")

        # Projeto do módulo
        module_project = module.get("module_project", {})
        if module_project:
            project_title = module_project.get("title", "")
            if project_title:
                projects.append({
                    "title": project_title,
                    "description": module_project.get("description", ""),
                    "type": "module",
                    "source": f"Módulo: {module_title}"
                })

        # Projetos em lições
        lessons = module.get("lessons", [])
        for lesson in lessons:
            lesson_title = lesson.get("lesson_title", "")

            lesson_project = lesson.get("project", {})
            if lesson_project:
                project_title = lesson_project.get("title", "")
                if project_title:
                    projects.append({
                        "title": project_title,
                        "description": lesson_project.get("description", ""),
                        "type": "lesson",
                        "source": f"Aula: {lesson_title} (Módulo: {module_title})"
                    })

    if not projects:
        print("\nNão há projetos disponíveis neste nível.")
        input("\nPressione Enter para continuar...")
        return

    # Mostrar projetos disponíveis
    print("\n=== Projetos Disponíveis ===")
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project['title']} ({project['type'].capitalize()})")
        print(f"   {project['description']}")
        print(f"   Fonte: {project['source']}")

    choice = input("\nSelecione um projeto para iniciar (número) ou 0 para voltar: ").strip()
    if choice == "0" or not choice.isdigit() or int(choice) < 1 or int(choice) > len(projects):
        return

    selected_project = projects[int(choice) - 1]

    # Registrar o projeto como iniciado
    _register_project_started(db, user_id, selected_project['title'], selected_project['type'])

    print(f"\nVocê iniciou o projeto '{selected_project['title']}'.")
    print("Você pode continuar trabalhando nele e marcá-lo como concluído no menu de gerenciamento de projetos.")

    input("\nPressione Enter para continuar...")


def _apply_assessment(assessment_data, user_age, teaching_style):
    """
    Aplica uma avaliação ao usuário e retorna a pontuação obtida.
    """
    questions = assessment_data.get("questions", [])
    if not questions:
        return 0

    correct_answers = 0
    total_questions = len(questions)

    print(f"\n=== {assessment_data.get('title', 'Avaliação')} ===\n")

    for i, question in enumerate(questions, 1):
        print(f"Questão {i}: {question.get('text', '')}")

        if question.get("type") == "múltipla escolha":
            options = question.get("options", [])
            for j, option in enumerate(options):
                print(f"  {chr(65 + j)}. {option}")

            user_answer = input("\nSua resposta (letra): ").strip().upper()
            correct_idx = question.get("correct_answer", 0)
            correct_letter = chr(65 + int(correct_idx))

            if user_answer == correct_letter:
                print("✓ Correto!")
                correct_answers += 1
            else:
                print(f"✗ Incorreto. A resposta correta é {correct_letter}.")

            print(f"Explicação: {question.get('explanation', '')}\n")

        elif question.get("type") == "verdadeiro/falso":
            user_answer = input("\nVerdadeiro ou Falso? (V/F): ").strip().upper()
            is_true = question.get("correct_answer", False)
            correct_answer = "V" if is_true else "F"

            if user_answer == correct_answer:
                print("✓ Correto!")
                correct_answers += 1
            else:
                print(f"✗ Incorreto. A resposta correta é {correct_answer}.")

            print(f"Explicação: {question.get('explanation', '')}\n")

        elif question.get("type") == "dissertativa":
            print("\nEsta é uma questão dissertativa.")
            user_answer = input("Sua resposta: ").strip()

            # Para questões dissertativas, usamos o LLM para avaliar
            key_points = question.get("key_points", [])
            sample_answer = question.get("sample_answer", "")

            prompt = (
                f"Avalie a resposta de um aluno de {user_age} anos à seguinte questão dissertativa:\n"
                f"Questão: {question.get('text', '')}\n\n"
                f"Resposta do aluno: {user_answer}\n\n"
                f"Pontos-chave esperados: {', '.join(key_points)}\n"
                f"Exemplo de resposta adequada: {sample_answer}\n\n"
                f"Decida se a resposta é satisfatória (inclui pelo menos 70% dos pontos-chave) "
                f"e forneça feedback construtivo."
            )

            evaluation = call_teacher_llm(
                prompt,
                student_age=user_age,
                teaching_style=teaching_style,
                max_tokens=1000
            )

            print("\nAvaliação:")
            print(evaluation)

            is_correct = input("\nA resposta foi satisfatória? (s/n, decidido pelo professor): ").lower() == 's'
            if is_correct:
                correct_answers += 1

    score = (correct_answers / total_questions) * 100
    return score


def _get_level_order(levels):
    """
    Retorna uma lista ordenada dos níveis (iniciante -> intermediário -> avançado).
    """
    preferred_order = ["iniciante", "basico", "intermediario", "avancado"]
    level_names = list(levels.keys())

    # Primeiro incluir os níveis na ordem preferida
    ordered_levels = []
    for level in preferred_order:
        if level in level_names:
            ordered_levels.append(level)

    # Depois incluir outros níveis não presentes na ordem preferida
    for level in level_names:
        if level not in ordered_levels:
            ordered_levels.append(level)

    return ordered_levels


# Funções para registrar progresso e atividades

def _register_project_started(db, user_id, project_title, project_type):
    """
    Registra o início de um projeto no perfil do usuário.
    """
    user_ref = db.collection("users").document(user_id)

    # Estrutura do projeto iniciado
    project_data = {
        "title": project_title,
        "type": project_type,
        "start_date": time.strftime("%Y-%m-%d"),
        "status": "in_progress"
    }

    # Adicionar à lista de projetos iniciados
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "started_projects": ArrayUnion([project_data])
    })


def _register_project_completed(db, user_id, project_title, project_type):
    """
    Registra a conclusão de um projeto no perfil do usuário.
    """
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print("Erro: dados do usuário não encontrados.")
        return

    user_data = user_doc.to_dict()
    started_projects = user_data.get("started_projects", [])

    # Encontrar o projeto na lista de iniciados
    project_found = False
    for project in started_projects:
        if project["title"] == project_title and project["type"] == project_type:
            project_found = True
            # Marcar como concluído
            project["status"] = "completed"
            break

    if not project_found:
        # Se o projeto não foi encontrado na lista de iniciados, criá-lo agora
        project_data = {
            "title": project_title,
            "type": project_type,
            "start_date": time.strftime("%Y-%m-%d"),
            "status": "completed"
        }
        started_projects.append(project_data)

    # Estrutura do projeto concluído
    completed_project = {
        "title": project_title,
        "type": project_type,
        "start_date": next(
            (p["start_date"] for p in started_projects if p["title"] == project_title and p["type"] == project_type),
            time.strftime("%Y-%m-%d")),
        "completion_date": time.strftime("%Y-%m-%d")
    }

    # Atualizar o perfil do usuário
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "started_projects": started_projects,
        "completed_projects": ArrayUnion([completed_project])
    })


def _register_lesson_completion(db, user_id, lesson_title):
    """
    Registra a conclusão de uma lição no perfil do usuário.
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar à lista de lições concluídas
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "completed_lessons": ArrayUnion([{
            "title": lesson_title,
            "completion_date": time.strftime("%Y-%m-%d")
        }])
    })


def _register_module_completion(db, user_id, module_title):
    """
    Registra a conclusão de um módulo no perfil do usuário.
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar à lista de módulos concluídos
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "completed_modules": ArrayUnion([{
            "title": module_title,
            "completion_date": time.strftime("%Y-%m-%d")
        }])
    })


def _register_level_completion(db, user_id, area_name, subarea_name, level_name):
    """
    Registra a conclusão de um nível no perfil do usuário.
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar à lista de níveis concluídos
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "completed_levels": ArrayUnion([{
            "area": area_name,
            "subarea": subarea_name,
            "level": level_name,
            "completion_date": time.strftime("%Y-%m-%d")
        }])
    })


def _register_assessment_passed(db, user_id, module_title, score):
    """
    Registra a aprovação em uma avaliação de módulo.
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar à lista de avaliações concluídas
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "passed_assessments": ArrayUnion([{
            "module": module_title,
            "score": score,
            "date": time.strftime("%Y-%m-%d")
        }])
    })


def _register_final_assessment_passed(db, user_id, level_name, score):
    """
    Registra a aprovação em uma avaliação final de nível.
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar à lista de avaliações finais concluídas
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "passed_final_assessments": ArrayUnion([{
            "level": level_name,
            "score": score,
            "date": time.strftime("%Y-%m-%d")
        }])
    })


def _award_certification(db, user_id, certification_title):
    """
    Emite uma certificação para o usuário.
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar à lista de certificações
    from google.cloud.firestore import ArrayUnion
    user_ref.update({
        "certifications": ArrayUnion([{
            "title": certification_title,
            "date": time.strftime("%Y-%m-%d"),
            "id": f"CERT-{int(time.time())}"
        }])
    })

    print(f"\n🎓 Parabéns! Você obteve a certificação: {certification_title}")


def dynamic_progress_flow(db, user_id):
    """
    Gerencia o fluxo de progresso dinâmico onde o usuário escolhe as subáreas.
    Versão atualizada para a nova estrutura hierárquica.
    """
    user_ref = db.collection("users").document(user_id)
    snap = user_ref.get()
    if not snap.exists:
        print("Usuário não encontrado.")
        return

    user_data = snap.to_dict()
    area_name = user_data.get("recommended_track", "")

    if not area_name:
        print("Nenhuma área recomendada. Faça o mapeamento primeiro.")
        return

    # Obter os dados do usuário para personalização
    user_age = user_data.get("age", 14)
    learning_style = user_data.get("learning_style", "didático")

    # Carrega dados da área
    area_ref = db.collection("learning_paths").document(area_name)
    area_doc = area_ref.get()

    if not area_doc.exists:
        print(f"Área '{area_name}' não encontrada.")
        return

    area_data = area_doc.to_dict()
    subareas = area_data.get("subareas", {})

    if not subareas:
        print("Esta área não possui subáreas configuradas.")
        return

    while True:
        print(f"\n=== Modo Dinâmico: Área {area_name} ===")
        print("Escolha uma subárea para explorar:")

        # Listar subáreas disponíveis
        subarea_names = list(subareas.keys())
        for i, subarea_name in enumerate(subarea_names, 1):
            subarea_data = subareas[subarea_name]
            short_desc = subarea_data.get("description", "")[:60]
            print(f"{i}. {subarea_name} - {short_desc}")

        print("0. Voltar")

        choice = input("\nSua escolha: ").strip()
        if choice == "0":
            break

        if choice.isdigit() and 1 <= int(choice) <= len(subarea_names):
            selected_subarea = subarea_names[int(choice) - 1]

            # Explorar a subárea selecionada
            explore_subarea(db, user_id, area_name, area_data, selected_subarea, user_age, learning_style)
        else:
            print("Opção inválida.")


def explore_subarea(db, user_id, area_name, area_data, subarea_name, user_age, learning_style):
    """
    Permite ao usuário explorar uma subárea específica.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        area_name: Nome da área atual
        area_data: Dados da área
        subarea_name: Nome da subárea selecionada
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    subareas = area_data.get("subareas", {})
    if subarea_name not in subareas:
        print(f"Subárea '{subarea_name}' não encontrada.")
        return

    subarea_data = subareas[subarea_name]

    # Mostrar informações da subárea
    print(f"\n=== Subárea: {subarea_name} ===")

    description = subarea_data.get("description", "")
    if description:
        print(f"Descrição: {description}")

    est_time = subarea_data.get("estimated_time", "")
    if est_time:
        print(f"Tempo estimado: {est_time}")

    # Listar níveis disponíveis
    levels = subarea_data.get("levels", {})

    if not levels:
        print("\nEsta subárea não possui níveis configurados ainda.")
        input("\nPressione Enter para voltar...")
        return

    # Menu de exploração da subárea
    while True:
        print("\n=== Níveis Disponíveis ===")

        level_names = _get_level_order(levels)
        for i, level_name in enumerate(level_names, 1):
            level_data = levels[level_name]
            level_desc = level_data.get("description", "")[:60]
            print(f"{i}. {level_name.capitalize()} - {level_desc}")

        print("0. Voltar")

        choice = input("\nSua escolha: ").strip()
        if choice == "0":
            break

        if choice.isdigit() and 1 <= int(choice) <= len(level_names):
            selected_level = level_names[int(choice) - 1]

            # Explorar o nível selecionado
            explore_level(db, user_id, area_name, subarea_name, selected_level, levels[selected_level], user_age,
                          learning_style)
        else:
            print("Opção inválida.")


def explore_level(db, user_id, area_name, subarea_name, level_name, level_data, user_age, learning_style):
    """
    Permite ao usuário explorar um nível específico.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        area_name: Nome da área atual
        subarea_name: Nome da subárea
        level_name: Nome do nível selecionado
        level_data: Dados do nível
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    # Mostrar informações do nível
    print(f"\n=== Nível: {level_name.capitalize()} ===")

    description = level_data.get("description", "")
    if description:
        print(f"Descrição: {description}")

    # Mostrar objetivos de aprendizado
    learning_outcomes = level_data.get("learning_outcomes", [])
    if learning_outcomes:
        print("\nObjetivos de Aprendizado:")
        for i, outcome in enumerate(learning_outcomes, 1):
            print(f"{i}. {outcome}")

    # Listar módulos disponíveis
    modules = level_data.get("modules", [])

    # Menu de opções para o nível
    while True:
        if modules:
            print("\n=== Módulos Disponíveis ===")
            for i, module in enumerate(modules, 1):
                module_title = module.get("module_title", "Sem título")
                module_desc = module.get("module_description", "")[:60]
                print(f"{i}. {module_title}")
                if module_desc:
                    print(f"   {module_desc}")
        else:
            print("\nEste nível não possui módulos configurados ainda.")

        print("\n=== Opções ===")
        print("1. Explorar um módulo" if modules else "")
        print("2. Ver projeto final do nível" if level_data.get("final_project") else "")
        print("3. Fazer avaliação final do nível" if level_data.get("final_assessment") else "")
        print("4. Definir como nível atual")
        print("5. Gerar aula completa sobre este nível")
        print("6. Gerar roteiro de aprendizado para este nível")
        print("0. Voltar")

        choice = input("\nSua escolha: ").strip()

        if choice == "0":
            break
        elif choice == "1" and modules:
            module_idx = int(input("Qual módulo deseja explorar? (número): ").strip()) - 1
            if 0 <= module_idx < len(modules):
                explore_module(db, user_id, area_name, subarea_name, level_name, modules[module_idx], user_age,
                               learning_style)
            else:
                print("Módulo inválido.")
        elif choice == "2" and level_data.get("final_project"):
            show_final_project(level_data.get("final_project", {}), user_age, learning_style)
        elif choice == "3" and level_data.get("final_assessment"):
            take_final_assessment(db, user_id, area_name, subarea_name, level_name,
                                  level_data.get("final_assessment", {}), user_age, learning_style)
        elif choice == "4":
            # Definir como nível atual do usuário
            user_ref = db.collection("users").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                # Atualizar progresso
                progress = user_data.get("progress", {})
                current = progress.get("current", {})

                current["subarea"] = subarea_name
                current["level"] = level_name
                current["module_index"] = 0
                current["lesson_index"] = 0
                current["step_index"] = 0

                user_data["progress"]["current"] = current
                user_ref.set(user_data, merge=True)

                print(f"\nO nível atual foi definido como '{level_name.capitalize()}' na subárea '{subarea_name}'.")
                print("Você pode continuar seu aprendizado no modo linear.")
            else:
                print("\nErro: Dados do usuário não encontrados.")
        elif choice == "5":
            # Gerar aula completa
            topic = f"{subarea_name} - nível {level_name}"

            print(f"\nGerando aula completa sobre '{topic}'...")

            lesson = generate_complete_lesson(
                topic=topic,
                subject_area=area_name,
                age_range=user_age,
                knowledge_level=level_name,
                teaching_style=learning_style,
                lesson_duration_min=30
            )

            print("\n" + "=" * 80)
            print(lesson.to_text())
            print("=" * 80)

            input("\nPressione Enter para continuar...")
        elif choice == "6":
            # Gerar roteiro de aprendizado
            topic = f"{subarea_name} (nível {level_name})"

            print(f"\nGerando roteiro de aprendizado para '{topic}'...")

            pathway = generate_learning_pathway(
                topic=topic,
                duration_weeks=4,
                hours_per_week=3,
                initial_level=level_name,
                target_level="avançado"
            )

            print(f"\n=== ROTEIRO DE APRENDIZADO: {pathway['title']} ===\n")
            print(pathway['description'])

            # Exibir o resto do roteiro
            # ...

            input("\nPressione Enter para continuar...")
        else:
            print("Opção inválida.")


def explore_module(db, user_id, area_name, subarea_name, level_name, module_data, user_age, learning_style):
    """
    Permite ao usuário explorar um módulo específico.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        area_name: Nome da área atual
        subarea_name: Nome da subárea
        level_name: Nome do nível
        module_data: Dados do módulo
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    module_title = module_data.get("module_title", "Sem título")
    module_desc = module_data.get("module_description", "")

    print(f"\n=== Módulo: {module_title} ===")
    if module_desc:
        print(f"Descrição: {module_desc}")

    # Listar lições
    lessons = module_data.get("lessons", [])

    if not lessons:
        print("\nEste módulo não possui lições configuradas ainda.")

        # Gerar conteúdo para o módulo
        generate_content = input("\nDeseja gerar conteúdo para este módulo? (s/n): ").lower()
        if generate_content == 's':
            topic = f"{subarea_name} - {module_title}"

            print(f"\nGerando conteúdo para '{topic}'...")

            content = call_teacher_llm(
                f"Crie um conteúdo educacional completo sobre '{topic}' para um estudante de {user_age} anos. "
                f"Use linguagem acessível, exemplos práticos e relacione com o dia a dia. "
                f"O conteúdo deve incluir: introdução ao tema, conceitos principais, exemplos, "
                f"atividades práticas e desafios para fixação.",
                student_age=user_age,
                subject_area=area_name,
                teaching_style=learning_style,
                max_tokens=3000
            )

            print("\n" + "=" * 80)
            print(content)
            print("=" * 80)

        input("\nPressione Enter para voltar...")
        return

    # Menu de opções para o módulo
    while True:
        print("\n=== Lições Disponíveis ===")
        for i, lesson in enumerate(lessons, 1):
            lesson_title = lesson.get("lesson_title", "Sem título")
            lesson_obj = lesson.get("objectives", "")[:60]
            print(f"{i}. {lesson_title}")
            if lesson_obj:
                print(f"   Objetivos: {lesson_obj}")

        print("\n=== Opções ===")
        print("1. Ver uma lição")
        print("2. Ver projeto do módulo" if module_data.get("module_project") else "")
        print("3. Fazer avaliação do módulo" if module_data.get("module_assessment") else "")
        print("4. Definir como módulo atual")
        print("0. Voltar")

        choice = input("\nSua escolha: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            lesson_idx = int(input("Qual lição deseja ver? (número): ").strip()) - 1
            if 0 <= lesson_idx < len(lessons):
                view_lesson(db, user_id, area_name, subarea_name, level_name, module_title, lessons[lesson_idx],
                            user_age, learning_style)
            else:
                print("Lição inválida.")
        elif choice == "2" and module_data.get("module_project"):
            show_module_project(module_data.get("module_project", {}), user_age, learning_style)
        elif choice == "3" and module_data.get("module_assessment"):
            take_module_assessment(db, user_id, module_title, module_data.get("module_assessment", {}), user_age,
                                   learning_style)
        elif choice == "4":
            # Definir como módulo atual do usuário
            user_ref = db.collection("users").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                # Encontrar o índice do módulo
                modules_ref = db.collection("learning_paths").document(area_name).get().to_dict()
                subareas = modules_ref.get("subareas", {})

                if subarea_name in subareas:
                    subarea_data = subareas[subarea_name]
                    levels = subarea_data.get("levels", {})

                    if level_name in levels:
                        level_data = levels[level_name]
                        modules = level_data.get("modules", [])

                        module_index = -1
                        for i, module in enumerate(modules):
                            if module.get("module_title") == module_title:
                                module_index = i
                                break

                        if module_index >= 0:
                            # Atualizar progresso
                            progress = user_data.get("progress", {})
                            current = progress.get("current", {})

                            current["subarea"] = subarea_name
                            current["level"] = level_name
                            current["module_index"] = module_index
                            current["lesson_index"] = 0
                            current["step_index"] = 0

                            user_data["progress"]["current"] = current
                            user_ref.set(user_data, merge=True)

                            print(f"\nO módulo atual foi definido como '{module_title}'.")
                            print("Você pode continuar seu aprendizado no modo linear.")
                        else:
                            print("\nErro: Não foi possível encontrar o módulo na estrutura.")
                    else:
                        print("\nErro: Nível não encontrado.")
                else:
                    print("\nErro: Subárea não encontrada.")
            else:
                print("\nErro: Dados do usuário não encontrados.")
        else:
            print("Opção inválida.")


def view_lesson(db, user_id, area_name, subarea_name, level_name, module_title, lesson_data, user_age, learning_style):
    """
    Permite ao usuário visualizar uma lição específica.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        area_name: Nome da área atual
        subarea_name: Nome da subárea
        level_name: Nome do nível
        module_title: Título do módulo
        lesson_data: Dados da lição
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    lesson_title = lesson_data.get("lesson_title", "Sem título")
    objectives = lesson_data.get("objectives", "")

    print(f"\n=== Lição: {lesson_title} ===")
    if objectives:
        print(f"Objetivos: {objectives}")

    # Verificar se há passos definidos
    steps = lesson_data.get("steps", [])

    if not steps:
        print("\nEsta lição não possui passos definidos.")

        # Gerar conteúdo para a lição
        generate_content = input("\nDeseja gerar conteúdo para esta lição? (s/n): ").lower()
        if generate_content == 's':
            print(f"\nGerando conteúdo para a lição '{lesson_title}'...")

            content = call_teacher_llm(
                f"Crie um conteúdo educacional para a lição '{lesson_title}' com objetivos: {objectives}. "
                f"Este conteúdo é para um estudante de {user_age} anos estudando {area_name}, subárea {subarea_name}, "
                f"nível {level_name}, dentro do módulo '{module_title}'. "
                f"Use linguagem acessível, exemplos práticos, e estruture o conteúdo de forma clara.",
                student_age=user_age,
                subject_area=f"{area_name} - {subarea_name}",
                teaching_style=learning_style,
                knowledge_level=level_name,
                max_tokens=2500
            )

            print("\n" + "=" * 80)
            print(content)
            print("=" * 80)

        input("\nPressione Enter para voltar...")
        return

    # Mostrar os passos da lição
    for i, step in enumerate(steps, 1):
        print(f"\n--- Passo {i}/{len(steps)} ---")

        # Gerar conteúdo para o passo
        context = f"Área: {area_name}, Subárea: {subarea_name}, Nível: {level_name}, Módulo: {module_title}, Lição: {lesson_title}"

        prompt = (
            f"Explique de forma didática e adequada para um estudante de {user_age} anos: {step}. "
            f"Contexto da aula: {context}. "
            f"Use linguagem acessível e exemplos práticos. Relacione com o dia a dia quando possível."
        )

        explanation = call_teacher_llm(
            prompt,
            student_age=user_age,
            subject_area=area_name,
            teaching_style=learning_style,
            knowledge_level=level_name
        )

        print(explanation)

        if i < len(steps):
            input("\nPressione Enter para o próximo passo...")

    # Verificar se há exercícios
    exercises = lesson_data.get("exercises", [])
    if exercises:
        do_exercises = input("\nDeseja fazer os exercícios desta lição? (s/n): ").lower()
        if do_exercises == 's':
            for i, exercise in enumerate(exercises, 1):
                question = exercise.get("question", "")
                print(f"\nExercício {i}: {question}")

                # Processar o exercício conforme seu tipo
                # ...

    # Verificar se há projeto da lição
    project = lesson_data.get("project", {})
    if project:
        show_project = input("\nDeseja ver o projeto desta lição? (s/n): ").lower()
        if show_project == 's':
            show_lesson_project(project, user_age, learning_style)

    input("\nPressione Enter para voltar...")


def show_final_project(project_data, user_age, learning_style):
    """
    Exibe informações sobre o projeto final e permite ao usuário explorá-lo.

    Args:
        project_data: Dados do projeto final
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    project_title = project_data.get("title", "Projeto Final")
    project_desc = project_data.get("description", "")
    requirements = project_data.get("requirements", [])

    print(f"\n=== Projeto Final: {project_title} ===")
    print(f"Descrição: {project_desc}")

    if requirements:
        print("\nRequisitos do projeto:")
        for i, req in enumerate(requirements, 1):
            print(f"{i}. {req}")

    # Oferecer orientações detalhadas para o projeto
    generate_guidance = input("\nDeseja ver orientações detalhadas para este projeto? (s/n): ").lower()
    if generate_guidance == 's':
        req_text = ", ".join(requirements) if requirements else ""

        prompt = (
            f"O aluno de {user_age} anos precisa realizar o projeto final: '{project_title}'. "
            f"Descrição: {project_desc}. "
            f"Requisitos: {req_text}. "
            f"Forneça um guia passo a passo detalhado sobre como realizar este projeto, "
            f"usando linguagem adequada para a idade do aluno. Inclua: "
            f"1) Planejamento inicial; "
            f"2) Pesquisa e preparação; "
            f"3) Desenvolvimento do projeto; "
            f"4) Finalização e apresentação."
        )

        guidance = call_teacher_llm(
            prompt,
            student_age=user_age,
            teaching_style=learning_style,
            max_tokens=2500
        )

        print("\n" + "=" * 80)
        print(guidance)
        print("=" * 80)

    input("\nPressione Enter para voltar...")


def show_module_project(project_data, user_age, learning_style):
    """
    Exibe informações sobre o projeto do módulo e permite ao usuário explorá-lo.

    Args:
        project_data: Dados do projeto do módulo
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    project_title = project_data.get("title", "Projeto do Módulo")
    project_desc = project_data.get("description", "")
    deliverables = project_data.get("deliverables", [])

    print(f"\n=== Projeto do Módulo: {project_title} ===")
    print(f"Descrição: {project_desc}")

    if deliverables:
        print("\nEntregas esperadas:")
        for i, deliv in enumerate(deliverables, 1):
            print(f"{i}. {deliv}")

    # Oferecer orientações detalhadas para o projeto
    generate_guidance = input("\nDeseja ver orientações detalhadas para este projeto? (s/n): ").lower()
    if generate_guidance == 's':
        deliv_text = ", ".join(deliverables) if deliverables else ""

        prompt = (
            f"O aluno de {user_age} anos precisa realizar o projeto: '{project_title}'. "
            f"Descrição: {project_desc}. "
            f"Entregas esperadas: {deliv_text}. "
            f"Forneça um guia passo a passo sobre como desenvolver este projeto, "
            f"usando linguagem adequada para a idade do aluno."
        )

        guidance = call_teacher_llm(
            prompt,
            student_age=user_age,
            teaching_style=learning_style,
            max_tokens=2000
        )

        print("\n" + "=" * 80)
        print(guidance)
        print("=" * 80)

    input("\nPressione Enter para voltar...")


def show_lesson_project(project_data, user_age, learning_style):
    """
    Exibe informações sobre o projeto da lição e permite ao usuário explorá-lo.

    Args:
        project_data: Dados do projeto da lição
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    project_title = project_data.get("title", "Projeto da Aula")
    project_desc = project_data.get("description", "")

    print(f"\n=== Projeto da Aula: {project_title} ===")
    print(f"Descrição: {project_desc}")

    # Oferecer orientações detalhadas para o projeto
    generate_guidance = input("\nDeseja ver orientações detalhadas para este projeto? (s/n): ").lower()
    if generate_guidance == 's':
        prompt = (
            f"O aluno de {user_age} anos precisa realizar o projeto: '{project_title}'. "
            f"Descrição: {project_desc}. "
            f"Forneça instruções passo a passo sobre como realizar este projeto, "
            f"usando linguagem adequada para a idade do aluno."
        )

        guidance = call_teacher_llm(
            prompt,
            student_age=user_age,
            teaching_style=learning_style,
            max_tokens=1500
        )

        print("\n" + "=" * 80)
        print(guidance)
        print("=" * 80)

    input("\nPressione Enter para voltar...")


def take_module_assessment(db, user_id, module_title, assessment_data, user_age, learning_style):
    """
    Permite ao usuário realizar a avaliação de um módulo.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        module_title: Título do módulo
        assessment_data: Dados da avaliação
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    assessment_title = assessment_data.get("title", "Avaliação do Módulo")
    passing_score = assessment_data.get("passing_score", 70)

    print(f"\n=== Avaliação do Módulo: {assessment_title} ===")
    print(f"Nota para aprovação: {passing_score}%")

    proceed = input("\nDeseja realizar esta avaliação agora? (s/n): ").lower()
    if proceed != 's':
        return

    # Verificar se há questões pré-definidas
    questions = assessment_data.get("questions", [])

    if not questions:
        # Gerar avaliação dinâmica
        assessment = generate_assessment(
            topic=f"{module_title} - {assessment_title}",
            difficulty="médio",
            num_questions=3,
            question_types=["múltipla escolha", "verdadeiro/falso"]
        )

        questions = assessment.get("questions", [])

    if not questions:
        print("\nNão foi possível gerar questões para a avaliação.")
        return

    score = _apply_assessment({"title": assessment_title, "questions": questions}, user_age, learning_style)

    if score >= passing_score:
        print(f"\nParabéns! Você passou na avaliação com {score}%!")

        # Registrar aprovação
        _register_assessment_passed(db, user_id, module_title, score)
    else:
        print(f"\nVocê obteve {score}%, abaixo da nota de aprovação de {passing_score}%.")
        print("Revise o conteúdo do módulo antes de tentar novamente.")

    input("\nPressione Enter para voltar...")


def take_final_assessment(db, user_id, area_name, subarea_name, level_name, assessment_data, user_age, learning_style):
    """
    Permite ao usuário realizar a avaliação final de um nível.

    Args:
        db: Conexão com o Firestore
        user_id: ID do usuário
        area_name: Nome da área
        subarea_name: Nome da subárea
        level_name: Nome do nível
        assessment_data: Dados da avaliação
        user_age: Idade do usuário
        learning_style: Estilo de ensino preferido
    """
    assessment_title = assessment_data.get("title", "Avaliação Final")
    passing_criteria = assessment_data.get("passing_criteria", "")

    print(f"\n=== Avaliação Final: {assessment_title} ===")
    if passing_criteria:
        print(f"Critérios de aprovação: {passing_criteria}")

    proceed = input("\nDeseja realizar esta avaliação final agora? (s/n): ").lower()
    if proceed != 's':
        return

    # Gerar avaliação abrangente para o nível
    assessment = generate_assessment(
        topic=f"{subarea_name} - nível {level_name}",
        difficulty=level_name,
        num_questions=5,
        question_types=["múltipla escolha", "verdadeiro/falso", "dissertativa"]
    )

    score = _apply_assessment(assessment, user_age, learning_style)

    # Verificar se passou
    passing_score = 70  # Valor padrão
    if passing_criteria and "mínimo" in passing_criteria.lower() and "%" in passing_criteria:
        try:
            # Tentar extrair o valor numérico do critério de aprovação
            passing_score = int(''.join(filter(str.isdigit, passing_criteria)))
        except:
            pass

    if score >= passing_score:
        print(f"\nParabéns! Você passou na avaliação final com {score}%!")

        # Registrar aprovação
        _register_final_assessment_passed(db, user_id, level_name, score)

        # Emitir certificação, se disponível
        certification = assessment_data.get("certification", "")
        if certification:
            _award_certification(db, user_id, certification)
    else:
        print(f"\nVocê obteve {score}%, abaixo da nota de aprovação.")
        print("Revise o conteúdo do nível e tente novamente quando estiver preparado.")

    input("\nPressione Enter para voltar...")