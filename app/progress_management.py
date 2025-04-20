# progress_management.py (refatorado)

from app.llm_integration import (
    call_teacher_llm,
    generate_complete_lesson,
    generate_assessment,
    LessonContent,
    TEACHING_STYLES,
    generate_learning_pathway
)
import time
from functools import wraps
from typing import Dict, List, Any, Optional, Union, Callable
from google.cloud.firestore import ArrayUnion
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constantes para níveis comuns
LEVEL_ORDER = ["iniciante", "básico", "basico", "intermediário", "intermediario", "avançado", "avancado"]


# Classes para representar estruturas de dados
class UserProgress:
    """Classe para encapsular o progresso do usuário."""

    def __init__(self, data: Dict = None):
        data = data or {}
        self.area = data.get("area", "")
        self.subarea = data.get("current", {}).get("subarea", "")
        self.level = data.get("current", {}).get("level", "iniciante")
        self.module_index = data.get("current", {}).get("module_index", 0)
        self.lesson_index = data.get("current", {}).get("lesson_index", 0)
        self.step_index = data.get("current", {}).get("step_index", 0)
        self.subareas_order = data.get("subareas_order", [])

    def to_dict(self) -> Dict:
        """Converte para dicionário para armazenamento no Firestore."""
        return {
            "area": self.area,
            "subareas_order": self.subareas_order,
            "current": {
                "subarea": self.subarea,
                "level": self.level,
                "module_index": self.module_index,
                "lesson_index": self.lesson_index,
                "step_index": self.step_index
            }
        }

    def advance_step(self):
        """Avança para o próximo passo."""
        self.step_index += 1

    def advance_lesson(self):
        """Avança para a próxima lição e reseta o índice de passos."""
        self.lesson_index += 1
        self.step_index = 0

    def advance_module(self):
        """Avança para o próximo módulo e reseta índices de lição e passos."""
        self.module_index += 1
        self.lesson_index = 0
        self.step_index = 0

    def advance_level(self, next_level: str):
        """Avança para o próximo nível e reseta todos os índices."""
        self.level = next_level
        self.module_index = 0
        self.lesson_index = 0
        self.step_index = 0


# Utilitários e decoradores
def db_operation(func):
    """Decorador para operações de banco de dados, com tratamento de erros."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Erro na operação de banco de dados {func.__name__}: {e}")
            print(f"Ocorreu um erro ao acessar o banco de dados: {e}")
            return None

    return wrapper


def llm_operation(func):
    """Decorador para operações com LLM, com tratamento de erros."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Erro na operação com LLM {func.__name__}: {e}")
            print(f"Ocorreu um erro ao gerar conteúdo: {e}")
            return None

    return wrapper


# Funções utilitárias
def get_level_order(levels: Dict) -> List[str]:
    """
    Retorna uma lista ordenada dos níveis (iniciante -> intermediário -> avançado).
    Normaliza as variações ortográficas.
    """
    level_names = list(levels.keys())
    normalized_names = {normalize_level_name(name): name for name in level_names}

    # Primeiro incluir os níveis na ordem preferida
    ordered_levels = []
    for level in LEVEL_ORDER:
        normalized = normalize_level_name(level)
        if normalized in normalized_names:
            ordered_levels.append(normalized_names[normalized])

    # Depois incluir outros níveis não presentes na ordem preferida
    for level in level_names:
        if level not in ordered_levels:
            ordered_levels.append(level)

    return ordered_levels


def normalize_level_name(level_name: str) -> str:
    """Normaliza nomes de níveis para evitar problemas com acentuação."""
    mapping = {
        "básico": "basico",
        "intermediário": "intermediario",
        "avançado": "avancado"
    }
    return mapping.get(level_name.lower(), level_name.lower())


# Funções de registro de progresso
@db_operation
def register_project_started(db, user_id: str, project_title: str, project_type: str):
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
    user_ref.update({
        "started_projects": ArrayUnion([project_data])
    })

    return True


@db_operation
def register_project_completed(db, user_id: str, project_title: str, project_type: str):
    """
    Registra a conclusão de um projeto no perfil do usuário.
    """
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        logger.error(f"Dados do usuário {user_id} não encontrados")
        print("Erro: dados do usuário não encontrados.")
        return False

    user_data = user_doc.to_dict()
    started_projects = user_data.get("started_projects", [])

    # Encontrar o projeto na lista de iniciados
    project_found = False
    updated_projects = []

    for project in started_projects:
        if project["title"] == project_title and project["type"] == project_type:
            project_found = True
            # Marcar como concluído
            updated_project = project.copy()
            updated_project["status"] = "completed"
            updated_projects.append(updated_project)
        else:
            updated_projects.append(project)

    if not project_found:
        # Se o projeto não foi encontrado na lista de iniciados, criá-lo agora
        project_data = {
            "title": project_title,
            "type": project_type,
            "start_date": time.strftime("%Y-%m-%d"),
            "status": "completed"
        }
        updated_projects.append(project_data)

    # Estrutura do projeto concluído
    completion_date = time.strftime("%Y-%m-%d")
    start_date = next(
        (p["start_date"] for p in updated_projects if p["title"] == project_title and p["type"] == project_type),
        completion_date)

    completed_project = {
        "title": project_title,
        "type": project_type,
        "start_date": start_date,
        "completion_date": completion_date
    }

    # Atualizar o perfil do usuário com operações atômicas
    user_ref.update({
        "started_projects": updated_projects,
        "completed_projects": ArrayUnion([completed_project])
    })

    return True


@db_operation
def register_completion(db, user_id: str, collection_name: str, item_data: Dict):
    """
    Registra a conclusão de um item (lição, módulo, avaliação) no perfil do usuário.

    Args:
        db: Referência do Firestore
        user_id: ID do usuário
        collection_name: Nome da coleção (ex: "completed_lessons")
        item_data: Dados a serem registrados
    """
    user_ref = db.collection("users").document(user_id)

    # Adicionar data de conclusão se não estiver presente
    if "completion_date" not in item_data:
        item_data["completion_date"] = time.strftime("%Y-%m-%d")

    # Adicionar à lista apropriada
    user_ref.update({
        collection_name: ArrayUnion([item_data])
    })

    return True


def register_lesson_completion(db, user_id: str, lesson_title: str):
    """Registra a conclusão de uma lição."""
    return register_completion(db, user_id, "completed_lessons", {
        "title": lesson_title,
        "completion_date": time.strftime("%Y-%m-%d")
    })


def register_module_completion(db, user_id: str, module_title: str):
    """Registra a conclusão de um módulo."""
    return register_completion(db, user_id, "completed_modules", {
        "title": module_title,
        "completion_date": time.strftime("%Y-%m-%d")
    })


def register_level_completion(db, user_id: str, area_name: str, subarea_name: str, level_name: str):
    """Registra a conclusão de um nível."""
    return register_completion(db, user_id, "completed_levels", {
        "area": area_name,
        "subarea": subarea_name,
        "level": level_name,
        "completion_date": time.strftime("%Y-%m-%d")
    })


def register_assessment_passed(db, user_id: str, module_title: str, score: float):
    """Registra a aprovação em uma avaliação de módulo."""
    return register_completion(db, user_id, "passed_assessments", {
        "module": module_title,
        "score": score,
        "date": time.strftime("%Y-%m-%d")
    })


def register_final_assessment_passed(db, user_id: str, level_name: str, score: float):
    """Registra a aprovação em uma avaliação final de nível."""
    return register_completion(db, user_id, "passed_final_assessments", {
        "level": level_name,
        "score": score,
        "date": time.strftime("%Y-%m-%d")
    })


def award_certification(db, user_id: str, certification_title: str):
    """Emite uma certificação para o usuário."""
    result = register_completion(db, user_id, "certifications", {
        "title": certification_title,
        "date": time.strftime("%Y-%m-%d"),
        "id": f"CERT-{int(time.time())}"
    })

    if result:
        print(f"\n🎓 Parabéns! Você obteve a certificação: {certification_title}")

    return result


# Funções de verificação e interação
def check_level_requirements(db, user_id: str, current: Dict, level_data: Dict) -> bool:
    """
    Verifica se o usuário atende aos requisitos para o nível atual.
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


@llm_operation
def apply_assessment(assessment_data: Dict, user_age: int, teaching_style: str) -> float:
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
                f"e forneça feedback construtivo. Conclua com uma recomendação clara: APROVADO ou REPROVADO."
            )

            evaluation = call_teacher_llm(
                prompt,
                student_age=user_age,
                teaching_style=teaching_style,
                max_tokens=1000
            )

            print("\nAvaliação:")
            print(evaluation)

            # Verificar se o LLM indicou aprovação
            is_approved = "APROVADO" in evaluation.upper()
            if is_approved:
                print("\nSua resposta foi considerada satisfatória!")
                correct_answers += 1
            else:
                proceed = input("\nVocê acredita que sua resposta está correta? (s/n): ").lower() == 's'
                if proceed:
                    print("\nResposta considerada válida após reavaliação.")
                    correct_answers += 1

    score = (correct_answers / total_questions) * 100
    return score


def check_for_activities(db, user_id: str, activities_type: str, data: Dict, user_age: int,
                         teaching_style: str) -> bool:
    """
    Função unificada para verificar e oferecer atividades (projetos e avaliações).

    Args:
        activities_type: 'final', 'module' ou 'lesson'

    Returns:
        True se as atividades foram concluídas, False caso contrário
    """
    # Definir os nomes das chaves conforme o tipo de atividade
    if activities_type == "final":
        project_key = "final_project"
        assessment_key = "final_assessment"
        register_assessment_func = register_final_assessment_passed
    elif activities_type == "module":
        project_key = "module_project"
        assessment_key = "module_assessment"
        register_assessment_func = register_assessment_passed
    else:  # lesson
        project_key = "project"
        assessment_key = "exercises"
        register_assessment_func = None  # Lições não têm avaliação formal

    # Verificar projeto
    project_data = data.get(project_key, {})
    if project_data:
        return show_project(db, user_id, project_data, activities_type, user_age, teaching_style)

    # Verificar avaliação
    assessment_data = data.get(assessment_key, {})
    if assessment_data and register_assessment_func:
        return take_assessment(db, user_id, assessment_data, activities_type,
                               user_age, teaching_style, register_assessment_func)

    # Se não houver atividades específicas
    return True


def show_project(db, user_id: str, project_data: Dict, project_type: str, user_age: int, teaching_style: str) -> bool:
    """
    Função unificada para mostrar e gerenciar projetos.

    Args:
        project_type: 'final', 'module' ou 'lesson'

    Returns:
        True se o projeto foi concluído, False caso contrário
    """
    project_title = project_data.get("title", f"Projeto {project_type.capitalize()}")
    project_desc = project_data.get("description", "")

    print(f"\n=== Projeto {project_type.capitalize()}: {project_title} ===")
    print(f"Descrição: {project_desc}")

    # Mostrar requisitos ou entregas esperadas, se houver
    if "requirements" in project_data:
        print("\nRequisitos do projeto:")
        for i, req in enumerate(project_data["requirements"], 1):
            print(f"{i}. {req}")
    elif "deliverables" in project_data:
        print("\nEntregas esperadas:")
        for i, deliv in enumerate(project_data["deliverables"], 1):
            print(f"{i}. {deliv}")

    do_project = input(f"\nDeseja {project_data.get('action_text', 'iniciar este projeto')} agora? (s/n): ").lower()
    if do_project != 's':
        return False

    # Gerar orientações para o projeto
    requirements = project_data.get("requirements", [])
    deliverables = project_data.get("deliverables", [])

    req_text = ", ".join(requirements) if requirements else ""
    deliv_text = ", ".join(deliverables) if deliverables else ""

    prompt = (
        f"O aluno de {user_age} anos precisa realizar o projeto: '{project_title}'. "
        f"Descrição: {project_desc}. "
    )

    if req_text:
        prompt += f"Requisitos: {req_text}. "
    if deliv_text:
        prompt += f"Entregas esperadas: {deliv_text}. "

    prompt += (
        f"Forneça um guia passo a passo detalhado sobre como realizar este projeto, "
        f"usando linguagem adequada para a idade do aluno, incluindo: "
        f"1) Planejamento inicial; "
        f"2) Pesquisa e preparação; "
        f"3) Desenvolvimento do projeto; "
        f"4) Finalização e apresentação."
    )

    guidance = call_teacher_llm(
        prompt,
        student_age=user_age,
        teaching_style=teaching_style,
        max_tokens=2500
    )

    print("\n" + "=" * 80)
    print(guidance)
    print("=" * 80)

    # Registrar o projeto como iniciado
    register_project_started(db, user_id, project_title, project_type)

    completed = input("\nVocê completou o projeto? (s/n): ").lower()
    if completed == 's':
        register_project_completed(db, user_id, project_title, project_type)
        return True

    return False


def take_assessment(db, user_id: str, assessment_data: Dict, assessment_type: str,
                    user_age: int, teaching_style: str, register_func: Callable) -> bool:
    """
    Função unificada para aplicar avaliações.

    Args:
        assessment_type: 'final' ou 'module'
        register_func: Função para registrar a aprovação

    Returns:
        True se a avaliação foi aprovada, False caso contrário
    """
    assessment_title = assessment_data.get("title", f"Avaliação {assessment_type.capitalize()}")

    # Determinar pontuação de aprovação
    passing_score = 70
    if "passing_score" in assessment_data:
        passing_score = assessment_data["passing_score"]
    elif "passing_criteria" in assessment_data:
        criteria = assessment_data["passing_criteria"]
        if isinstance(criteria, str) and "%" in criteria:
            try:
                # Tentar extrair o valor numérico do critério de aprovação
                passing_score = int(''.join(filter(str.isdigit, criteria)))
            except:
                pass

    print(f"\n=== Avaliação {assessment_type.capitalize()}: {assessment_title} ===")
    print(f"Nota para aprovação: {passing_score}%")

    do_assessment = input("\nDeseja fazer esta avaliação agora? (s/n): ").lower()
    if do_assessment != 's':
        return False

    # Verificar se há questões pré-definidas ou gerar
    questions = assessment_data.get("questions", [])

    if not questions:
        # Gerar avaliação dinâmica
        topic = assessment_data.get("topic", assessment_title)
        difficulty = assessment_data.get("difficulty", "médio")

        assessment = generate_assessment(
            topic=topic,
            difficulty=difficulty,
            num_questions=assessment_data.get("num_questions", 5),
            question_types=["múltipla escolha", "verdadeiro/falso", "dissertativa"]
        )
        questions = assessment.get("questions", [])

    if not questions:
        print("\nNão foi possível gerar questões para a avaliação.")
        return False

    # Aplicar a avaliação
    score = apply_assessment({"title": assessment_title, "questions": questions}, user_age, teaching_style)

    # Verificar aprovação
    if score >= passing_score:
        print(f"\nParabéns! Você passou na avaliação com {score}%!")

        # Registrar aprovação usando a função apropriada
        if assessment_type == "final":
            level_name = assessment_data.get("level", "")
            register_func(db, user_id, level_name, score)

            # Emitir certificação, se disponível
            certification = assessment_data.get("certification", "")
            if certification:
                award_certification(db, user_id, certification)
        else:
            module_title = assessment_data.get("module", "")
            register_func(db, user_id, module_title, score)

        return True
    else:
        print(f"\nVocê obteve {score}%, abaixo da nota de aprovação de {passing_score}%.")
        print("Revise o conteúdo antes de tentar novamente.")
        return False


def generate_lesson_content(lesson_title: str, objectives: str, user_age: int,
                            area_name: str, subarea_name: str, teaching_style: str):
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


def generate_module_content(module_title: str, module_desc: str, user_age: int,
                            area_name: str, subarea_name: str, teaching_style: str):
    """
    Gera conteúdo para um módulo que não tem lições definidas.
    """
    print(f"\nGerando conteúdo para o módulo: {module_title}")

    prompt = (
        f"Crie um conteúdo educacional completo para o módulo '{module_title}' "
        f"com descrição: {module_desc}. "
        f"Este conteúdo é para um estudante de {user_age} anos estudando {area_name}, "
        f"subárea {subarea_name}. "
        f"O conteúdo deve incluir: introdução ao tema, conceitos principais, exemplos práticos, "
        f"atividades sugeridas e resumo dos pontos principais. "
        f"Use linguagem adequada para a idade do aluno."
    )

    content = call_teacher_llm(
        prompt,
        student_age=user_age,
        subject_area=f"{area_name} - {subarea_name}",
        teaching_style=teaching_style,
        max_tokens=3000
    )

    print("\n" + "=" * 80)
    print(content)
    print("=" * 80)


def ask_teacher_question(user_age: int, area_name: str, subarea_name: str,
                         level_name: str, teaching_style: str):
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


# Funções principais do módulo
def print_current_status(area_name: str, subarea_name: str, level_name: str,
                         current: Dict, subarea_data: Dict, level_data: Dict):
    """
    Exibe o status atual de progresso do usuário.
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


def continue_next_step(db, user_id: str, user_data: Dict, area_name: str, subarea_name: str,
                       level_name: str, current: Dict, subarea_data: Dict, level_data: Dict,
                       user_age: int, teaching_style: str):
    """
    Avança para o próximo passo na sequência de aprendizado.
    Versão refatorada para melhor modularidade e manutenibilidade.
    """
    module_index = current.get("module_index", 0)
    lesson_index = current.get("lesson_index", 0)
    step_index = current.get("step_index", 0)

    # Criar objeto de progresso para facilitar manipulação
    progress = UserProgress(user_data.get("progress", {}))

    # ETAPA 1: Verificar módulos disponíveis
    modules = level_data.get("modules", [])

    if not modules:
        print("\nEste nível não possui módulos configurados ainda.")

        # Verificar atividades finais e possivelmente avançar de nível
        if check_for_activities(db, user_id, "final", level_data, user_age, teaching_style):
            register_level_completion(db, user_id, area_name, subarea_name, level_name)
            advance_to_next_level(db, user_id, user_data, subarea_data, level_name)
        return

    # ETAPA 2: Verificar se todos os módulos foram concluídos
    if module_index >= len(modules):
        print("\nVocê já concluiu todos os módulos deste nível!")

        # Verificar atividades finais e possivelmente avançar de nível
        if check_for_activities(db, user_id, "final", level_data, user_age, teaching_style):
            register_level_completion(db, user_id, area_name, subarea_name, level_name)
            advance_to_next_level(db, user_id, user_data, subarea_data, level_name)
        return

    # ETAPA 3: Processar o módulo atual
    module_data = modules[module_index]
    module_title = module_data.get("module_title", "Sem título")
    process_current_module(db, user_id, user_data, area_name, subarea_name, level_name,
                           module_data, module_title, lesson_index, step_index, user_age, teaching_style)


def advance_to_next_level(db, user_id: str, user_data: Dict, subarea_data: Dict, current_level: str):
    """
    Tenta avançar o usuário para o próximo nível se possível.
    """
    # Obter a ordem dos níveis
    levels = subarea_data.get("levels", {})
    level_order = get_level_order(levels)

    # Verificar se há próximo nível
    current_idx = level_order.index(current_level) if current_level in level_order else -1
    if current_idx >= 0 and current_idx < len(level_order) - 1:
        next_level = level_order[current_idx + 1]

        # Atualizar progresso
        progress = UserProgress(user_data.get("progress", {}))
        progress.advance_level(next_level)

        # Salvar no banco de dados
        user_data["progress"] = progress.to_dict()
        db.collection("users").document(user_id).set(user_data, merge=True)

        print(f"\nParabéns! Você avançou para o nível {next_level.capitalize()}!")
        return True

    print("\nVocê concluiu o nível mais avançado desta subárea!")
    return False


def process_current_module(db, user_id: str, user_data: Dict, area_name: str, subarea_name: str,
                           level_name: str, module_data: Dict, module_title: str,
                           lesson_index: int, step_index: int, user_age: int, teaching_style: str):
    """
    Processa o módulo atual, verificando lições e avanços.
    """
    lessons = module_data.get("lessons", [])

    # Verificar se o módulo tem lições
    if not lessons:
        print(f"\nO módulo '{module_title}' não possui lições configuradas ainda.")

        # Gerar conteúdo e verificar atividades
        generate_module_content(module_title, module_data.get("module_description", ""),
                                user_age, area_name, subarea_name, teaching_style)

        if check_for_activities(db, user_id, "module", module_data, user_age, teaching_style):
            register_module_completion(db, user_id, module_title)
            advance_to_next_module(db, user_id, user_data)
        return

    # Verificar se todas as lições foram concluídas
    if lesson_index >= len(lessons):
        print(f"\nVocê já concluiu todas as lições do módulo '{module_title}'!")

        if check_for_activities(db, user_id, "module", module_data, user_age, teaching_style):
            register_module_completion(db, user_id, module_title)
            advance_to_next_module(db, user_id, user_data)
        return

    # Processar a lição atual
    lesson_data = lessons[lesson_index]
    lesson_title = lesson_data.get("lesson_title", "Sem título")
    process_current_lesson(db, user_id, user_data, area_name, subarea_name, level_name,
                           module_title, lesson_data, lesson_title, step_index, user_age, teaching_style)


def advance_to_next_module(db, user_id: str, user_data: Dict):
    """
    Avança para o próximo módulo, atualizando o progresso do usuário.
    """
    # Atualizar progresso
    progress = UserProgress(user_data.get("progress", {}))
    progress.advance_module()

    # Salvar no banco de dados
    user_data["progress"] = progress.to_dict()
    db.collection("users").document(user_id).set(user_data, merge=True)

    print("\nMódulo concluído! Avançando para o próximo módulo.")


def process_current_lesson(db, user_id: str, user_data: Dict, area_name: str, subarea_name: str,
                           level_name: str, module_title: str, lesson_data: Dict,
                           lesson_title: str, step_index: int, user_age: int, teaching_style: str):
    """
    Processa a lição atual, verificando passos e avanços.
    """
    steps = lesson_data.get("steps", [])

    # Verificar se a lição tem passos definidos
    if not steps:
        print(f"\nA lição '{lesson_title}' não possui passos definidos.")

        # Gerar conteúdo para a lição
        generate_lesson_content(lesson_title, lesson_data.get("objectives", ""),
                                user_age, area_name, subarea_name, teaching_style)

        # Verificar atividades da lição
        if check_for_activities(db, user_id, "lesson", lesson_data, user_age, teaching_style):
            register_lesson_completion(db, user_id, lesson_title)
            advance_to_next_lesson(db, user_id, user_data)
        return

    # Verificar se todos os passos foram concluídos
    if step_index >= len(steps):
        print(f"\nVocê já concluiu todos os passos da lição '{lesson_title}'!")

        if check_for_activities(db, user_id, "lesson", lesson_data, user_age, teaching_style):
            register_lesson_completion(db, user_id, lesson_title)
            advance_to_next_lesson(db, user_id, user_data)
        return

    # Apresentar o passo atual
    present_current_step(db, user_id, user_data, area_name, subarea_name, level_name,
                         module_title, lesson_title, lesson_data, steps, step_index, user_age, teaching_style)


def advance_to_next_lesson(db, user_id: str, user_data: Dict):
    """
    Avança para a próxima lição, atualizando o progresso do usuário.
    """
    # Atualizar progresso
    progress = UserProgress(user_data.get("progress", {}))
    progress.advance_lesson()

    # Salvar no banco de dados
    user_data["progress"] = progress.to_dict()
    db.collection("users").document(user_id).set(user_data, merge=True)

    print("\nLição concluída! Avançando para a próxima lição.")


def present_current_step(db, user_id: str, user_data: Dict, area_name: str, subarea_name: str,
                         level_name: str, module_title: str, lesson_title: str, lesson_data: Dict,
                         steps: List, step_index: int, user_age: int, teaching_style: str):
    """
    Apresenta o passo atual da lição ao usuário.
    """
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
        teaching_style=teaching_style
    )

    print(explanation)

    # Avançar para o próximo passo
    progress = UserProgress(user_data.get("progress", {}))
    progress.advance_step()

    # Salvar no banco de dados
    user_data["progress"] = progress.to_dict()
    db.collection("users").document(user_id).set(user_data, merge=True)

    print(f"\n[Progresso] Passo {step_index + 1}/{len(steps)} concluído na aula '{lesson_title}'.")
    print("Use [1] para continuar ou escolha outra opção.")


def change_level(db, user_id: str, user_data: Dict, subarea_data: Dict) -> bool:
    """
    Permite ao usuário mudar para outro nível dentro da mesma subárea.
    Versão refatorada para maior clareza.
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
    progress = UserProgress(user_data.get("progress", {}))
    progress.level = selected_level
    progress.module_index = 0
    progress.lesson_index = 0
    progress.step_index = 0

    # Atualizar no Firestore
    user_data["progress"] = progress.to_dict()
    db.collection("users").document(user_id).set(user_data, merge=True)

    print(f"\nNível alterado para '{selected_level.capitalize()}'.")
    return True


def change_subarea(db, user_id: str, user_data: Dict, area_data: Dict) -> bool:
    """
    Permite ao usuário mudar para outra subárea dentro da mesma área.
    Versão refatorada para maior clareza.
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
    progress = UserProgress(user_data.get("progress", {}))
    progress.subarea = selected_subarea
    progress.level = "iniciante"  # Volta para o nível iniciante por padrão
    progress.module_index = 0
    progress.lesson_index = 0
    progress.step_index = 0

    # Atualizar no Firestore
    user_data["progress"] = progress.to_dict()
    db.collection("users").document(user_id).set(user_data, merge=True)

    print(f"\nSubárea alterada para '{selected_subarea}'.")
    return True


def change_teaching_style(db, user_id: str) -> str:
    """
    Permite ao usuário alterar o estilo de ensino.
    Versão refatorada para maior clareza.
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


# Funções para o fluxo principal de progresso
def continue_progress_flow(db, user_id: str):
    """
    Gerencia o fluxo de progresso linear (estilo "video-game") para o usuário.
    Versão refatorada para melhor estrutura e manutenibilidade.
    """
    # Obter dados do usuário
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

    # Inicializar progresso se necessário
    current = progress.get("current", {})
    if not current:
        current = initialize_user_progress(db, user_id, user_data, area_data)
        if not current:
            return

    # Obter subárea atual
    subarea_name = current.get("subarea", "")
    if not subarea_name:
        subarea_name = select_subarea(db, user_id, user_data, area_data)
        if not subarea_name:
            return

    # Obter dados da subárea
    subareas = area_data.get("subareas", {})
    if subarea_name not in subareas:
        print(f"Subárea '{subarea_name}' não encontrada na área '{area_name}'.")
        return

    subarea_data = subareas[subarea_name]

    # Obter nível atual
    level_name = current.get("level", "iniciante")
    levels = subarea_data.get("levels", {})

    if level_name not in levels:
        level_name = select_level(db, user_id, user_data, subarea_data)
        if not level_name:
            return

    level_data = levels[level_name]

    # Obter dados de personalização
    user_age = user_data.get("age", 14)
    learning_style = user_data.get("learning_style", "didático")

    # Assegurar que temos um estilo de ensino válido
    if learning_style not in TEACHING_STYLES:
        learning_style = "didático"

    # Iniciar loop principal
    main_progress_loop(db, user_id, user_data, area_name, area_data, subarea_name,
                       subarea_data, level_name, level_data, current, user_age, learning_style)


def initialize_user_progress(db, user_id: str, user_data: Dict, area_data: Dict) -> Dict:
    """
    Inicializa o progresso do usuário se não existir.
    """
    # Selecionar uma subárea padrão
    subarea_name = ""
    subareas = area_data.get("subareas", {})

    if subareas:
        subarea_name = next(iter(subareas.keys()), "")

    # Criar estrutura de progresso
    current = {
        "subarea": subarea_name,
        "level": "iniciante",
        "module_index": 0,
        "lesson_index": 0,
        "step_index": 0
    }

    # Atualizar dados do usuário
    user_data["progress"] = {
        "area": user_data["progress"].get("area", ""),
        "subareas_order": list(subareas.keys()) if subareas else [],
        "current": current
    }

    # Salvar no banco de dados
    db.collection("users").document(user_id).set(user_data, merge=True)

    return current


def select_subarea(db, user_id: str, user_data: Dict, area_data: Dict) -> str:
    """
    Permite ao usuário selecionar uma subárea disponível.
    """
    print("Nenhuma subárea selecionada.")

    # Listar subáreas disponíveis
    subareas = area_data.get("subareas", {})
    if not subareas:
        print("Esta área não possui subáreas configuradas ainda.")
        return ""

    print("\nSubáreas disponíveis:")
    subareas_list = list(subareas.keys())

    for i, name in enumerate(subareas_list, 1):
        desc = subareas[name].get("description", "")[:80]
        print(f"{i}. {name} - {desc}")

    choice = input("\nEscolha uma subárea (número): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(subareas_list):
        subarea_name = subareas_list[int(choice) - 1]

        # Atualizar progresso do usuário
        progress = user_data.get("progress", {})
        current = progress.get("current", {})
        current["subarea"] = subarea_name

        # Salvar no banco de dados
        user_data["progress"]["current"] = current
        db.collection("users").document(user_id).set(user_data, merge=True)

        print(f"\nSubárea '{subarea_name}' selecionada!")
        return subarea_name
    else:
        print("Escolha inválida. Voltando ao menu principal.")
        return ""


def select_level(db, user_id: str, user_data: Dict, subarea_data: Dict) -> str:
    """
    Seleciona um nível disponível se o atual não existir.
    """
    # Obter níveis disponíveis
    levels = subarea_data.get("levels", {})
    if not levels:
        print("Esta subárea não possui níveis configurados.")
        return ""

    # Selecionar o primeiro nível disponível
    level_name = next(iter(levels.keys()), "iniciante")

    # Atualizar progresso do usuário
    progress = user_data.get("progress", {})
    current = progress.get("current", {})
    current["level"] = level_name

    # Salvar no banco de dados
    user_data["progress"]["current"] = current
    db.collection("users").document(user_id).set(user_data, merge=True)

    print(f"\nNível '{level_name}' selecionado automaticamente.")
    return level_name


def main_progress_loop(db, user_id: str, user_data: Dict, area_name: str, area_data: Dict,
                       subarea_name: str, subarea_data: Dict, level_name: str, level_data: Dict,
                       current: Dict, user_age: int, learning_style: str):
    """
    Loop principal para o progresso do usuário.
    """
    while True:
        # Exibir status atual
        print_current_status(area_name, subarea_name, level_name, current, subarea_data, level_data)

        # Verificar requisitos para o nível atual
        if not check_level_requirements(db, user_id, current, level_data):
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
            continue_next_step(db, user_id, user_data, area_name, subarea_name, level_name,
                               current, subarea_data, level_data, user_age, learning_style)

            # Recarregar dados após o avanço
            user_snap = db.collection("users").document(user_id).get()
            if user_snap.exists:
                user_data = user_snap.to_dict()
                progress = user_data.get("progress", {})
                current = progress.get("current", {})

                # Verificar se mudou de nível ou subárea
                new_level = current.get("level", level_name)
                new_subarea = current.get("subarea", subarea_name)

                if new_level != level_name or new_subarea != subarea_name:
                    # Recarregar dados se necessário
                    if new_subarea != subarea_name:
                        subarea_name = new_subarea
                        subarea_data = area_data.get("subareas", {}).get(subarea_name, {})

                    if new_level != level_name:
                        level_name = new_level
                        level_data = subarea_data.get("levels", {}).get(level_name, {})

        elif choice == "2":
            # Reiniciar a lição atual
            current["step_index"] = 0
            db.collection("users").document(user_id).update({"progress.current": current})
            print("A lição atual foi reiniciada. Você poderá rever todos os passos novamente.")

        elif choice == "3":
            if change_level(db, user_id, user_data, subarea_data):
                # Recarregar dados após a mudança
                user_snap = db.collection("users").document(user_id).get()
                user_data = user_snap.to_dict()
                progress = user_data.get("progress", {})
                current = progress.get("current", {})
                level_name = current.get("level", "iniciante")
                level_data = subarea_data.get("levels", {}).get(level_name, {})

        elif choice == "4":
            if change_subarea(db, user_id, user_data, area_data):
                # Recarregar dados após a mudança
                user_snap = db.collection("users").document(user_id).get()
                user_data = user_snap.to_dict()
                progress = user_data.get("progress", {})
                current = progress.get("current", {})
                subarea_name = current.get("subarea", "")
                subarea_data = area_data.get("subareas", {}).get(subarea_name, {})
                level_name = current.get("level", "iniciante")
                level_data = subarea_data.get("levels", {}).get(level_name, {})

        elif choice == "5":
            ask_teacher_question(user_age, area_name, subarea_name, level_name, learning_style)

        elif choice == "6":
            generate_complete_lesson_topic(user_age, area_name, subarea_name, level_name, learning_style)

        elif choice == "7":
            generate_assessment_topic(user_age, area_name, subarea_name, level_name, learning_style)

        elif choice == "8":
            generate_learning_pathway_topic(user_age, area_name, subarea_name, level_name, learning_style)

        elif choice == "9":
            learning_style = change_teaching_style(db, user_id)

        elif choice == "10":
            view_available_projects(db, user_id, area_name, subarea_name, level_data, user_age, learning_style)

        elif choice == "0":
            print("Saindo do modo linear.")
            break

        else:
            print("Opção inválida. Tente novamente.")


def generate_complete_lesson_topic(user_age: int, area_name: str, subarea_name: str,
                                   level_name: str, teaching_style: str):
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


def generate_assessment_topic(user_age: int, area_name: str, subarea_name: str,
                              level_name: str, teaching_style: str):
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

    # Aplicar a avaliação gerada
    apply_assessment(assessment, user_age, teaching_style)

    input("\nPressione Enter para continuar...")


def generate_learning_pathway_topic(user_age: int, area_name: str, subarea_name: str,
                                    level_name: str, teaching_style: str):
    """
    Gera um roteiro de aprendizado personalizado.
    """
    # Determinar o tópico com base no contexto atual
    topic = f"{subarea_name} ({area_name})"

    print(f"\nGerando roteiro de aprendizado para '{topic}'...")

    # Solicitar parâmetros personalizados
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

    display_learning_pathway(pathway)
    input("\nPressione Enter para continuar...")


def display_learning_pathway(pathway: Dict):
    """
    Exibe um roteiro de aprendizado de forma organizada.
    """
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


def view_available_projects(db, user_id: str, area_name: str, subarea_name: str,
                            level_data: Dict, user_age: int, teaching_style: str):
    """
    Permite ao usuário ver os projetos disponíveis no nível atual.
    Versão refatorada para melhor organização.
    """
    # Coletar todos os projetos disponíveis
    projects = collect_available_projects(level_data)

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

    # Iniciar o projeto selecionado
    register_project_started(db, user_id, selected_project['title'], selected_project['type'])

    print(f"\nVocê iniciou o projeto '{selected_project['title']}'.")
    print("Você pode continuar trabalhando nele e marcá-lo como concluído no menu de gerenciamento de projetos.")

    input("\nPressione Enter para continuar...")


def collect_available_projects(level_data: Dict) -> List[Dict]:
    """
    Coleta todos os projetos disponíveis em um nível, incluindo módulos e lições.
    """
    projects = []

    # Verificar projeto final do nível
    final_project = level_data.get("final_project", {})
    if final_project:
        project_title = final_project.get("title", "")
        if project_title:
            projects.append({
                "title": project_title,
                "description": final_project.get("description", ""),
                "type": "final",
                "source": "Nível"
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

    return projects


# Funções para o modo dinâmico de progresso
def dynamic_progress_flow(db, user_id: str):
    """
    Gerencia o fluxo de progresso dinâmico onde o usuário escolhe as subáreas.
    Versão refatorada para maior organização.
    """
    # Obter dados do usuário
    user_ref = db.collection("users").document(user_id)
    user_snap = user_ref.get()

    if not user_snap.exists:
        print("Usuário não encontrado.")
        return

    user_data = user_snap.to_dict()
    area_name = user_data.get("recommended_track", "")

    if not area_name:
        print("Nenhuma área recomendada. Faça o mapeamento primeiro.")
        return

    # Obter dados de personalização
    user_age = user_data.get("age", 14)
    learning_style = user_data.get("learning_style", "didático")

    # Carregar dados da área
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

    # Loop principal do modo dinâmico
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


def explore_subarea(db, user_id: str, area_name: str, area_data: Dict,
                    subarea_name: str, user_age: int, learning_style: str):
    """
    Permite ao usuário explorar uma subárea específica.
    Versão refatorada para melhor organização.
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

        level_names = get_level_order(levels)
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
            explore_level(db, user_id, area_name, subarea_name, selected_level,
                          levels[selected_level], user_age, learning_style)
        else:
            print("Opção inválida.")


def explore_level(db, user_id: str, area_name: str, subarea_name: str,
                  level_name: str, level_data: Dict, user_age: int, learning_style: str):
    """
    Permite ao usuário explorar um nível específico.
    Versão refatorada para melhor organização.
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
                explore_module(db, user_id, area_name, subarea_name, level_name,
                               modules[module_idx], user_age, learning_style)
            else:
                print("Módulo inválido.")
        elif choice == "2" and level_data.get("final_project"):
            show_project(db, user_id, level_data.get("final_project", {}), "final", user_age, learning_style)
        elif choice == "3" and level_data.get("final_assessment"):
            take_assessment(db, user_id, level_data.get("final_assessment", {}), "final",
                            user_age, learning_style, register_final_assessment_passed)
        elif choice == "4":
            # Definir como nível atual
            set_current_level(db, user_id, area_name, subarea_name, level_name)
        elif choice == "5":
            generate_complete_lesson_topic(user_age, area_name, subarea_name, level_name, learning_style)
        elif choice == "6":
            generate_learning_pathway_topic(user_age, area_name, subarea_name, level_name, learning_style)
        else:
            print("Opção inválida.")


def set_current_level(db, user_id: str, area_name: str, subarea_name: str, level_name: str):
    """
    Define o nível atual do usuário.
    """
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print("\nErro: Dados do usuário não encontrados.")
        return False

    # Atualizar progresso
    user_data = user_doc.to_dict()
    progress = UserProgress(user_data.get("progress", {}))

    progress.area = area_name
    progress.subarea = subarea_name
    progress.level = level_name
    progress.module_index = 0
    progress.lesson_index = 0
    progress.step_index = 0

    # Salvar no banco de dados
    user_data["progress"] = progress.to_dict()
    user_ref.set(user_data, merge=True)

    print(f"\nO nível atual foi definido como '{level_name.capitalize()}' na subárea '{subarea_name}'.")
    print("Você pode continuar seu aprendizado no modo linear.")
    return True


def explore_module(db, user_id: str, area_name: str, subarea_name: str, level_name: str,
                   module_data: Dict, user_age: int, learning_style: str):
    """
    Permite ao usuário explorar um módulo específico.
    Versão refatorada para melhor organização.
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
            generate_module_content(module_title, module_desc, user_age, area_name, subarea_name, learning_style)

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
                view_lesson(db, user_id, area_name, subarea_name, level_name,
                            module_title, lessons[lesson_idx], user_age, learning_style)
            else:
                print("Lição inválida.")
        elif choice == "2" and module_data.get("module_project"):
            show_project(db, user_id, module_data.get("module_project", {}), "module", user_age, learning_style)
        elif choice == "3" and module_data.get("module_assessment"):
            take_assessment(db, user_id, module_data.get("module_assessment", {}), "module",
                            user_age, learning_style, register_assessment_passed)
        elif choice == "4":
            set_current_module(db, user_id, area_name, subarea_name, level_name, module_title)
        else:
            print("Opção inválida.")


def set_current_module(db, user_id: str, area_name: str, subarea_name: str,
                       level_name: str, module_title: str):
    """
    Define o módulo atual do usuário.
    """
    # Buscar dados atualizados da área, subárea e nível
    area_ref = db.collection("learning_paths").document(area_name)
    area_doc = area_ref.get()

    if not area_doc.exists:
        print("\nErro: Área não encontrada.")
        return False

    area_data = area_doc.to_dict()
    subareas = area_data.get("subareas", {})

    if subarea_name not in subareas:
        print("\nErro: Subárea não encontrada.")
        return False

    subarea_data = subareas[subarea_name]
    levels = subarea_data.get("levels", {})

    if level_name not in levels:
        print("\nErro: Nível não encontrado.")
        return False

    level_data = levels[level_name]
    modules = level_data.get("modules", [])

    # Encontrar o módulo pelo título
    module_index = -1
    for i, module in enumerate(modules):
        if module.get("module_title") == module_title:
            module_index = i
            break

    if module_index < 0:
        print("\nErro: Módulo não encontrado.")
        return False

    # Atualizar dados do usuário
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print("\nErro: Dados do usuário não encontrados.")
        return False

    user_data = user_doc.to_dict()
    progress = UserProgress(user_data.get("progress", {}))

    progress.area = area_name
    progress.subarea = subarea_name
    progress.level = level_name
    progress.module_index = module_index
    progress.lesson_index = 0
    progress.step_index = 0

    # Salvar no banco de dados
    user_data["progress"] = progress.to_dict()
    user_ref.set(user_data, merge=True)

    print(f"\nMódulo atual definido como '{module_title}'.")
    print("Você pode continuar seu aprendizado no modo linear.")
    return True


def view_lesson(db, user_id: str, area_name: str, subarea_name: str, level_name: str,
                module_title: str, lesson_data: Dict, user_age: int, teaching_style: str):
    """
    Permite visualizar os detalhes de uma lição.
    Versão refatorada para melhor organização.
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
            generate_lesson_content(lesson_title, objectives, user_age, area_name, subarea_name, teaching_style)

        input("\nPressione Enter para voltar...")
        return

    # Mostrar os passos da lição
    view_lesson_steps(db, user_id, area_name, subarea_name, level_name,
                      module_title, lesson_title, lesson_data, steps, user_age, teaching_style)


def view_lesson_steps(db, user_id: str, area_name: str, subarea_name: str, level_name: str,
                      module_title: str, lesson_title: str, lesson_data: Dict, steps: List,
                      user_age: int, teaching_style: str):
    """
    Exibe todos os passos de uma lição.
    """
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
            teaching_style=teaching_style,
            knowledge_level=level_name
        )

        print(explanation)

        if i < len(steps):
            input("\nPressione Enter para o próximo passo...")

    # Verificar se há exercícios
    check_lesson_exercises(lesson_data, user_age, teaching_style)

    # Verificar se há projeto da lição
    project = lesson_data.get("project", {})
    if project:
        show_project = input("\nDeseja ver o projeto desta lição? (s/n): ").lower()
        if show_project == 's':
            show_project(db, user_id, project, "lesson", user_age, teaching_style)

    input("\nPressione Enter para voltar...")


def check_lesson_exercises(lesson_data: Dict, user_age: int, teaching_style: str):
    """
    Verifica e aplica os exercícios de uma lição.
    """
    exercises = lesson_data.get("exercises", [])
    if not exercises:
        return

    do_exercises = input("\nDeseja fazer os exercícios desta lição? (s/n): ").lower()
    if do_exercises != 's':
        return

    for i, exercise in enumerate(exercises, 1):
        question = exercise.get("question", "")
        print(f"\nExercício {i}: {question}")

        # Processar o exercício conforme seu tipo
        exercise_type = exercise.get("type", "open")
        answer = exercise.get("answer", "")

        if exercise_type == "multiple_choice" and "options" in exercise:
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


"""
Funções auxiliares para imprimir mensagens e formatação
"""


def print_header(title: str, width: int = 60):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * width)
    print(title)
    print("=" * width)


def print_subheader(title: str, width: int = 60):
    """Imprime um subcabeçalho formatado."""
    print("\n" + "-" * width)
    print(title)
    print("-" * width)


def print_progress_bar(current: int, total: int, width: int = 40):
    """
    Imprime uma barra de progresso visual.

    Args:
        current: Valor atual
        total: Valor total
        width: Largura da barra em caracteres
    """
    progress = current / total
    bar_length = int(width * progress)

    bar = "[" + "=" * bar_length + " " * (width - bar_length) + "]"
    percentage = int(progress * 100)

    print(f"{bar} {percentage}% ({current}/{total})")


def input_with_default(prompt: str, default: str) -> str:
    """
    Solicita input do usuário com um valor padrão caso o input seja vazio.

    Args:
        prompt: Texto do prompt
        default: Valor padrão

    Returns:
        O input do usuário ou o valor padrão
    """
    user_input = input(f"{prompt} [padrão: {default}]: ").strip()
    return user_input if user_input else default


def confirm_action(prompt: str) -> bool:
    """
    Solicita confirmação do usuário para uma ação.

    Args:
        prompt: Texto do prompt

    Returns:
        True se confirmado, False caso contrário
    """
    return input(f"{prompt} (s/n): ").lower() == 's'


"""
Funções de análise de conteúdo e adaptação
"""


def analyze_content_difficulty(content: str, user_age: int) -> Dict:
    """
    Analisa a dificuldade de um conteúdo para a idade do usuário.

    Args:
        content: Conteúdo a ser analisado
        user_age: Idade do usuário

    Returns:
        Dicionário com análise de dificuldade
    """
    prompt = (
        f"Analise o seguinte conteúdo educacional para determinar sua adequação "
        f"para um estudante de {user_age} anos:\n\n"
        f"{content[:2000]}...\n\n"  # Limitando para evitar tokens excessivos
        f"Forneça uma análise em JSON com os seguintes campos:\n"
        f"- adequação_idade (0.0 a 1.0): o quão adequado é para a idade\n"
        f"- complexidade_vocabulário (baixa, média, alta): nível de vocabulário\n"
        f"- complexidade_conceitual (baixa, média, alta): dificuldade dos conceitos\n"
        f"- pontos_fortes: lista de aspectos positivos\n"
        f"- sugestões_melhoria: lista de possíveis melhorias\n"
    )

    try:
        result = call_teacher_llm(
            prompt,
            student_age=user_age,
            temperature=0.3,  # Baixa temperatura para análise objetiva
            max_tokens=1000
        )

        # Processar resultado para extrair o JSON
        import json
        import re

        # Procurar por um objeto JSON no texto
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                logger.error(f"Erro ao decodificar JSON: {json_text}")

        logger.error(f"Nenhum JSON encontrado na resposta: {result}")
        return {
            "adequação_idade": 0.5,
            "complexidade_vocabulário": "média",
            "complexidade_conceitual": "média",
            "pontos_fortes": ["Conteúdo educacional básico"],
            "sugestões_melhoria": ["Análise detalhada não disponível"]
        }
    except Exception as e:
        logger.error(f"Erro ao analisar conteúdo: {e}")
        return {
            "adequação_idade": 0.5,
            "complexidade_vocabulário": "média",
            "complexidade_conceitual": "média",
            "pontos_fortes": ["Análise não disponível"],
            "sugestões_melhoria": ["Ocorreu um erro na análise"]
        }


def adapt_content_for_age(content: str, user_age: int, teaching_style: str) -> str:
    """
    Adapta um conteúdo para ser mais adequado à idade do usuário.

    Args:
        content: Conteúdo a ser adaptado
        user_age: Idade do usuário
        teaching_style: Estilo de ensino preferido

    Returns:
        Conteúdo adaptado
    """
    prompt = (
        f"Adapte o seguinte conteúdo educacional para ser mais adequado "
        f"para um estudante de {user_age} anos, mantendo o estilo de ensino {teaching_style}:\n\n"
        f"{content}\n\n"
        f"Torne o vocabulário, exemplos e complexidade conceitual apropriados para a idade, "
        f"sem perder o essencial do conteúdo. Inclua elementos visuais descritivos "
        f"e conexões com o cotidiano."
    )

    try:
        return call_teacher_llm(
            prompt,
            student_age=user_age,
            teaching_style=teaching_style,
            max_tokens=len(content.split()) * 2  # Dobro dos tokens para dar margem
        )
    except Exception as e:
        logger.error(f"Erro ao adaptar conteúdo: {e}")
        return content  # Retorna o conteúdo original em caso de erro


"""
Configuração para testes e execução direta
"""

if __name__ == "__main__":
    # Configuração para testes
    import argparse
    from app.firestore_client import get_firestore_client

    parser = argparse.ArgumentParser(description="Sistema de Gestão de Progresso Educacional")
    parser.add_argument("--user_id", help="ID do usuário para testes")
    parser.add_argument("--mode", choices=["linear", "dynamic"], default="linear",
                        help="Modo de progresso (linear ou dinâmico)")
    parser.add_argument("--debug", action="store_true", help="Ativa logs de debug")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Modo de debug ativado")

    # Obter instância do Firestore
    db = get_firestore_client()

    if not args.user_id:
        print("ID de usuário necessário. Execute com --user_id=<id>")
        exit(1)

    # Executar o modo de progresso solicitado
    if args.mode == "linear":
        continue_progress_flow(db, args.user_id)
    else:
        dynamic_progress_flow(db, args.user_id)