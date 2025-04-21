import time

from app.firestore_client import get_firestore_client


def setup_exatas_programacao_subarea(db):
    """
    Configura a subárea de Programação dentro da área de Ciências Exatas e Aplicadas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    # Primeiro, verificar se a área principal já existe
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        # Se a área não existir, criar a estrutura básica da área
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        # Se já existir, apenas recuperar os dados
        area_data = area_doc.to_dict()

    # Definir a subárea de Programação com conteúdo adequado para ensino básico e médio
    programacao_subarea = {
        "name": "Programação",
        "description": "Aprenda a criar seus próprios jogos, aplicativos e resolver problemas usando código de computador!",
        "estimated_time": "2-6 meses (dependendo da dedicação)",
        "icon": "laptop-code",  # Ícone para visualização na interface
        "references": [
            {"title": "Code.org - Hora do Código", "url": "https://code.org/"},
            {"title": "Scratch - Programação para iniciantes", "url": "https://scratch.mit.edu/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos na programação - para quem nunca programou antes",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Entender o que é programação e como os computadores funcionam",
                    "Aprender a pensar como um programador",
                    "Criar pequenos programas divertidos e jogos simples",
                    "Conhecer os blocos básicos de construção da programação"
                ],
                "modules": [
                    {
                        "module_title": "O Mundo da Programação",
                        "module_description": "Descubra o que é programação e como ela está presente no seu dia a dia",
                        "estimated_time": "2 semanas",
                        "difficulty": "muito fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "O que é Programação?",
                                "objectives": "Entender o que é programação e como ela faz parte do nosso dia a dia",
                                "estimated_time": "30 minutos",
                                "content_summary": "Uma introdução divertida ao mundo da programação, explorando exemplos do cotidiano",
                                "steps": [
                                    "O que são programas e para que servem",
                                    "Exemplos de programação no seu dia a dia (celular, jogos, sites)",
                                    "Como dar 'ordens' para o computador",
                                    "Diferentes linguagens de programação (como diferentes idiomas)"
                                ],
                                "exercises": [
                                    {
                                        "question": "Se você tivesse que explicar para um robô como escovar os dentes, quais passos você descreveria?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Resposta pessoal, mas deve incluir passos como: pegar a escova, colocar pasta, escovar em movimentos circulares, etc."
                                    },
                                    {
                                        "question": "O que é um programa de computador?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Um show de TV sobre computadores",
                                            "Um conjunto de instruções que o computador segue",
                                            "Um tipo de teclado especial",
                                            "Um jogo de videogame"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "game",
                                        "title": "Detective Bit",
                                        "description": "Descubra onde a programação está escondida em uma casa digital interativa"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Programação é como Receita de Bolo",
                                     "url": "https://exemplo.com/video1"},
                                    {"type": "artigo", "title": "O que os programadores fazem?",
                                     "url": "https://exemplo.com/artigo1"}
                                ]
                            },
                            {
                                "lesson_title": "Como os Computadores Pensam",
                                "objectives": "Entender como os computadores interpretam comandos e o pensamento lógico na programação",
                                "estimated_time": "45 minutos",
                                "steps": [
                                    "O pensamento lógico passo a passo",
                                    "Computadores seguem instruções exatas",
                                    "O que acontece quando damos instruções incompletas",
                                    "0s e 1s - a linguagem das máquinas"
                                ],
                                "exercises": [
                                    {
                                        "question": "Imagine que você é um computador e recebe esta instrução: 'Mova-se para frente'. O que está faltando nessa instrução?",
                                        "type": "open",
                                        "answer": "Falta dizer quantos passos ou por quanto tempo deve se mover para frente."
                                    }
                                ],
                                "project": {
                                    "title": "Robô Humano",
                                    "description": "Em duplas, um aluno será o 'programador' e outro o 'computador'. O programador deve dar instruções para o computador realizar uma tarefa simples, como pegar um objeto.",
                                    "expected_outcome": "Compreender que computadores precisam de instruções claras e precisas",
                                    "estimated_time": "20 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: O Mundo da Programação",
                            "format": "5 questões divertidas, jogo de combinar conceitos",
                            "passing_score": 60,
                            "time_limit": "15 minutos",
                            "certificate": "Explorador de Códigos - Nível 1"
                        }
                    },
                    {
                        "module_title": "Primeiros Programas com Blocos",
                        "module_description": "Crie seus primeiros programas usando blocos coloridos de arrastar e soltar",
                        "estimated_time": "3 semanas",
                        "prerequisites": ["O Mundo da Programação"],
                        "lessons": [
                            {
                                "lesson_title": "Programação em Blocos com Scratch",
                                "objectives": "Aprender a usar o Scratch para criar programas simples",
                                "steps": [
                                    "Conhecendo a interface do Scratch",
                                    "Movendo personagens na tela",
                                    "Criando sequências de comandos",
                                    "Mudando cores e efeitos"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais blocos do Scratch usamos para fazer um personagem andar?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Blocos de Som",
                                            "Blocos de Movimento",
                                            "Blocos de Aparência",
                                            "Blocos de Caneta"
                                        ],
                                        "correct_answer": 1
                                    }
                                ]
                            },
                            {
                                "lesson_title": "Histórias Interativas",
                                "objectives": "Criar histórias onde personagens conversam e se movem",
                                "steps": [
                                    "Adicionando diálogos com balões de fala",
                                    "Trocando cenários",
                                    "Fazendo personagens interagirem",
                                    "Adicionando efeitos especiais"
                                ],
                                "project": {
                                    "title": "Minha História Animada",
                                    "description": "Criar uma história curta com pelo menos dois personagens que conversam e se movem",
                                    "steps": [
                                        "Planejar a história em papel",
                                        "Escolher personagens e cenários",
                                        "Programar diálogos e movimentos",
                                        "Compartilhar com a turma"
                                    ],
                                    "estimated_time": "60 minutos"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Jogo de Pega-Pega",
                            "description": "Criar um jogo simples onde um personagem precisa pegar outro",
                            "deliverables": ["Código do jogo no Scratch", "Demonstração para a turma"],
                            "estimated_time": "2 horas (divididas em várias aulas)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Meu Primeiro Jogo Completo",
                    "description": "Criar um jogo completo com início, pontuação e fim de jogo",
                    "requirements": [
                        "Pelo menos 2 personagens",
                        "Sistema de pontuação",
                        "Tela de início e fim de jogo",
                        "Sons ou música"
                    ],
                    "rubric": "Será avaliado pela criatividade, funcionamento e uso correto dos conceitos aprendidos",
                    "showcase": "Feira de Jogos - apresentação para pais e colegas"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos de Programação",
                    "format": "Quiz interativo e pequeno projeto",
                    "passing_criteria": "70% no quiz e projeto funcional básico",
                    "certification": "Programador Júnior - Nível Iniciante"
                },
                "suggested_path_forward": ["Python para Jovens", "Criação de Jogos"]
            },
            "intermediario": {
                "description": "Aprendendo programação com texto e projetos mais avançados",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Python para Jovens",
                        "module_description": "Aprenda Python, uma linguagem de programação real usada por profissionais",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Do Scratch ao Python",
                                "objectives": "Entender as diferenças entre programação em blocos e em texto",
                                "steps": [
                                    "Comparando blocos do Scratch com comandos Python",
                                    "Primeiros comandos em Python (print, input)",
                                    "Regras de escrita (sintaxe) em Python",
                                    "Usando o interpretador Python online"
                                ]
                            },
                            {
                                "lesson_title": "Variáveis e Tipos em Python",
                                "objectives": "Aprender a guardar e manipular informações usando variáveis",
                                "steps": [
                                    "Criando variáveis para armazenar informações",
                                    "Tipos de dados (números, texto, listas)",
                                    "Operações com variáveis",
                                    "Entrada de dados do usuário"
                                ],
                                "project": {
                                    "title": "Calculadora Personalizada",
                                    "description": "Criar uma calculadora que pode fazer operações básicas e tem uma mensagem personalizada para o usuário"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Criando Jogos Simples em Python",
                        "module_description": "Use Python para criar jogos de texto interativos",
                        "estimated_time": "5 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Jogo de Adivinhação",
                                "objectives": "Criar um jogo onde o computador escolhe um número e o jogador tenta adivinhar",
                                "steps": [
                                    "Gerando números aleatórios",
                                    "Usando condicionais (if/else) para verificar respostas",
                                    "Loops para repetir tentativas",
                                    "Contando pontos e limitando tentativas"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "RPG de Texto",
                            "description": "Criar uma aventura interativa onde o jogador toma decisões que afetam a história",
                            "deliverables": ["Código Python", "Mapa da história", "Demonstração para a classe"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Aplicativo Útil",
                    "description": "Criar um programa Python que resolva um problema real do seu dia a dia",
                    "requirements": [
                        "Interface amigável para o usuário",
                        "Armazenamento de informações",
                        "Pelo menos 3 funcionalidades diferentes",
                        "Documentação explicando como usar"
                    ]
                }
            },
            "avancado": {
                "description": "Projetos mais complexos e conceitos avançados de programação",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Desenvolvimento Web para Adolescentes",
                        "module_description": "Aprenda a criar seus próprios sites e aplicativos web",
                        "lessons": [
                            {
                                "lesson_title": "HTML: Criando Páginas Web",
                                "objectives": "Aprender a estruturar conteúdo para a web usando HTML",
                                "steps": [
                                    "Estrutura básica de uma página HTML",
                                    "Tags para textos, imagens e links",
                                    "Listas e tabelas",
                                    "Criando múltiplas páginas"
                                ]
                            },
                            {
                                "lesson_title": "CSS: Estilizando sua Página",
                                "objectives": "Usar CSS para deixar sites bonitos e organizados",
                                "steps": [
                                    "Cores e fundos",
                                    "Tamanhos e posicionamento",
                                    "Classes e IDs",
                                    "Layouts responsivos básicos"
                                ]
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Website Completo",
                    "description": "Criar um site completo sobre um tema de seu interesse",
                    "requirements": [
                        "Pelo menos 5 páginas interligadas",
                        "Design responsivo que funciona em celulares",
                        "Formulário de contato",
                        "Menu de navegação"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Desenvolvimento de Jogos",
                "description": "Focada na criação de jogos digitais para diferentes plataformas",
                "age_range": "14-17 anos",
                "modules": [
                    "Conceitos Básicos de Game Design",
                    "Criação de Jogos 2D com Pygame",
                    "Arte para Jogos",
                    "Programação de Mecânicas de Jogo"
                ],
                "final_project": {
                    "title": "Jogo 2D Completo",
                    "description": "Criar um jogo original com vários níveis e mecânicas"
                }
            },
            {
                "name": "Robótica e Automação",
                "description": "Aplicar programação para controlar robôs e automatizar tarefas",
                "age_range": "12-17 anos",
                "modules": [
                    "Introdução à Robótica Educacional",
                    "Sensores e Atuadores",
                    "Programação de Robôs com Arduino",
                    "Projetos de Automação"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Desenvolvedor de Software",
                "Designer de Jogos",
                "Cientista de Dados",
                "Especialista em Inteligência Artificial",
                "Desenvolvedor Web"
            ],
            "day_in_life": [
                "Um programador resolve problemas usando código",
                "Trabalha em equipe com outros profissionais",
                "Cria, testa e melhora programas de computador",
                "Aprende constantemente novas tecnologias"
            ],
            "educational_paths": [
                "Cursos técnicos em programação",
                "Graduação em Ciência da Computação ou áreas relacionadas",
                "Cursos online e bootcamps",
                "Projetos pessoais para construir portfólio"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Matemática básica", "Raciocínio lógico"],
            "cross_curricular": ["Matemática", "Artes", "Português", "Ciências"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Programação"] = programacao_subarea
    area_ref.set(area_data)

    return area_data


def setup_exatas_matematica_subarea(db):
    """
    Configura a subárea de Matemática dentro da área de Ciências Exatas e Aplicadas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        # Se a área não existir, criar a estrutura básica da área
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        # Se já existir, apenas recuperar os dados
        area_data = area_doc.to_dict()

    # Definir a subárea de Matemática
    matematica_subarea = {
        "name": "Matemática",
        "description": "Explore o mundo dos números, formas e padrões de maneira divertida e prática!",
        "estimated_time": "Contínuo - desenvolve-se ao longo de todo o período escolar",
        "icon": "calculator",
        "references": [
            {"title": "Khan Academy", "url": "https://pt.khanacademy.org/"},
            {"title": "Matific", "url": "https://www.matific.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Matemática básica e pensamento lógico matemático inicial",
                "age_range": "10-12 anos",
                "learning_outcomes": [
                    "Compreender operações básicas com números inteiros e decimais",
                    "Reconhecer formas geométricas e suas propriedades",
                    "Resolver problemas matemáticos do dia a dia",
                    "Entender frações e porcentagens simples"
                ],
                "modules": [
                    {
                        "module_title": "Matemática no Cotidiano",
                        "module_description": "Aprenda como a matemática está presente em tudo o que fazemos",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Matemática nas Compras",
                                "objectives": "Aprender a usar operações matemáticas para fazer compras e calcular trocos",
                                "estimated_time": "45 minutos",
                                "content_summary": "Atividade prática sobre uso de matemática em situações de compra",
                                "steps": [
                                    "Adição e subtração em situações de compra",
                                    "Calculando valores de várias mercadorias",
                                    "Verificando se o troco está correto",
                                    "Calculando descontos simples"
                                ],
                                "exercises": [
                                    {
                                        "question": "Se você comprar um chocolate de R$3,50 e um suco de R$4,25, quanto vai gastar no total?",
                                        "type": "calculation",
                                        "answer": "R$7,75"
                                    },
                                    {
                                        "question": "Se você pagar uma conta de R$12,30 com uma nota de R$20,00, quanto receberá de troco?",
                                        "type": "calculation",
                                        "answer": "R$7,70"
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "simulação",
                                        "title": "Mercadinho Matemático",
                                        "description": "Simulador de compras onde você precisa calcular totais e trocos"
                                    }
                                ],
                                "project": {
                                    "title": "Feira da Turma",
                                    "description": "Organizar uma pequena feira onde os alunos vendem e compram itens usando dinheiro fictício, calculando preços e trocos",
                                    "estimated_time": "1 aula de 50 minutos"
                                }
                            },
                            {
                                "lesson_title": "Formas Geométricas ao Nosso Redor",
                                "objectives": "Identificar formas geométricas em objetos do dia a dia",
                                "estimated_time": "40 minutos",
                                "steps": [
                                    "Reconhecendo círculos, quadrados, triângulos e retângulos",
                                    "Formas 3D: cubos, esferas, cilindros e cones",
                                    "Caça às formas na sala de aula",
                                    "Desenhando formas e criando arte geométrica"
                                ],
                                "exercises": [
                                    {
                                        "question": "Dê 3 exemplos de objetos do seu dia a dia que têm formato de círculo.",
                                        "type": "open",
                                        "answer": "Respostas possíveis: rodas, pratos, relógios, moedas, botões, etc."
                                    }
                                ]
                            }
                        ],
                        "module_assessment": {
                            "title": "Desafio: Matemática no Dia a Dia",
                            "format": "Jogo em grupos + quiz individual",
                            "passing_score": 70,
                            "time_limit": "30 minutos",
                            "certificate": "Detetive Matemático - Nível 1"
                        }
                    },
                    {
                        "module_title": "Frações e Decimais Divertidos",
                        "module_description": "Aprenda sobre frações e números decimais de forma prática e divertida",
                        "estimated_time": "5 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Frações na Cozinha",
                                "objectives": "Entender frações usando exemplos de receitas e medidas culinárias",
                                "steps": [
                                    "O que são frações - partes de um todo",
                                    "Medidas na cozinha: 1/2 xícara, 1/4 colher, etc.",
                                    "Somando frações em receitas",
                                    "Convertendo entre frações e números decimais simples"
                                ],
                                "project": {
                                    "title": "Livro de Receitas Matemático",
                                    "description": "Criar um pequeno livro de receitas simples, destacando as frações usadas e calculando quantidades para diferentes números de pessoas",
                                    "estimated_time": "Projeto de 1 semana (trabalho em casa + apresentação)"
                                }
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Cidade Matemática",
                    "description": "Criar uma maquete de cidade usando formas geométricas e incluindo elementos que demonstrem uso de matemática (preços em lojas, horários de ônibus, etc.)",
                    "requirements": [
                        "Usar pelo menos 5 formas geométricas diferentes",
                        "Incluir exemplos de números decimais (preços)",
                        "Mostrar uso de frações em algum elemento",
                        "Apresentar um problema matemático que pode ser resolvido na sua cidade"
                    ],
                    "rubric": "Avaliação por criatividade, precisão matemática e apresentação oral"
                }
            },
            "intermediario": {
                "description": "Álgebra básica, geometria e estatística introdutória",
                "age_range": "12-15 anos",
                "modules": [
                    {
                        "module_title": "Introdução à Álgebra",
                        "module_description": "Aprenda a trabalhar com variáveis e expressões algébricas",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Das Palavras às Equações",
                                "objectives": "Aprender a transformar problemas escritos em equações matemáticas",
                                "steps": [
                                    "Usando letras para representar valores desconhecidos",
                                    "Transformando frases em expressões matemáticas",
                                    "Resolvendo equações simples de primeiro grau",
                                    "Verificando as soluções"
                                ],
                                "exercises": [
                                    {
                                        "question": "Transforme em equação: 'Um número mais 5 é igual a 12'. Depois resolva.",
                                        "type": "equation",
                                        "answer": "x + 5 = 12, então x = 7"
                                    }
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Jogo de Mistérios Algébricos",
                            "description": "Criar um jogo de cartas ou tabuleiro onde os jogadores precisam resolver enigmas algébricos para avançar",
                            "deliverables": ["Jogo físico com regras", "Pelo menos 10 enigmas/problemas",
                                             "Demonstração para a turma"]
                        }
                    },
                    {
                        "module_title": "Estatística do Dia a Dia",
                        "module_description": "Aprenda a coletar, analisar e apresentar dados",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Pesquisas e Gráficos",
                                "objectives": "Aprender a coletar dados através de pesquisas e representá-los em gráficos",
                                "steps": [
                                    "Criando questionários simples",
                                    "Tabulando dados coletados",
                                    "Fazendo gráficos de barras e setores (pizza)",
                                    "Interpretando dados visuais"
                                ]
                            }
                        ]
                    }
                ]
            },
            "avancado": {
                "description": "Matemática mais avançada para o ensino médio",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Funções e Modelagem",
                        "module_description": "Aprenda a usar funções para modelar situações do mundo real",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Funções na Prática",
                                "objectives": "Entender como as funções matemáticas descrevem relações do mundo real",
                                "steps": [
                                    "Identificando funções no cotidiano (custo x quantidade, distância x tempo)",
                                    "Representando funções com equações, tabelas e gráficos",
                                    "Funções lineares e quadráticas - comportamento e aplicações",
                                    "Usando funções para fazer previsões"
                                ],
                                "exercises": [
                                    {
                                        "question": "Um plano de celular custa R$30,00 fixos mais R$0,50 por minuto de ligação. Escreva a função que representa o custo total C em função do tempo t em minutos.",
                                        "type": "equation",
                                        "answer": "C(t) = 30 + 0,5t"
                                    }
                                ]
                            },
                            {
                                "lesson_title": "Modelagem com Tecnologia",
                                "objectives": "Usar ferramentas digitais para modelar e resolver problemas matemáticos",
                                "steps": [
                                    "Introdução a planilhas eletrônicas para matemática",
                                    "Criando e manipulando gráficos de funções",
                                    "Simulações com valores diferentes",
                                    "Resolução de problemas com tecnologia"
                                ],
                                "project": {
                                    "title": "Simulador de Orçamento Pessoal",
                                    "description": "Criar uma planilha que modela receitas e despesas, permitindo simular diferentes cenários financeiros",
                                    "estimated_time": "3 horas (em múltiplas sessões)"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Matemática Financeira",
                        "module_description": "Aprenda conceitos financeiros essenciais usando matemática",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Juros e Investimentos",
                                "objectives": "Entender como funcionam juros simples e compostos e sua aplicação em investimentos",
                                "steps": [
                                    "Diferença entre juros simples e compostos",
                                    "Calculando juros em diferentes cenários",
                                    "Simulando investimentos ao longo do tempo",
                                    "Comparando opções de investimento"
                                ]
                            },
                            {
                                "lesson_title": "Financiamentos e Empréstimos",
                                "objectives": "Entender como funcionam financiamentos e calcular o custo real de empréstimos",
                                "steps": [
                                    "Calculando prestações e valor total",
                                    "Entendendo o impacto da taxa de juros",
                                    "Calculando o valor presente de pagamentos futuros",
                                    "Tomando decisões financeiras informadas"
                                ],
                                "project": {
                                    "title": "Comparativo de Compras",
                                    "description": "Analisar diferentes cenários de compra (à vista com desconto vs. parcelado) e determinar a opção mais vantajosa em diferentes situações"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Feira de Educação Financeira",
                            "description": "Organizar uma feira onde os alunos apresentam simuladores, infográficos e jogos sobre conceitos de matemática financeira para a comunidade escolar",
                            "deliverables": ["Material educativo", "Apresentação interativa", "Relatório de feedback dos participantes"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Aplicação Matemática",
                    "description": "Desenvolver um projeto que aplica conceitos matemáticos avançados para resolver um problema real da comunidade ou escola",
                    "requirements": [
                        "Usar conceitos de pelo menos dois módulos diferentes",
                        "Incluir coleta e análise de dados reais",
                        "Criar pelo menos uma modelagem matemática",
                        "Apresentar resultados em formato visual (gráficos, infográficos)",
                        "Propor soluções baseadas na análise matemática"
                    ],
                    "rubric": "Avaliação baseada em rigor matemático, relevância prática, criatividade e comunicação clara"
                }
            }
        },
        "specializations": [
            {
                "name": "Matemática para Finanças",
                "description": "Aplicação da matemática no mundo financeiro e dos negócios",
                "age_range": "15-17 anos",
                "modules": [
                    "Análise de Investimentos",
                    "Planejamento Financeiro",
                    "Matemática para Empreendedores",
                    "Estatística Aplicada a Negócios"
                ]
            },
            {
                "name": "Matemática Computacional",
                "description": "Intersecção entre matemática e ciência da computação",
                "age_range": "14-17 anos",
                "modules": [
                    "Lógica Matemática e Programação",
                    "Algoritmos Matemáticos",
                    "Matemática Discreta",
                    "Visualização de Dados"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Analista Financeiro",
                "Estatístico",
                "Atuário",
                "Engenheiro",
                "Professor de Matemática",
                "Cientista de Dados"
            ],
            "day_in_life": [
                "Um estatístico coleta e analisa dados para encontrar padrões e tendências",
                "Um analista financeiro usa matemática para avaliar investimentos e riscos",
                "Um engenheiro aplica conceitos matemáticos para projetar estruturas e sistemas",
                "Um cientista de dados combina estatística, programação e matemática para extrair insights"
            ],
            "educational_paths": [
                "Graduação em Matemática, Estatística ou áreas relacionadas",
                "Cursos técnicos em áreas que aplicam matemática",
                "Certificações específicas em ferramentas de análise de dados",
                "Olimpíadas de Matemática e competições"
            ]
        },
        "learning_resources": {
            "apps": [
                {"name": "GeoGebra", "description": "Aplicativo gratuito para geometria, álgebra e cálculo"},
                {"name": "Photomath", "description": "App que resolve e explica problemas matemáticos"},
                {"name": "Khan Academy", "description": "Plataforma com aulas e exercícios gratuitos"}
            ],
            "games": [
                {"name": "Prodigy", "description": "Jogo de RPG com desafios matemáticos"},
                {"name": "DragonBox", "description": "Série de jogos que ensinam álgebra e geometria"}
            ],
            "websites": [
                {"name": "Matemática Rio", "url": "https://www.matematicario.com.br/"},
                {"name": "OBMEP", "url": "https://www.obmep.org.br/"}
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Matemática básica de anos anteriores"],
            "cross_curricular": ["Ciências", "Geografia", "Economia", "Física"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Matemática"] = matematica_subarea
    area_ref.set(area_data)

    return area_data



def setup_exatas_fisica_subarea(db):
    """
    Configura a subárea de Física dentro da área de Ciências Exatas e Aplicadas.
    """
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    fisica_subarea = {
        "name": "Física",
        "description": "Descubra como funcionam as leis que regem o universo, desde o movimento dos objetos até a energia e as forças da natureza.",
        "estimated_time": "Contínuo - conhecimento que se desenvolve durante todo o período escolar",
        "icon": "atom",
        "references": [
            {"title": "Khan Academy - Física", "url": "https://pt.khanacademy.org/science/physics"},
            {"title": "PhET Simulações Interativas", "url": "https://phet.colorado.edu/pt_BR/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução aos conceitos básicos da física de forma prática e divertida",
                "age_range": "10-13 anos",
                "learning_outcomes": [
                    "Entender conceitos básicos de movimento, forças e energia",
                    "Realizar experimentos simples para observar leis físicas",
                    "Aplicar conceitos físicos para explicar fenômenos do cotidiano",
                    "Desenvolver o pensamento científico através de observações e hipóteses"
                ],
                "modules": [
                    {
                        "module_title": "Movimento e Forças no Dia a Dia",
                        "module_description": "Explore como os objetos se movem e por que mudam de direção",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Empurrões e Puxões: Introdução às Forças",
                                "objectives": "Entender que forças são empurrões e puxões que podem alterar o movimento dos objetos",
                                "estimated_time": "45 minutos",
                                "steps": [
                                    "O que são forças e como elas agem nos objetos",
                                    "Identificando forças no nosso dia a dia",
                                    "Como medir a intensidade de uma força",
                                    "Forças equilibradas e desequilibradas"
                                ],
                                "exercises": [
                                    {
                                        "question": "Cite três exemplos de forças que você usa no seu dia a dia.",
                                        "type": "open",
                                        "answer": "Respostas possíveis: empurrar uma porta, puxar uma gaveta, levantar uma mochila, etc."
                                    },
                                    {
                                        "question": "O que acontece quando aplicamos forças em direções opostas em um objeto?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "O objeto sempre quebra",
                                            "O objeto se move na direção da força maior",
                                            "O objeto gira rapidamente",
                                            "O objeto continua parado"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Medidor de Forças",
                                    "description": "Construir um dinamômetro simples com elásticos e utilizá-lo para medir e comparar diferentes forças",
                                    "estimated_time": "60 minutos"
                                }
                            },
                            {
                                "lesson_title": "Gravidade: A Força que nos Mantém no Chão",
                                "objectives": "Compreender a força da gravidade e seus efeitos",
                                "steps": [
                                    "O que é gravidade e como ela age",
                                    "Gravidade na Terra e no espaço",
                                    "Por que os objetos caem",
                                    "Como a gravidade afeta diferentes objetos"
                                ],
                                "exercises": [
                                    {
                                        "question": "Uma pena e uma bola caem ao mesmo tempo no vácuo. Quem chega primeiro ao solo?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "A pena",
                                            "A bola",
                                            "Chegam juntas",
                                            "Nenhuma cai no vácuo"
                                        ],
                                        "correct_answer": 2,
                                        "explanation": "Sem resistência do ar, todos os objetos caem com a mesma aceleração devido à gravidade."
                                    }
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Parque de Diversões da Física",
                            "description": "Criar modelos de brinquedos de parque de diversões que demonstrem diferentes princípios físicos",
                            "deliverables": ["Modelos de pelo menos 2 brinquedos", "Explicação dos princípios físicos envolvidos"],
                            "estimated_time": "2 aulas de 50 minutos"
                        }
                    },
                    {
                        "module_title": "Energia à Nossa Volta",
                        "module_description": "Descubra os diferentes tipos de energia e como ela se transforma",
                        "estimated_time": "5 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Energia em Movimento",
                                "objectives": "Entender a energia cinética e potencial e suas transformações",
                                "steps": [
                                    "O que é energia e suas formas",
                                    "Energia potencial (armazenada) e cinética (movimento)",
                                    "Transformações de energia",
                                    "Conservação de energia"
                                ],
                                "project": {
                                    "title": "Montanha-Russa de Bolinhas",
                                    "description": "Criar uma pista para bolinhas que demonstre as transformações entre energia potencial e cinética",
                                    "estimated_time": "90 minutos"
                                }
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Máquina de Reações em Cadeia",
                    "description": "Construir uma máquina de Rube Goldberg que demonstre diferentes princípios físicos",
                    "requirements": [
                        "Pelo menos 5 etapas diferentes",
                        "Uso de pelo menos 3 princípios físicos diferentes",
                        "Documentação do processo com fotos ou vídeos",
                        "Explicação oral dos princípios físicos utilizados"
                    ]
                }
            },
            "intermediario": {
                "description": "Aprofundamento nos conceitos físicos com abordagem mais quantitativa",
                "age_range": "13-15 anos",
                "modules": [
                    {
                        "module_title": "Mecânica: As Leis do Movimento",
                        "module_description": "Estude as Leis de Newton e como prever o movimento dos objetos",
                        "lessons": [
                            {
                                "lesson_title": "As Três Leis de Newton",
                                "objectives": "Compreender e aplicar as três leis de Newton do movimento",
                                "steps": [
                                    "Lei da Inércia (1ª Lei)",
                                    "Lei da Força e Aceleração (2ª Lei)",
                                    "Lei da Ação e Reação (3ª Lei)",
                                    "Aplicações práticas das leis de Newton"
                                ]
                            }
                        ]
                    },
                    {
                        "module_title": "Eletricidade Básica",
                        "module_description": "Descobrir como funciona a eletricidade que usamos todos os dias",
                        "lessons": [
                            {
                                "lesson_title": "Circuitos Elétricos Simples",
                                "objectives": "Aprender a montar e analisar circuitos elétricos básicos",
                                "steps": [
                                    "Componentes básicos: pilhas, lâmpadas, fios",
                                    "Circuitos em série e paralelo",
                                    "Medindo corrente e tensão",
                                    "Leis de Ohm básicas"
                                ],
                                "project": {
                                    "title": "Jogo de Perguntas e Respostas Elétrico",
                                    "description": "Criar um jogo onde as respostas corretas fecham um circuito e acendem uma luz"
                                }
                            }
                        ]
                    }
                ]
            },
            "avancado": {
                "description": "Física para o ensino médio com abordagem mais aprofundada e matemática",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Física e Tecnologia",
                        "module_description": "Entenda os princípios físicos por trás das tecnologias modernas",
                        "lessons": [
                            {
                                "lesson_title": "Ondas e Comunicação",
                                "objectives": "Compreender como as ondas eletromagnéticas são usadas em comunicações",
                                "steps": [
                                    "Espectro eletromagnético",
                                    "Como funcionam rádio, TV e celulares",
                                    "Transmissão digital vs. analógica",
                                    "Fibra óptica e comunicação por luz"
                                ]
                            }
                        ]
                    },
                    {
                        "module_title": "Física Moderna: Uma Introdução",
                        "module_description": "Explore os conceitos básicos da física do século XX",
                        "lessons": [
                            {
                                "lesson_title": "Relatividade para Iniciantes",
                                "objectives": "Compreender as ideias básicas da Teoria da Relatividade de Einstein",
                                "steps": [
                                    "O problema da velocidade da luz",
                                    "Tempo e espaço relativos",
                                    "A famosa equação E=mc²",
                                    "Aplicações práticas da relatividade"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Infográfico de Física Moderna",
                            "description": "Criar um infográfico digital ou físico explicando um conceito de física moderna e suas aplicações no mundo atual"
                        }
                    }
                ],
                "final_project": {
                    "title": "Desafio Tecnológico",
                    "description": "Desenvolver um projeto que aplique princípios físicos para resolver um problema real ou criar um dispositivo útil",
                    "requirements": [
                        "Aplicação clara de princípios físicos estudados",
                        "Documentação completa do processo de desenvolvimento",
                        "Testes e análise de resultados",
                        "Apresentação para uma banca avaliadora"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Astronomia e Astrofísica",
                "description": "Estudo dos corpos celestes e dos fenômenos físicos do universo",
                "age_range": "12-17 anos",
                "modules": [
                    "Sistema Solar e Exploração Espacial",
                    "Estrelas e Galáxias",
                    "Cosmologia Básica",
                    "Observação Astronômica Prática"
                ]
            },
            {
                "name": "Robótica Física",
                "description": "Aplicação da física na construção e programação de robôs",
                "age_range": "13-17 anos",
                "modules": [
                    "Mecânica para Robótica",
                    "Sensores e Atuadores",
                    "Energia e Potência em Robôs",
                    "Projeto Integrado de Robótica"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Físico",
                "Engenheiro",
                "Astrônomo",
                "Meteorologista",
                "Técnico em Eletrônica",
                "Professor de Física",
                "Pesquisador em Energias Renováveis"
            ],
            "day_in_life": [
                "Um físico realiza experimentos para testar teorias sobre como o universo funciona",
                "Um engenheiro usa princípios físicos para projetar estruturas e máquinas",
                "Um meteorologista aplica física atmosférica para prever o tempo",
                "Um técnico em eletrônica usa conhecimentos de física para consertar e criar dispositivos"
            ]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Física"] = fisica_subarea
    area_ref.set(area_data)

    return area_data


def setup_exatas_quimica_subarea(db):
    """
    Configura a subárea de Química dentro da área de Ciências Exatas e Aplicadas.
    """
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    quimica_subarea = {
        "name": "Química",
        "description": "Explore o fascinante mundo da matéria, suas propriedades, transformações e as reações que ocorrem ao nosso redor.",
        "estimated_time": "Contínuo - desenvolve-se ao longo do período escolar",
        "icon": "flask",
        "references": [
            {"title": "Khan Academy - Química", "url": "https://pt.khanacademy.org/science/chemistry"},
            {"title": "Manual da Química", "url": "https://www.manualdaquimica.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução ao mundo da química de forma prática e visual",
                "age_range": "11-13 anos",
                "learning_outcomes": [
                    "Identificar propriedades da matéria e suas transformações",
                    "Reconhecer reações químicas no cotidiano",
                    "Compreender estados físicos e mudanças de estado",
                    "Relacionar a química com fenômenos do dia a dia"
                ],
                "modules": [
                    {
                        "module_title": "Química na Cozinha",
                        "module_description": "Descubra como a química está presente no preparo dos alimentos",
                        "estimated_time": "3 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Misturas e Soluções",
                                "objectives": "Entender diferentes tipos de misturas através de exemplos culinários",
                                "steps": [
                                    "Misturas homogêneas e heterogêneas na cozinha",
                                    "Soluções: soluto e solvente",
                                    "Separação de misturas em receitas",
                                    "Concentração de soluções"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual tipo de mistura é o suco de laranja com polpa?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Mistura homogênea",
                                            "Mistura heterogênea",
                                            "Substância pura",
                                            "Composto"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Laboratório de Sorvetes",
                                    "description": "Preparar diferentes sorvetes e explorar conceitos de soluções, misturas e mudanças de estado",
                                    "estimated_time": "60 minutos"
                                }
                            },
                            {
                                "lesson_title": "Reações Químicas na Cozinha",
                                "objectives": "Identificar transformações químicas que ocorrem durante o cozimento",
                                "steps": [
                                    "Evidências de reações químicas",
                                    "Fermentação em pães e bolos",
                                    "Caramelização e reação de Maillard",
                                    "Ácidos e bases na culinária"
                                ]
                            }
                        ]
                    },
                    {
                        "module_title": "Matéria e Suas Transformações",
                        "module_description": "Explore os estados físicos e as transformações da matéria",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Estados Físicos da Matéria",
                                "objectives": "Compreender os diferentes estados físicos e suas características",
                                "steps": [
                                    "Sólidos, líquidos e gases",
                                    "Características de cada estado",
                                    "Modelo de partículas simples",
                                    "Mudanças de estado no dia a dia"
                                ],
                                "project": {
                                    "title": "Estação Meteorológica",
                                    "description": "Construir uma estação meteorológica simples para observar mudanças de estado na natureza (ciclo da água)"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Desafio das Transformações",
                            "format": "Estações de experimentação + quiz em grupo",
                            "passing_score": 70,
                            "certificate": "Explorador Químico - Nível 1"
                        }
                    }
                ],
                "final_project": {
                    "title": "Feira de Química Cotidiana",
                    "description": "Criar uma demonstração ou experimento que explique um fenômeno químico presente no dia a dia",
                    "requirements": [
                        "Usar materiais seguros e acessíveis",
                        "Explicar claramente o fenômeno químico demonstrado",
                        "Criar um cartaz ou apresentação visual",
                        "Apresentar para colegas e responder perguntas"
                    ]
                }
            },
            "intermediario": {
                "description": "Estrutura atômica, tabela periódica e reações químicas básicas",
                "age_range": "13-15 anos",
                "modules": [
                    {
                        "module_title": "Átomos e Moléculas",
                        "module_description": "Entenda as partículas básicas que formam toda a matéria",
                        "lessons": [
                            {
                                "lesson_title": "Estrutura Atômica",
                                "objectives": "Compreender a estrutura do átomo e suas partículas",
                                "steps": [
                                    "Modelos atômicos ao longo da história",
                                    "Prótons, nêutrons e elétrons",
                                    "Número atômico e número de massa",
                                    "Isótopos e suas aplicações"
                                ]
                            },
                            {
                                "lesson_title": "Ligações Químicas",
                                "objectives": "Entender como os átomos se unem para formar moléculas",
                                "steps": [
                                    "Ligações iônicas",
                                    "Ligações covalentes",
                                    "Ligações metálicas",
                                    "Geometria molecular básica"
                                ],
                                "project": {
                                    "title": "Modelos Moleculares",
                                    "description": "Construir modelos 3D de moléculas comuns usando materiais simples"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Tabela Periódica: O Mapa da Química",
                        "module_description": "Explore a organização dos elementos e suas propriedades",
                        "lessons": [
                            {
                                "lesson_title": "Navegando pela Tabela Periódica",
                                "objectives": "Compreender a organização e padrões da tabela periódica",
                                "steps": [
                                    "História e evolução da tabela periódica",
                                    "Famílias e períodos",
                                    "Propriedades periódicas",
                                    "Elementos no cotidiano"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Tabela Periódica Interativa",
                            "description": "Criar uma tabela periódica criativa que destaque aplicações reais dos elementos"
                        }
                    }
                ]
            },
            "avancado": {
                "description": "Físico-química, química orgânica e análises químicas",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Química Orgânica no Dia a Dia",
                        "module_description": "Explore os compostos de carbono presentes em nossa vida",
                        "lessons": [
                            {
                                "lesson_title": "Introdução aos Compostos Orgânicos",
                                "objectives": "Compreender a química do carbono e seus compostos",
                                "steps": [
                                    "Características do átomo de carbono",
                                    "Hidrocarbonetos e suas aplicações",
                                    "Principais grupos funcionais",
                                    "Compostos orgânicos no cotidiano"
                                ]
                            }
                        ]
                    },
                    {
                        "module_title": "Química e Sustentabilidade",
                        "module_description": "Entenda como a química pode ajudar a resolver problemas ambientais",
                        "lessons": [
                            {
                                "lesson_title": "Química Verde",
                                "objectives": "Compreender os princípios da química sustentável",
                                "steps": [
                                    "Princípios da química verde",
                                    "Redução de resíduos em processos químicos",
                                    "Biocombustíveis e energias alternativas",
                                    "Materiais biodegradáveis e recicláveis"
                                ],
                                "project": {
                                    "title": "Solução Verde",
                                    "description": "Desenvolver uma solução química sustentável para um problema ambiental local"
                                }
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Química em Ação",
                    "description": "Desenvolver um projeto de pesquisa sobre um problema real que pode ser solucionado com conhecimentos químicos",
                    "requirements": [
                        "Escolher um problema relevante (ambiental, industrial, saúde, etc.)",
                        "Realizar pesquisa bibliográfica sobre o tema",
                        "Propor uma solução baseada em princípios químicos",
                        "Quando possível, testar a solução em pequena escala",
                        "Apresentar os resultados em formato de artigo científico simplificado"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Química Forense",
                "description": "Aplicação da química na investigação criminal e análise de evidências",
                "age_range": "15-17 anos",
                "modules": [
                    "Coleta e Análise de Evidências Químicas",
                    "Toxicologia Básica",
                    "Identificação de Substâncias",
                    "Documentação Científica"
                ]
            },
            {
                "name": "Química dos Alimentos",
                "description": "Estudo dos processos químicos envolvidos na produção, conservação e preparo dos alimentos",
                "age_range": "13-17 anos",
                "modules": [
                    "Conservação e Deterioração de Alimentos",
                    "Reações Culinárias",
                    "Aditivos Alimentares",
                    "Análise Sensorial"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Químico",
                "Farmacêutico",
                "Engenheiro Químico",
                "Técnico em Laboratório",
                "Cientista de Alimentos",
                "Pesquisador em Cosméticos",
                "Professor de Química"
            ],
            "day_in_life": [
                "Um químico analisa substâncias em laboratório para determinar suas propriedades",
                "Um engenheiro químico projeta processos industriais para produção em larga escala",
                "Um cientista forense usa química para analisar evidências de crimes",
                "Um pesquisador farmacêutico desenvolve novos medicamentos baseados em reações químicas"
            ]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Química"] = quimica_subarea
    area_ref.set(area_data)

    return area_data


def setup_exatas_robotica_subarea(db):
    """
    Configura a subárea de Robótica dentro da área de Ciências Exatas e Aplicadas.
    """
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    robotica_subarea = {
        "name": "Robótica",
        "description": "Aprenda a criar e programar robôs, combinando conhecimentos de eletrônica, mecânica e programação.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "robot",
        "references": [
            {"title": "Arduino Brasil", "url": "https://www.arduino.cc/"},
            {"title": "Robotics for Kids", "url": "https://www.roboticsforkids.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos com robótica e automação",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os princípios básicos da robótica",
                    "Montar estruturas simples com kits de robótica",
                    "Programar comandos básicos para controlar movimentos",
                    "Entender sensores e atuadores simples"
                ],
                "modules": [
                    {
                        "module_title": "Introdução à Robótica",
                        "module_description": "Descubra o que são robôs e como eles funcionam",
                        "estimated_time": "3 semanas",
                        "lessons": [
                            {
                                "lesson_title": "O que é um Robô?",
                                "objectives": "Entender o conceito de robótica e os tipos de robôs existentes",
                                "steps": [
                                    "Definição de robô e robótica",
                                    "História da robótica",
                                    "Robôs no nosso dia a dia",
                                    "Principais tipos de robôs e suas aplicações"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são as três características principais que definem um robô?",
                                        "type": "open",
                                        "answer": "Sensores (perceber o ambiente), processamento (tomar decisões) e atuadores (agir sobre o ambiente)."
                                    }
                                ],
                                "project": {
                                    "title": "Meu Primeiro Robô de Papel",
                                    "description": "Criar um modelo de robô articulado usando papel, para entender os conceitos de juntas e movimento",
                                    "estimated_time": "45 minutos"
                                }
                            },
                            {
                                "lesson_title": "Componentes Básicos de um Robô",
                                "objectives": "Identificar e entender as principais partes de um robô",
                                "steps": [
                                    "Estrutura e chassis",
                                    "Motores e atuadores",
                                    "Sensores básicos",
                                    "Controladores (cérebro do robô)"
                                ]
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Fundamentos da Robótica",
                            "format": "Perguntas de múltipla escolha e identificação de componentes",
                            "passing_score": 70,
                            "certificate": "Iniciado em Robótica"
                        }
                    },
                    {
                        "module_title": "Construindo Mecanismos",
                        "module_description": "Aprenda a criar estruturas mecânicas para robôs",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Rodas e Movimentos",
                                "objectives": "Aprender sobre diferentes sistemas de locomoção para robôs",
                                "steps": [
                                    "Tipos de rodas e suas vantagens",
                                    "Sistemas de tração e direção",
                                    "Equilíbrio e estabilidade",
                                    "Desafios de terreno e obstáculos"
                                ],
                                "project": {
                                    "title": "Veículo com Tração",
                                    "description": "Construir um veículo simples que consiga se movimentar usando rodas e um sistema de propulsão"
                                }
                            },
                            {
                                "lesson_title": "Garras e Manipuladores",
                                "objectives": "Aprender a construir mecanismos para agarrar objetos",
                                "steps": [
                                    "Tipos de garras e pinças",
                                    "Princípios mecânicos (alavancas, engrenagens)",
                                    "Controle de força e precisão",
                                    "Desenho e montagem de garras simples"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Robô Coletor",
                            "description": "Criar um robô simples que consiga se mover e coletar pequenos objetos",
                            "deliverables": ["Estrutura montada", "Demonstração de funcionamento"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Desafio de Resgate",
                    "description": "Construir um robô que consiga navegar por um pequeno percurso e resgatar um objeto",
                    "requirements": [
                        "O robô deve se mover de forma autônoma ou por controle remoto",
                        "Deve ter algum mecanismo para agarrar ou empurrar objetos",
                        "Precisa superar pelo menos um obstáculo no percurso",
                        "Documentação do processo de construção"
                    ]
                }
            },
            "intermediario": {
                "description": "Programação e sensores para robótica mais avançada",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Programação para Robôs",
                        "module_description": "Aprenda a programar comportamentos em robôs",
                        "lessons": [
                            {
                                "lesson_title": "Lógica de Programação para Robótica",
                                "objectives": "Compreender estruturas básicas de programação aplicadas à robótica",
                                "steps": [
                                    "Sequências de comandos",
                                    "Condicionais (se... então...)",
                                    "Loops (repetições)",
                                    "Variáveis para armazenar informações"
                                ]
                            },
                            {
                                "lesson_title": "Sensores e Decisões",
                                "objectives": "Usar sensores para que o robô tome decisões",
                                "steps": [
                                    "Tipos de sensores (toque, luz, distância)",
                                    "Leitura e interpretação de dados dos sensores",
                                    "Tomada de decisão baseada nos sensores",
                                    "Calibração e testes"
                                ],
                                "project": {
                                    "title": "Robô Seguidor de Linha",
                                    "description": "Programar um robô para seguir uma linha usando sensores de luz"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Arduino Básico",
                        "module_description": "Aprenda a usar a plataforma Arduino para controlar robôs",
                        "lessons": [
                            {
                                "lesson_title": "Introdução ao Arduino",
                                "objectives": "Entender a plataforma Arduino e seu ambiente de programação",
                                "steps": [
                                    "O que é Arduino e suas aplicações",
                                    "Componentes básicos e instalação",
                                    "Primeiro programa (Blink)",
                                    "Estrutura de um sketch Arduino"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Robô Controlado por Arduino",
                            "description": "Construir um pequeno robô controlado por Arduino que reaja a estímulos do ambiente"
                        }
                    }
                ]
            },
            "avancado": {
                "description": "Robótica avançada com inteligência artificial e automação",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Robôs Autônomos",
                        "module_description": "Desenvolva robôs que tomam decisões baseadas no ambiente",
                        "lessons": [
                            {
                                "lesson_title": "Navegação Autônoma",
                                "objectives": "Programar robôs para navegar em ambientes desconhecidos",
                                "steps": [
                                    "Mapeamento de ambiente",
                                    "Algoritmos de pathfinding",
                                    "Evitando obstáculos",
                                    "Tomada de decisão em tempo real"
                                ]
                            }
                        ]
                    },
                    {
                        "module_title": "Introdução à IA para Robótica",
                        "module_description": "Aplicar conceitos básicos de inteligência artificial em robôs",
                        "lessons": [
                            {
                                "lesson_title": "Aprendizado de Máquina Simples",
                                "objectives": "Entender como robôs podem aprender com experiências",
                                "steps": [
                                    "Conceitos básicos de aprendizado de máquina",
                                    "Coleta de dados para treinamento",
                                    "Reconhecimento de padrões simples",
                                    "Implementação de algoritmos básicos"
                                ],
                                "project": {
                                    "title": "Robô que Aprende",
                                    "description": "Criar um robô que melhora seu desempenho em uma tarefa através de tentativa e erro"
                                }
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Projeto de Automação",
                    "description": "Desenvolver um sistema robótico que automatiza uma tarefa real do cotidiano",
                    "requirements": [
                        "Identificar um problema real que possa ser resolvido com automação",
                        "Projetar e construir um protótipo funcional",
                        "Programar comportamentos inteligentes",
                        "Testar em situações reais e refinar",
                        "Apresentar o projeto com documentação completa"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Drones e Veículos Aéreos",
                "description": "Construção e programação de veículos aéreos não tripulados",
                "age_range": "14-17 anos",
                "modules": [
                    "Princípios de Voo",
                    "Sistemas de Controle de Voo",
                    "Programação de Missões",
                    "Aplicações de Drones"
                ]
            },
            {
                "name": "Competições de Robótica",
                "description": "Preparação para participação em torneios de robótica",
                "age_range": "12-17 anos",
                "modules": [
                    "Regras e Categorias de Competição",
                    "Estratégias de Design para Competição",
                    "Trabalho em Equipe",
                    "Otimização de Desempenho"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Engenheiro de Robótica",
                "Técnico em Automação",
                "Desenvolvedor de Sistemas Embarcados",
                "Projetista de Drones",
                "Especialista em IA para Robótica",
                "Professor/Pesquisador em Robótica"
            ],
            "day_in_life": [
                "Um engenheiro de robótica projeta, testa e melhora sistemas robóticos",
                "Um especialista em automação industrial programa robôs para linhas de produção",
                "Um pesquisador desenvolve novos algoritmos para tornar os robôs mais inteligentes",
                "Um técnico mantém e repara robôs em hospitais, fábricas e outros ambientes"
            ]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Robótica"] = robotica_subarea
    area_ref.set(area_data)

    return area_data


def setup_exatas_astronomia_subarea(db):
    """
    Configura a subárea de Astronomia dentro da área de Ciências Exatas e Aplicadas.
    """
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    astronomia_subarea = {
        "name": "Astronomia",
        "description": "Explore o universo, desde o sistema solar até as galáxias mais distantes, compreendendo os astros e fenômenos cósmicos.",
        "estimated_time": "6-24 meses (dependendo da dedicação)",
        "icon": "star",
        "references": [
            {"title": "NASA Space Place", "url": "https://spaceplace.nasa.gov/"},
            {"title": "Stellarium - Planetário Virtual", "url": "https://stellarium.org/pt/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução ao céu noturno e aos conceitos básicos de astronomia",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Identificar as principais constelações no céu noturno",
                    "Compreender o sistema solar e seus planetas",
                    "Entender os movimentos básicos da Terra, Lua e Sol",
                    "Utilizar instrumentos simples de observação astronômica"
                ],
                "modules": [
                    {
                        "module_title": "Explorando o Céu Noturno",
                        "module_description": "Aprenda a identificar estrelas, planetas e constelações a olho nu",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Orientação pelo Céu",
                                "objectives": "Aprender a se localizar usando o céu noturno",
                                "steps": [
                                    "Encontrando os pontos cardeais pelo céu",
                                    "Identificando a estrela Polar e a constelação do Cruzeiro do Sul",
                                    "Movimentos aparentes das estrelas",
                                    "Uso de mapas celestes básicos"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que as estrelas parecem se mover no céu ao longo da noite?",
                                        "type": "open",
                                        "answer": "As estrelas parecem se mover devido à rotação da Terra em seu próprio eixo, criando uma ilusão de movimento no céu."
                                    }
                                ],
                                "project": {
                                    "title": "Diário de Observação Celeste",
                                    "description": "Criar um diário de observações do céu noturno durante uma semana, registrando as mudanças percebidas",
                                    "estimated_time": "7 dias (10-15 minutos por dia)"
                                }
                            },
                            {
                                "lesson_title": "Constelações e Suas Histórias",
                                "objectives": "Conhecer as principais constelações e suas mitologias",
                                "steps": [
                                    "Constelações mais proeminentes nas diferentes estações",
                                    "Mitologia por trás das constelações",
                                    "Como identificar padrões no céu",
                                    "Constelações do Zodíaco"
                                ],
                                "project": {
                                    "title": "Mapa de Constelações Favoritas",
                                    "description": "Criar um mapa ou modelo de suas constelações favoritas e contar suas histórias"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Navegadores Celestes",
                            "format": "Identificação de constelações e questionário",
                            "passing_score": 70,
                            "certificate": "Navegador Celeste Júnior"
                        }
                    },
                    {
                        "module_title": "Nosso Sistema Solar",
                        "module_description": "Explore os planetas, luas e outros objetos que compõem nosso sistema solar",
                        "estimated_time": "5 semanas",
                        "lessons": [
                            {
                                "lesson_title": "O Sol e Sua Família",
                                "objectives": "Compreender a estrutura do sistema solar e as características do Sol",
                                "steps": [
                                    "O Sol como estrela central",
                                    "Planetas rochosos vs. gigantes gasosos",
                                    "Cinturão de asteroides e objetos transnetunianos",
                                    "Formação do sistema solar"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são os oito planetas do Sistema Solar, em ordem a partir do Sol?",
                                        "type": "open",
                                        "answer": "Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno."
                                    }
                                ]
                            },
                            {
                                "lesson_title": "Explorando Marte",
                                "objectives": "Conhecer o planeta Marte e as missões que o exploraram",
                                "steps": [
                                    "Características físicas de Marte",
                                    "Missões robóticas: rovers e orbitadores",
                                    "Evidências de água e habitabilidade",
                                    "Desafios para exploração humana"
                                ],
                                "project": {
                                    "title": "Modelo de Base Marciana",
                                    "description": "Projetar e construir um modelo de uma possível base humana em Marte"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Maquete do Sistema Solar",
                            "description": "Criar uma maquete em escala do sistema solar, com informações sobre cada planeta",
                            "deliverables": ["Maquete física ou digital", "Cartões informativos sobre cada planeta"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Noite de Observação Astronômica",
                    "description": "Organizar uma pequena sessão de observação do céu para amigos ou família",
                    "requirements": [
                        "Preparar um roteiro de observação com pelo menos 5 objetos celestes",
                        "Criar materiais explicativos sobre os objetos a serem observados",
                        "Utilizar um instrumento óptico (binóculos ou pequeno telescópio) se disponível",
                        "Documentar a experiência com fotos ou desenhos"
                    ]
                }
            },
            "intermediario": {
                "description": "Aprofundamento em astronomia observacional e conceitos astrofísicos",
                "age_range": "13-16 anos",
                "modules": [
                    {
                        "module_title": "Astronomia Observacional",
                        "module_description": "Aprenda técnicas mais avançadas de observação do céu",
                        "lessons": [
                            {
                                "lesson_title": "Telescópios e Binóculos",
                                "objectives": "Compreender os diferentes tipos de instrumentos ópticos e seu uso",
                                "steps": [
                                    "Tipos de telescópios (refrator, refletor, catadióptrico)",
                                    "Características ópticas: abertura, distância focal, ampliação",
                                    "Montagens e apontamento",
                                    "Acessórios úteis para observação"
                                ]
                            },
                            {
                                "lesson_title": "Observando Objetos de Céu Profundo",
                                "objectives": "Aprender a localizar e observar nebulosas, aglomerados e galáxias",
                                "steps": [
                                    "Catálogo Messier e NGC",
                                    "Técnicas de visão periférica e adaptação ao escuro",
                                    "Desenho astronômico de observações",
                                    "Astrofotografia básica com smartphone"
                                ],
                                "project": {
                                    "title": "Álbum de Céu Profundo",
                                    "description": "Criar um álbum com observações ou fotografias de pelo menos 5 objetos de céu profundo"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Astrofísica Básica",
                        "module_description": "Entenda os princípios físicos que regem o comportamento dos astros",
                        "lessons": [
                            {
                                "lesson_title": "Ciclo de Vida das Estrelas",
                                "objectives": "Compreender como as estrelas nascem, evoluem e morrem",
                                "steps": [
                                    "Formação estelar em nebulosas",
                                    "Sequência principal e diagrama HR",
                                    "Gigantes vermelhas e anãs brancas",
                                    "Supernovas, estrelas de nêutrons e buracos negros"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Diagrama H-R Interativo",
                            "description": "Criar um diagrama Hertzsprung-Russell interativo que explique os diferentes tipos de estrelas"
                        }
                    }
                ]
            },
            "avancado": {
                "description": "Estudo aprofundado da cosmologia e física do universo",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Cosmologia Moderna",
                        "module_description": "Explore as teorias sobre a origem e evolução do universo",
                        "lessons": [
                            {
                                "lesson_title": "Big Bang e Expansão do Universo",
                                "objectives": "Compreender as evidências e teorias sobre a origem do universo",
                                "steps": [
                                    "Evidências do Big Bang: radiação cósmica de fundo, abundância de elementos",
                                    "Expansão do universo e lei de Hubble",
                                    "Matéria escura e energia escura",
                                    "Destino do universo: diferentes cenários"
                                ]
                            }
                        ]
                    },
                    {
                        "module_title": "Astronomia Computacional",
                        "module_description": "Use software e programação para analisar dados astronômicos",
                        "lessons": [
                            {
                                "lesson_title": "Análise de Dados Astronômicos",
                                "objectives": "Aprender a processar e analisar dados de observatórios",
                                "steps": [
                                    "Fontes de dados astronômicos abertos",
                                    "Análise básica usando Python ou planilhas",
                                    "Visualização de dados astronômicos",
                                    "Ciência cidadã em astronomia"
                                ],
                                "project": {
                                    "title": "Projeto de Ciência Cidadã",
                                    "description": "Participar de um projeto de ciência cidadã como Zooniverse e analisar os resultados"
                                }
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Pesquisa Astronômica Original",
                    "description": "Desenvolver um pequeno projeto de pesquisa astronômica usando dados reais",
                    "requirements": [
                        "Formular uma pergunta de pesquisa específica",
                        "Coletar dados relevantes de fontes abertas",
                        "Analisar os dados usando métodos apropriados",
                        "Apresentar os resultados em formato de artigo científico simplificado",
                        "Criar uma apresentação visual do projeto"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Astrofotografia",
                "description": "Técnicas e equipamentos para fotografar objetos celestes",
                "age_range": "14-17 anos",
                "modules": [
                    "Equipamentos para Astrofotografia",
                    "Fotografia Planetária",
                    "Fotografia de Céu Profundo",
                    "Processamento de Imagens Astronômicas"
                ]
            },
            {
                "name": "Exoplanetas e Astrobiologia",
                "description": "Estudo de planetas fora do sistema solar e possibilidade de vida extraterrestre",
                "age_range": "15-17 anos",
                "modules": [
                    "Métodos de Detecção de Exoplanetas",
                    "Zonas Habitáveis e Condições para Vida",
                    "Missões de Busca por Exoplanetas",
                    "Astrobiologia e Vida Extremófila"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Astrônomo",
                "Astrofísico",
                "Cientista Planetário",
                "Engenheiro Aeroespacial",
                "Divulgador Científico",
                "Técnico em Observatórios",
                "Analista de Dados Astronômicos"
            ],
            "day_in_life": [
                "Um astrônomo observa o céu usando telescópios, coleta e analisa dados celestes",
                "Um cientista planetário estuda a formação, estrutura e evolução dos planetas",
                "Um engenheiro aeroespacial projeta equipamentos para exploração espacial",
                "Um divulgador científico traduz descobertas astronômicas para o público geral"
            ]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Astronomia"] = astronomia_subarea
    area_ref.set(area_data)

    return area_data


def setup_exatas_estatistica_subarea(db):
    """
    Configura a subárea de Estatística dentro da área de Ciências Exatas e Aplicadas.
    """
    area_ref = db.collection("learning_paths").document("Ciências Exatas e Aplicadas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Ciências Exatas e Aplicadas",
            "description": "Área que engloba matemática, física, química, computação, engenharia e outras ciências exatas.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    estatistica_subarea = {
        "name": "Estatística",
        "description": "Aprenda a coletar, analisar e interpretar dados para extrair informações significativas e tomar decisões baseadas em evidências.",
        "estimated_time": "4-12 meses (dependendo da dedicação)",
        "icon": "chart-bar",
        "references": [
            {"title": "Khan Academy - Estatística", "url": "https://pt.khanacademy.org/math/statistics-probability"},
            {"title": "Estatística para Todos", "url": "https://www.estatisticaparatodos.com.br/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução à estatística descritiva e conceitos básicos de probabilidade",
                "age_range": "12-14 anos",
                "learning_outcomes": [
                    "Compreender e calcular medidas de tendência central (média, mediana, moda)",
                    "Interpretar diferentes formas de representação de dados",
                    "Aplicar conceitos de probabilidade em situações simples",
                    "Coletar e organizar dados de experimentos simples"
                ],
                "modules": [
                    {
                        "module_title": "Estatística no Dia a Dia",
                        "module_description": "Descubra como a estatística está presente em nosso cotidiano",
                        "estimated_time": "3 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Introdução à Estatística",
                                "objectives": "Compreender o que é estatística e sua importância",
                                "steps": [
                                    "O que é estatística e para que serve",
                                    "Onde encontramos estatística no dia a dia",
                                    "Diferença entre estatística e matemática comum",
                                    "Estatística descritiva vs. inferencial"
                                ],
                                "exercises": [
                                    {
                                        "question": "Cite três exemplos do uso de estatística que você encontra no seu dia a dia.",
                                        "type": "open",
                                        "answer": "Respostas possíveis: previsão do tempo, pesquisas eleitorais, estatísticas esportivas, notas escolares, etc."
                                    }
                                ],
                                "project": {
                                    "title": "Estatística ao Meu Redor",
                                    "description": "Criar um álbum de exemplos de estatística encontrados em jornais, revistas e internet",
                                    "estimated_time": "Uma semana"
                                }
                            },
                            {
                                "lesson_title": "Coletando e Organizando Dados",
                                "objectives": "Aprender a coletar dados e organizá-los de forma eficiente",
                                "steps": [
                                    "Métodos de coleta de dados",
                                    "Tabelas de frequência",
                                    "Dados qualitativos e quantitativos",
                                    "Amostragem básica"
                                ],
                                "project": {
                                    "title": "Minha Primeira Pesquisa",
                                    "description": "Realizar uma pequena pesquisa entre colegas sobre um tema de interesse e organizar os dados"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Fundamentos da Estatística",
                            "format": "Perguntas de múltipla escolha e problemas práticos",
                            "passing_score": 70,
                            "certificate": "Coletor de Dados Júnior"
                        }
                    },
                    {
                        "module_title": "Visualizando Dados",
                        "module_description": "Aprenda a criar e interpretar diferentes tipos de gráficos",
                        "estimated_time": "4 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Gráficos para Dados Categóricos",
                                "objectives": "Criar e interpretar gráficos para dados qualitativos",
                                "steps": [
                                    "Gráficos de barras e colunas",
                                    "Gráficos de setores (pizza)",
                                    "Pictogramas",
                                    "Escolhendo o gráfico adequado"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual tipo de gráfico seria mais adequado para mostrar a preferência dos alunos por diferentes esportes?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Gráfico de linhas",
                                            "Gráfico de barras",
                                            "Gráfico de dispersão",
                                            "Histograma"
                                        ],
                                        "correct_answer": 1
                                    }
                                ]
                            },
                            {
                                "lesson_title": "Gráficos para Dados Numéricos",
                                "objectives": "Criar e interpretar gráficos para dados quantitativos",
                                "steps": [
                                    "Histogramas",
                                    "Gráficos de linhas",
                                    "Box plots (diagramas de caixa)",
                                    "Gráficos de dispersão"
                                ],
                                "project": {
                                    "title": "Visualização de Dados Pessoais",
                                    "description": "Coletar dados pessoais durante uma semana (como horas de sono, tempo de estudo) e criar visualizações"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Infográfico Estatístico",
                            "description": "Criar um infográfico sobre um tema relevante usando diferentes tipos de gráficos",
                            "deliverables": ["Infográfico finalizado", "Dados brutos coletados", "Justificativa para escolha dos gráficos"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Mini Relatório Estatístico",
                    "description": "Desenvolver um pequeno projeto de pesquisa estatística sobre um tema de interesse",
                    "requirements": [
                        "Formulação de uma pergunta de pesquisa",
                        "Coleta de pelo menos 30 dados",
                        "Uso de pelo menos três tipos diferentes de visualização",
                        "Cálculo de medidas de tendência central e dispersão",
                        "Interpretação dos resultados"
                    ]
                }
            },
            "intermediario": {
                "description": "Estatística inferencial básica e análise de dados mais complexos",
                "age_range": "14-16 anos",
                "modules": [
                    {
                        "module_title": "Medidas Estatísticas",
                        "module_description": "Aprofunde-se nas medidas que descrevem conjuntos de dados",
                        "lessons": [
                            {
                                "lesson_title": "Medidas de Tendência Central",
                                "objectives": "Aprofundar o entendimento da média, mediana e moda",
                                "steps": [
                                    "Média aritmética, ponderada e geométrica",
                                    "Mediana e quartis",
                                    "Moda e distribuições multimodais",
                                    "Escolhendo a medida mais adequada"
                                ]
                            },
                            {
                                "lesson_title": "Medidas de Dispersão",
                                "objectives": "Compreender como quantificar a variabilidade dos dados",
                                "steps": [
                                    "Amplitude e intervalo interquartil",
                                    "Variância e desvio padrão",
                                    "Coeficiente de variação",
                                    "Interpretação das medidas de dispersão"
                                ],
                                "project": {
                                    "title": "Análise Comparativa",
                                    "description": "Comparar dois conjuntos de dados usando medidas de tendência central e dispersão"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Probabilidade Aplicada",
                        "module_description": "Explore conceitos de probabilidade e suas aplicações",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos de Probabilidade",
                                "objectives": "Compreender e aplicar conceitos básicos de probabilidade",
                                "steps": [
                                    "Eventos e espaço amostral",
                                    "Probabilidade clássica, frequentista e subjetiva",
                                    "Regras de adição e multiplicação",
                                    "Probabilidade condicional básica"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Simulação de Probabilidade",
                            "description": "Criar uma simulação para demonstrar um conceito de probabilidade (ex: problema de Monty Hall)"
                        }
                    }
                ]
            },
            "avancado": {
                "description": "Estatística inferencial avançada e introdução à ciência de dados",
                "age_range": "16-17 anos",
                "modules": [
                    {
                        "module_title": "Inferência Estatística",
                        "module_description": "Aprenda a tirar conclusões sobre populações a partir de amostras",
                        "lessons": [
                            {
                                "lesson_title": "Intervalos de Confiança",
                                "objectives": "Entender e calcular intervalos de confiança",
                                "steps": [
                                    "Conceito de intervalo de confiança",
                                    "Nível de confiança e margem de erro",
                                    "Cálculo para média populacional",
                                    "Interpretação correta dos intervalos"
                                ]
                            },
                            {
                                "lesson_title": "Testes de Hipóteses",
                                "objectives": "Aprender a formular e testar hipóteses estatísticas",
                                "steps": [
                                    "Formulação de hipóteses nula e alternativa",
                                    "Erros tipo I e tipo II",
                                    "Valor-p e significância estatística",
                                    "Testes para média e proporção"
                                ],
                                "project": {
                                    "title": "Testando uma Afirmação",
                                    "description": "Realizar um teste de hipótese sobre uma afirmação do cotidiano"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Introdução à Ciência de Dados",
                        "module_description": "Dê os primeiros passos no mundo da análise de dados",
                        "lessons": [
                            {
                                "lesson_title": "Análise Exploratória de Dados",
                                "objectives": "Aprender técnicas para explorar e entender conjuntos de dados",
                                "steps": [
                                    "Ciclo da análise de dados",
                                    "Limpeza e preparação de dados",
                                    "Detecção de padrões e anomalias",
                                    "Ferramentas para análise exploratória"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Projeto de Análise de Dados Reais",
                            "description": "Analisar um conjunto de dados abertos e extrair insights relevantes"
                        }
                    }
                ],
                "final_project": {
                    "title": "Pesquisa Estatística Completa",
                    "description": "Conduzir uma pesquisa estatística completa, desde a coleta até a análise inferencial",
                    "requirements": [
                        "Definição clara do problema de pesquisa",
                        "Planejamento de amostragem adequado",
                        "Coleta e limpeza de dados",
                        "Análise exploratória com visualizações",
                        "Aplicação de pelo menos um método inferencial",
                        "Relatório técnico com conclusões e limitações",
                        "Apresentação dos resultados para um público não técnico"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Estatística para Ciências Sociais",
                "description": "Aplicação de métodos estatísticos em pesquisas sociais, educacionais e comportamentais",
                "age_range": "15-17 anos",
                "modules": [
                    "Desenho de Pesquisa em Ciências Sociais",
                    "Análise de Questionários e Escalas",
                    "Amostragem em Populações Humanas",
                    "Estatística Não-Paramétrica"
                ]
            },
            {
                "name": "Data Science Junior",
                "description": "Introdução à ciência de dados para jovens, combinando estatística e programação",
                "age_range": "15-17 anos",
                "modules": [
                    "Programação com R ou Python para Análise de Dados",
                    "Visualização Avançada de Dados",
                    "Introdução ao Machine Learning",
                    "Projetos Práticos de Data Science"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Estatístico",
                "Cientista de Dados",
                "Analista de Business Intelligence",
                "Pesquisador Quantitativo",
                "Atuário",
                "Analista de Mercado",
                "Epidemiologista"
            ],
            "day_in_life": [
                "Um estatístico projeta pesquisas, coleta dados e aplica métodos estatísticos para resolver problemas",
                "Um cientista de dados utiliza programação e estatística para extrair insights de grandes conjuntos de dados",
                "Um atuário usa estatística para avaliar riscos financeiros em seguros e investimentos",
                "Um analista de mercado estuda tendências e padrões para orientar decisões empresariais"
            ]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Estatística"] = estatistica_subarea
    area_ref.set(area_data)

    return area_data

def setup_artes_desenho_subarea(db):
    """
    Configura a subárea de Desenho dentro da área de Artes e Expressão,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    desenho_subarea = {
        "name": "Desenho",
        "description": "Explore o mundo do desenho e desenvolva suas habilidades para expressar ideias, emoções e histórias através de linhas, formas e composições visuais.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "pencil-alt",
        "references": [
            {"title": "Curso de Desenho Online Gratuito", "url": "https://www.cursodedesenho.com.br/"},
            {"title": "Drawing for All", "url": "https://www.drawingforall.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos no mundo do desenho, aprendendo técnicas básicas e desenvolvendo coordenação olho-mão",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender elementos básicos do desenho: linha, forma, proporção e composição",
                    "Desenvolver coordenação motora fina e percepção visual",
                    "Criar desenhos simples a partir de observação e imaginação",
                    "Utilizar diferentes materiais de desenho e entender suas características"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos do Desenho",
                        "module_description": "Aprenda os elementos básicos que compõem qualquer desenho",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "médio",
                        "lessons": [
                            {
                                "lesson_title": "O Mundo das Linhas",
                                "objectives": "Compreender os diferentes tipos de linhas e como utilizá-las",
                                "estimated_time": "45 minutos",
                                "content_summary": "Exploração dos vários tipos de linhas e como elas criam diferentes sensações e formas",
                                "steps": [
                                    "Tipos de linhas: retas, curvas, orgânicas, geométricas",
                                    "Qualidades da linha: espessura, intensidade, velocidade",
                                    "Criação de texturas com diferentes linhas",
                                    "Expressividade através da linha"
                                ],
                                "exercises": [
                                    {
                                        "question": "Que emoções você consegue expressar apenas com linhas?",
                                        "type": "open",
                                        "suggested_time": "15 minutos",
                                        "answer": "Resposta pessoal. Os alunos podem mencionar raiva (linhas agressivas), calma (linhas fluidas), confusão (linhas entrelaçadas), etc."
                                    },
                                    {
                                        "question": "Qual é a diferença entre uma linha orgânica e uma linha geométrica?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "A linha orgânica é feita à mão livre enquanto a geométrica usa régua",
                                            "A linha orgânica possui curvas naturais e irregulares, enquanto a geométrica tem ângulos e curvas precisas",
                                            "A linha orgânica é mais grossa que a geométrica",
                                            "A linha orgânica só pode ser feita com lápis e a geométrica com caneta"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "exercício",
                                        "title": "Biblioteca de Linhas",
                                        "description": "Criar uma coleção de diferentes tipos de linhas em uma única folha para referência"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Expressividade da Linha na Arte",
                                     "url": "https://exemplo.com/video1"},
                                    {"type": "artigo", "title": "Como as Linhas Definem o Estilo",
                                     "url": "https://exemplo.com/artigo1"}
                                ]
                            },
                            {
                                "lesson_title": "Formas Básicas",
                                "objectives": "Entender como as formas fundamentais são a base de qualquer desenho",
                                "estimated_time": "50 minutos",
                                "steps": [
                                    "Formas geométricas básicas: círculo, quadrado, triângulo",
                                    "Simplificando objetos complexos em formas básicas",
                                    "Construção de desenhos a partir de formas simples",
                                    "Relações entre formas e espaço negativo"
                                ],
                                "exercises": [
                                    {
                                        "question": "Observe os objetos à sua volta. Identifique e desenhe três objetos decompostos em formas básicas.",
                                        "type": "open",
                                        "answer": "Resposta varia. Exemplos: Um telefone celular (retângulo), um copo (cilindro), uma cadeira (combinação de retângulos e cilindros)."
                                    }
                                ],
                                "project": {
                                    "title": "Monstros Geométricos",
                                    "description": "Criar personagens usando apenas formas geométricas básicas",
                                    "expected_outcome": "Compreender como objetos complexos podem ser construídos a partir de formas simples",
                                    "estimated_time": "30 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Desafio de Observação",
                            "format": "Desenho de um objeto simples com foco em linha e forma",
                            "passing_score": 60,
                            "time_limit": "30 minutos",
                            "certificate": "Desenhista Observador - Nível 1"
                        }
                    },
                    {
                        "module_title": "Materiais e Técnicas",
                        "module_description": "Explore diferentes materiais de desenho e aprenda técnicas básicas",
                        "estimated_time": "5 semanas",
                        "prerequisites": ["Fundamentos do Desenho"],
                        "lessons": [
                            {
                                "lesson_title": "Lápis e seus Segredos",
                                "objectives": "Conhecer os diferentes tipos de lápis e como utilizá-los",
                                "steps": [
                                    "Tipos de lápis: H, HB, B e suas diferenças",
                                    "Técnicas de sombreamento: hachura, tracejado, esfumado",
                                    "Controle de pressão e gradações de tom",
                                    "Cuidados com materiais e como apontar corretamente"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual lápis é mais indicado para desenhos suaves e sombreados?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "6H",
                                            "HB",
                                            "2B",
                                            "4H"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "project": {
                                    "title": "Escala de Cinza",
                                    "description": "Criar uma escala de tons de cinza do mais claro ao mais escuro usando diferentes lápis e pressões",
                                    "steps": [
                                        "Preparar papel dividido em 10 seções",
                                        "Aplicar gradualmente mais pressão ou lápis mais macios",
                                        "Comparar resultados com colegas",
                                        "Usar a escala como referência para outros desenhos"
                                    ],
                                    "estimated_time": "40 minutos"
                                }
                            },
                            {
                                "lesson_title": "Além do Lápis",
                                "objectives": "Explorar outros materiais de desenho e suas possibilidades",
                                "steps": [
                                    "Canetas: técnicas de pontilhismo e hachura",
                                    "Carvão: expressividade e contraste",
                                    "Giz de cera e giz pastel: cores e texturas",
                                    "Combinações de materiais em um mesmo desenho"
                                ],
                                "project": {
                                    "title": "Um Objeto, Três Materiais",
                                    "description": "Desenhar o mesmo objeto simples com três materiais diferentes para comparar resultados"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Natureza-morta Simples",
                            "description": "Criar um desenho de natureza-morta usando pelo menos dois materiais diferentes",
                            "deliverables": ["Desenho finalizado", "Esboços de planejamento", "Breve explicação das escolhas de materiais"],
                            "estimated_time": "3 horas (divididas em várias aulas)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Meu Mundo em Desenho",
                    "description": "Criar uma série de três desenhos relacionados a um tema pessoal",
                    "requirements": [
                        "Aplicação clara de conceitos de linha, forma e composição",
                        "Uso apropriado de pelo menos dois materiais diferentes",
                        "Demonstração de técnicas de sombreamento",
                        "Apresentação organizada dos trabalhos"
                    ],
                    "rubric": "Avaliação baseada em criatividade, aplicação técnica, esforço e progresso individual",
                    "showcase": "Miniexposição para colegas e familiares"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Desenho",
                    "format": "Desenho de observação com tema surpresa",
                    "passing_criteria": "Demonstração de compreensão dos conceitos básicos e técnicas aprendidas",
                    "certification": "Desenhista Iniciante"
                },
                "suggested_path_forward": ["Técnicas Intermediárias de Desenho", "Ilustração Digital"]
            },
            "intermediario": {
                "description": "Aprofundamento de técnicas de desenho e introdução a conceitos mais complexos",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Perspectiva e Profundidade",
                        "module_description": "Aprenda a criar a ilusão de tridimensionalidade em superfícies planas",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Introdução à Perspectiva",
                                "objectives": "Entender os princípios básicos da perspectiva no desenho",
                                "steps": [
                                    "Conceitos de linha do horizonte e pontos de fuga",
                                    "Perspectiva de um ponto (frontal)",
                                    "Perspectiva de dois pontos (angular)",
                                    "Desenho de objetos simples em perspectiva"
                                ]
                            },
                            {
                                "lesson_title": "Luz e Sombra",
                                "objectives": "Aprender como a luz cria volume e profundidade",
                                "steps": [
                                    "Identificação de fonte de luz e direção",
                                    "Sombras próprias e sombras projetadas",
                                    "Gradações de luz e técnicas de sombreamento avançadas",
                                    "Criação de atmosfera com luz e sombra"
                                ],
                                "project": {
                                    "title": "Estudo de Natureza-morta com Luz Dirigida",
                                    "description": "Criar um desenho de objetos iluminados por uma única fonte de luz forte"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Figura Humana Básica",
                        "module_description": "Aprenda os fundamentos do desenho da figura humana",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Proporções do Corpo Humano",
                                "objectives": "Compreender as relações entre as diferentes partes do corpo",
                                "steps": [
                                    "Cânones de proporção: a cabeça como unidade de medida",
                                    "Diferenças entre proporções de adultos, crianças e adolescentes",
                                    "Esquemas simplificados para construção da figura",
                                    "Análise de movimento e equilíbrio"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Personagem em Movimento",
                            "description": "Criar um personagem em diferentes poses de ação",
                            "deliverables": ["Estudos de poses", "Desenho final refinado", "Breve descrição do personagem"]
                        }
                    }
                ],
                "final_project": {
                    "title": "História Visual",
                    "description": "Criar uma narrativa visual de 5-10 quadros que conte uma história simples",
                    "requirements": [
                        "Personagens consistentes com proporções corretas",
                        "Cenários em perspectiva apropriada",
                        "Uso efetivo de luz e sombra para criar atmosfera",
                        "Sequência clara que comunique uma narrativa"
                    ]
                }
            },
            "avancado": {
                "description": "Técnicas avançadas de desenho e desenvolvimento de estilo pessoal",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Estilo e Expressão",
                        "module_description": "Desenvolva seu estilo pessoal e aprenda a expressar ideias através do desenho",
                        "lessons": [
                            {
                                "lesson_title": "Encontrando Seu Estilo",
                                "objectives": "Explorar diferentes estilos e técnicas para desenvolver uma voz visual própria",
                                "steps": [
                                    "Análise de estilos de artistas e ilustradores famosos",
                                    "Experimentos com diferentes abordagens técnicas",
                                    "Identificação de interesses e pontos fortes pessoais",
                                    "Desenvolvimento de uma série com unidade estilística"
                                ]
                            },
                            {
                                "lesson_title": "Desenho Conceitual",
                                "objectives": "Usar o desenho para comunicar ideias e conceitos abstratos",
                                "steps": [
                                    "Símbolos visuais e metáforas",
                                    "Simplificação e estilização para comunicação eficaz",
                                    "Storyboarding e pensamento narrativo",
                                    "Design thinking aplicado ao desenho"
                                ]
                            }
                        ]
                    }
                ],
                "final_project": {
                    "title": "Portfólio Pessoal",
                    "description": "Criar um portfólio coeso que demonstre habilidades técnicas e estilo pessoal",
                    "requirements": [
                        "Mínimo de 10 trabalhos que demonstrem diferentes habilidades",
                        "Unidade visual ou temática",
                        "Declaração de artista explicando abordagem e interesses",
                        "Apresentação profissional, física ou digital"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Ilustração",
                "description": "Focada na criação de imagens que contam histórias e comunicam ideias específicas",
                "age_range": "14-17 anos",
                "modules": [
                    "Narrativa Visual",
                    "Técnicas de Ilustração Editorial",
                    "Ilustração de Personagens",
                    "Ilustração de Ambientes"
                ],
                "final_project": {
                    "title": "Livro Ilustrado",
                    "description": "Criar uma série de ilustrações para uma história curta ou poema"
                }
            },
            {
                "name": "Desenho Anatômico",
                "description": "Estudo aprofundado da estrutura do corpo humano para desenho realista",
                "age_range": "15-17 anos",
                "modules": [
                    "Anatomia Artística Básica",
                    "Expressões Faciais e Emoções",
                    "Mãos e Pés",
                    "Anatomia em Movimento"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Ilustrador",
                "Artista de Conceito",
                "Animador",
                "Designer Gráfico",
                "Quadrinista",
                "Artista de Storyboard",
                "Professor de Arte"
            ],
            "day_in_life": [
                "Um ilustrador cria imagens para livros, revistas, anúncios e mídias digitais",
                "Um artista de conceito desenvolve designs visuais para filmes, jogos e animações",
                "Um designer gráfico combina imagens e texto para criar comunicação visual eficaz",
                "Um quadrinista narra histórias através de sequências de imagens"
            ],
            "educational_paths": [
                "Cursos técnicos em ilustração e design",
                "Graduação em Artes Visuais, Design ou áreas relacionadas",
                "Workshops especializados e cursos online",
                "Construção de portfólio pessoal e projetos autorais"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Arte básica"],
            "cross_curricular": ["História da Arte", "Literatura", "Tecnologia", "Comunicação"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Desenho"] = desenho_subarea
    area_ref.set(area_data)

    return area_data


def setup_artes_pintura_subarea(db):
    """
    Configura a subárea de Pintura dentro da área de Artes e Expressão.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    pintura_subarea = {
        "name": "Pintura",
        "description": "Descubra o maravilhoso mundo das cores e texturas através da pintura, explorando diferentes técnicas, materiais e estilos para expressar suas ideias e emoções.",
        "estimated_time": "4-12 meses (dependendo da dedicação)",
        "icon": "paint-brush",
        "references": [
            {"title": "Curso de Pintura Online", "url": "https://www.cursodepintura.com.br/"},
            {"title": "Art Is Fun - Painting Guides", "url": "https://www.art-is-fun.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiras explorações com cores e materiais básicos de pintura",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender a teoria básica das cores e suas relações",
                    "Aprender a preparar e utilizar diferentes materiais de pintura",
                    "Desenvolver técnicas básicas de aplicação de tinta",
                    "Criar composições simples usando cor e forma"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos da Cor",
                        "module_description": "Explore o mundo das cores e descubra como elas interagem",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "O Círculo Cromático",
                                "objectives": "Entender a organização das cores e suas relações básicas",
                                "estimated_time": "50 minutos",
                                "content_summary": "Exploração do círculo cromático, cores primárias, secundárias e terciárias, e como elas se relacionam",
                                "steps": [
                                    "Cores primárias: vermelho, azul e amarelo",
                                    "Criação de cores secundárias através de misturas",
                                    "Cores complementares e como se neutralizam",
                                    "Criação de um círculo cromático pessoal"
                                ],
                                "exercises": [
                                    {
                                        "question": "O que acontece quando misturamos amarelo e azul?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Laranja",
                                            "Verde",
                                            "Roxo",
                                            "Marrom"
                                        ],
                                        "correct_answer": 1
                                    },
                                    {
                                        "question": "Crie amostras de cores misturando as três cores primárias em diferentes proporções. Qual foi sua combinação favorita e por quê?",
                                        "type": "open",
                                        "suggested_time": "20 minutos",
                                        "answer": "Resposta pessoal, com reflexão sobre as combinações criadas."
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "experimento",
                                        "title": "Laboratório de Cores",
                                        "description": "Criar uma tabela de misturas mostrando o resultado de diferentes combinações de cores"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Teoria das Cores Explicada",
                                     "url": "https://exemplo.com/video_cores"},
                                    {"type": "artigo", "title": "Como as Cores Afetam Nossas Emoções",
                                     "url": "https://exemplo.com/artigo_cores"}
                                ]
                            },
                            {
                                "lesson_title": "Temperatura e Valor",
                                "objectives": "Compreender as qualidades de temperatura (quente/frio) e valor (claro/escuro) das cores",
                                "estimated_time": "45 minutos",
                                "steps": [
                                    "Distinção entre cores quentes e frias",
                                    "Como criar profundidade com temperatura de cor",
                                    "Escala de valores do claro ao escuro",
                                    "Criação de atmosfera com temperatura e valor"
                                ],
                                "exercises": [
                                    {
                                        "question": "Classifique estas cores como quentes ou frias: vermelho, azul-ciano, amarelo-ouro, roxo-azulado, laranja.",
                                        "type": "open",
                                        "answer": "Quentes: vermelho, amarelo-ouro, laranja. Frias: azul-ciano, roxo-azulado."
                                    }
                                ],
                                "project": {
                                    "title": "Paisagem em Temperatura",
                                    "description": "Criar duas versões miniatura da mesma paisagem, uma usando predominantemente cores quentes e outra com cores frias",
                                    "expected_outcome": "Compreensão de como a temperatura de cor afeta a sensação e atmosfera de uma imagem",
                                    "estimated_time": "30 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Desafio de Cores",
                            "format": "Criação de uma composição abstrata usando princípios específicos de cor",
                            "passing_score": 70,
                            "time_limit": "60 minutos",
                            "certificate": "Explorador de Cores - Nível 1"
                        }
                    },
                    {
                        "module_title": "Materiais e Técnicas Básicas",
                        "module_description": "Descubra diferentes materiais de pintura e como utilizá-los",
                        "estimated_time": "6 semanas",
                        "prerequisites": ["Fundamentos da Cor"],
                        "lessons": [
                            {
                                "lesson_title": "Aquarela para Iniciantes",
                                "objectives": "Aprender técnicas básicas de pintura com aquarela",
                                "steps": [
                                    "Preparação de materiais: papéis, pincéis e tintas",
                                    "Técnicas de aquarela: aguada, molhado sobre molhado, molhado sobre seco",
                                    "Transparência e camadas",
                                    "Efeitos especiais: sal, álcool, plástico"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual técnica de aquarela é melhor para criar gradientes suaves?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Molhado sobre molhado",
                                            "Molhado sobre seco",
                                            "Pontilhismo",
                                            "Dry brush"
                                        ],
                                        "correct_answer": 0
                                    }
                                ],
                                "project": {
                                    "title": "Cartões em Aquarela",
                                    "description": "Criar pequenos cartões usando diferentes técnicas de aquarela aprendidas",
                                    "steps": [
                                        "Esboçar ideias simples em lápis",
                                        "Aplicar técnicas diferentes em cada cartão",
                                        "Adicionar detalhes quando secar",
                                        "Compartilhar e explicar as técnicas para colegas"
                                    ],
                                    "estimated_time": "60 minutos"
                                }
                            },
                            {
                                "lesson_title": "Guache e Acrílica",
                                "objectives": "Explorar tintas opacas e suas possibilidades",
                                "steps": [
                                    "Diferenças entre guache e acrílica",
                                    "Técnicas de aplicação: pinceladas, camadas, texturas",
                                    "Misturando cores em tintas opacas",
                                    "Pintura em diferentes superfícies"
                                ],
                                "project": {
                                    "title": "Pintura em Objeto",
                                    "description": "Criar uma pintura em um objeto tridimensional simples (caixa, vaso, pedra)"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Natureza em Três Técnicas",
                            "description": "Criar três pinturas do mesmo tema natural usando aquarela, guache e acrílica",
                            "deliverables": ["Três pinturas finalizadas", "Anotações sobre as diferenças percebidas entre as técnicas", "Apresentação oral de 2 minutos"],
                            "estimated_time": "4 horas (divididas em várias aulas)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Meu Lugar Favorito",
                    "description": "Criar uma pintura de um lugar especial usando a técnica e materiais de sua preferência",
                    "requirements": [
                        "Uso consciente de princípios de cor",
                        "Aplicação adequada da técnica escolhida",
                        "Esboços preparatórios e planejamento",
                        "Reflexão escrita sobre o processo e escolhas"
                    ],
                    "rubric": "Avaliação baseada em experimentação, aplicação de conceitos, esforço e crescimento individual",
                    "showcase": "Exposição coletiva com visitação aberta"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos da Pintura",
                    "format": "Pintura de tema livre com restrições técnicas específicas",
                    "passing_criteria": "Demonstração de compreensão dos conceitos de cor e técnicas básicas",
                    "certification": "Pintor Iniciante"
                },
                "suggested_path_forward": ["Técnicas Intermediárias de Pintura", "Pintura Digital", "Artes Mistas"]
            },
            "intermediario": {
                "description": "Aprofundamento das técnicas de pintura e introdução à composição avançada",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Composição e Planejamento",
                        "module_description": "Aprenda a criar pinturas bem estruturadas e visualmente equilibradas",
                        "estimated_time": "5 semanas",
                        "lessons": [
                            {
        "lesson_title": "Princípios de Composição",
        "objectives": "Compreender regras e estratégias para organizar elementos visuais",
        "steps": [
            "Regra dos terços e proporção áurea",
            "Equilíbrio, ritmo e movimento",
            "Ponto focal e hierarquia visual",
            "Planejamento com thumbnails e estudos"
        ],
        "project": {
            "title": "Reformulação Compositiva",
            "description": "Analisar e redesenhar a composição de uma obra famosa usando princípios diferentes"
        }

    },
    {
    "lesson_title": "Paletas de Cores",
    "objectives": "Aprender a criar e utilizar paletas de cores harmônicas",
    "steps": [
        "Harmonias de cores: complementar, análoga, triádica",
        "Paletas limitadas e suas vantagens",
        "Criação de atmosfera com temperatura e saturação",
        "Uso de cores dominantes, secundárias e de acento"
    ],
    "project": {
        "title": "Paisagem em Quatro Estações",
        "description": "Criar quatro versões da mesma paisagem usando paletas que representem as estações do ano"
    }

}
]
},
{
    "module_title": "Pintura de Observação",
    "module_description": "Desenvolva sua capacidade de observar e representar o mundo visível",
    "estimated_time": "7 semanas",
    "lessons": [
        {
"lesson_title": "Luz e Sombra em Cores",
"objectives": "Compreender como representar volume e profundidade através da cor",
"steps": [
    "Observação de valores em objetos coloridos",
    "Sombras coloridas vs. sombras neutras",
    "Influência da luz ambiente na cor dos objetos",
    "Técnicas de modelagem tridimensional com cor"
]
},
{
"lesson_title": "Natureza-Morta Expressiva",
"objectives": "Ir além da representação literal para capturar a essência dos objetos",
"steps": [
    "Observação profunda vs. representação mecânica",
    "Simplificação e exagero de características",
    "Uso da pincelada como elemento expressivo",
    "Experimentação com perspectivas não convencionais"
],
"project": {
    "title": "Objetos Cotidianos Reinventados",
    "description": "Criar uma série de pinturas de objetos comuns com abordagem expressiva"
}
}
],
"module_project": {
    "title": "Interiores e Exteriores",
    "description": "Criar duas pinturas relacionadas: um espaço interior e uma cena exterior",
    "deliverables": ["Duas pinturas finalizadas", "Estudos preparatórios", "Breve análise comparativa das experiências"]
}
}
],
"final_project": {
    "title": "Narrativa Visual",
    "description": "Criar um díptico ou tríptico que conte uma história ou explore um tema pessoal",
    "requirements": [
        "Unidade compositiva e cromática entre as peças",
        "Desenvolvimento claro de uma ideia ou narrativa",
        "Utilização consciente de técnicas de pintura",
        "Declaração de artista explicando intenções e processo"
    ]
}
},
"avancado": {
    "description": "Desenvolvimento de estilo pessoal e abordagens conceituais à pintura",
    "age_range": "14-17 anos",
    "modules": [
        {
            "module_title": "Explorações Estilísticas",
            "module_description": "Experimente diferentes estilos históricos para encontrar sua voz pessoal",
            "lessons": [
                {
                    "lesson_title": "Do Realismo à Abstração",
                    "objectives": "Compreender o espectro de representação na pintura",
                    "steps": [
                        "Análise de estilos históricos e contemporâneos",
                        "Técnicas de simplificação e estilização",
                        "Pintura abstrata a partir de referências concretas",
                        "Encontrando seu lugar no espectro"
                    ]
                    },
                    {
                    "lesson_title": "Influências e Apropriação",
                    "objectives": "Aprender como artistas inspiram-se mutuamente e como desenvolver sua voz única",
                    "steps": [
                        "Estudo de influências entre artistas famosos",
                        "Diferença entre inspiração, homenagem e plágio",
                        "Técnicas para transformar influências em expressão pessoal",
                        "Criação de obra inspirada por artista admirado"
                    ],
                    "project": {
                        "title": "À Maneira De...",
                        "description": "Criar uma pintura explorando o estilo de um artista admirado, mas com tema e abordagem pessoal"
                    }
                    }
                    ]
                    },
                    {
                        "module_title": "Pintura Conceitual e Contemporânea",
                        "module_description": "Explore a pintura como meio de expressão de ideias complexas",
                        "lessons": [
                            {
                    "lesson_title": "Além da Tela",
                    "objectives": "Expandir noções tradicionais de pintura para novas dimensões",
                    "steps": [
                        "Pintura em suportes não convencionais",
                        "Instalações e obras tridimensionais com pintura",
                        "Combinação de pintura com outros meios",
                        "Performance e processo como parte da obra"
                    ]
                    }
                    ],
                    "module_project": {
                        "title": "Intervenção Pictórica",
                        "description": "Criar um projeto de pintura que interaja com um espaço específico ou objeto não convencional"
                    }
                    }
                    ],
                    "final_project": {
                        "title": "Exposição Individual",
                        "description": "Desenvolver uma série coesa de pinturas para uma pequena exposição individual",
                        "requirements": [
                            "Mínimo de 5 obras relacionadas conceitualmente",
                            "Desenvolvimento de identidade visual e estilo reconhecível",
                            "Texto curatorial e título para a exposição",
                            "Organização e montagem da exposição para público"
                        ]
                    }
                    }
                    },
                    "specializations": [
                        {
                            "name": "Pintura Digital",
                            "description": "Aplicação de princípios de pintura usando meios digitais",
                            "age_range": "12-17 anos",
                            "modules": [
                                "Fundamentos de Pintura Digital",
                                "Concept Art para Personagens e Cenários",
                                "Técnicas de Iluminação Digital",
                                "Design Visual para Jogos e Animação"
                            ],
                            "final_project": {
                                "title": "Portfólio Digital",
                                "description": "Criar um conjunto de pinturas digitais para um projeto fictício de mídia"
                            }
                        },
                        {
                            "name": "Pintura em Técnicas Tradicionais",
                            "description": "Domínio de materiais clássicos como óleo, têmpera e afresco",
                            "age_range": "14-17 anos",
                            "modules": [
                                "Introdução à Pintura a Óleo",
                                "Técnicas de Velatura e Glazing",
                                "Preparação de Suportes e Materiais",
                                "Restauração e Conservação Básica"
                            ]
                        }
                    ],
                    "career_exploration": {
                        "related_careers": [
                            "Artista Plástico",
                            "Ilustrador",
                            "Muralista",
                            "Restaurador de Arte",
                            "Cenógrafo",
                            "Designer de Conceito",
                            "Professor de Artes"
                        ],
                        "day_in_life": [
                            "Um artista plástico divide seu tempo entre criação em estúdio, pesquisa e contato com galerias",
                            "Um ilustrador editorial cria imagens para publicações com prazos definidos",
                            "Um muralista trabalha em grande escala, adaptando-se a espaços públicos",
                            "Um restaurador combina conhecimento artístico e científico para preservar obras"
                        ],
                        "educational_paths": [
                            "Bacharelado em Artes Visuais",
                            "Cursos técnicos em ilustração e pintura",
                            "Residências artísticas e workshops especializados",
                            "Desenvolvimento de portfólio independente"
                        ]
                    },
                    "meta": {
                        "age_appropriate": True,
                        "school_aligned": True,
                        "prerequisite_subjects": ["Desenho básico", "Teoria da cor"],
                        "cross_curricular": ["História da Arte", "Química (materiais)", "Psicologia (expressão emocional)"]
                    }
    }
    area_data["subareas"]["Pintura"] = pintura_subarea
    area_ref.set(area_data)
    return area_data


def setup_artes_fotografia_subarea(db):
    """
    Configura a subárea de Fotografia dentro da área de Artes e Expressão.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    fotografia_subarea = {
        "name": "Fotografia",
        "description": "Aprenda a capturar momentos, contar histórias e expressar sua visão única do mundo através das lentes da fotografia.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "camera",
        "references": [
            {"title": "Escola de Fotografia", "url": "https://www.escoladefotografia.com.br/"},
            {"title": "Digital Photography School", "url": "https://digital-photography-school.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução ao mundo da fotografia e aos princípios básicos da imagem",
                "age_range": "11-14 anos",
                "learning_outcomes": [
                    "Compreender o funcionamento básico de uma câmera e seus componentes",
                    "Aplicar princípios de composição para criar imagens visualmente interessantes",
                    "Reconhecer a importância da luz na fotografia",
                    "Desenvolver olhar crítico para análise de imagens fotográficas"
                ],
                "modules": [
                    {
                        "module_title": "A Câmera e Seus Segredos",
                        "module_description": "Descubra como funciona uma câmera e como tirar suas primeiras fotos",
                        "estimated_time": "3 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Conhecendo a Câmera",
                                "objectives": "Entender os componentes básicos e funcionalidades de uma câmera",
                                "estimated_time": "45 minutos",
                                "content_summary": "Introdução às partes essenciais de uma câmera e como elas trabalham juntas para criar uma imagem",
                                "steps": [
                                    "Tipos de câmeras: DSLR, mirrorless, compacta, smartphone",
                                    "Componentes principais: lente, sensor, visor, botões de controle",
                                    "Funcionamento básico da captura de imagem",
                                    "Cuidados e manutenção do equipamento"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual é a função da lente em uma câmera?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas proteger o sensor",
                                            "Capturar a luz e formar a imagem",
                                            "Servir como visor para o fotógrafo",
                                            "Armazenar as fotos digitalmente"
                                        ],
                                        "correct_answer": 1
                                    },
                                    {
                                        "question": "Identifique e nomeie pelo menos cinco partes da sua câmera (ou smartphone) e explique para que servem.",
                                        "type": "open",
                                        "suggested_time": "15 minutos",
                                        "answer": "Resposta varia. Exemplos: lente (foca a luz), botão do obturador (tira a foto), visor/tela (enquadra a imagem), cartão de memória (armazena as fotos), botões de controle (ajustam configurações)."
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "atividade prática",
                                        "title": "Explorando sua Câmera",
                                        "description": "Em pares, explorar as funcionalidades de diferentes câmeras e smartphones"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Anatomia de uma Câmera",
                                     "url": "https://exemplo.com/video_camera"},
                                    {"type": "infográfico", "title": "Partes da Câmera para Iniciantes",
                                     "url": "https://exemplo.com/infografico_camera"}
                                ]
                            },
                            {
                                "lesson_title": "Primeiros Cliques",
                                "objectives": "Aprender a tirar suas primeiras fotos com controle básico",
                                "estimated_time": "60 minutos",
                                "steps": [
                                    "Como segurar a câmera corretamente",
                                    "Enquadramento e foco",
                                    "Estabilização para evitar fotos tremidas",
                                    "Modo automático vs. modos semiautomáticos"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que é importante apoiar bem a câmera ao fotografar?",
                                        "type": "open",
                                        "answer": "Para evitar trepidação (fotos tremidas), especialmente em condições de pouca luz ou quando usando zoom."
                                    }
                                ],
                                "project": {
                                    "title": "Álbum de Primeiros Passos",
                                    "description": "Tirar 20 fotos de temas livres, experimentando diferentes enquadramentos",
                                    "expected_outcome": "Familiarização com o processo básico de captura de imagens",
                                    "estimated_time": "Tarefa para casa - 1 semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Fundamentos da Câmera",
                            "format": "Teste de múltipla escolha + demonstração prática",
                            "passing_score": 70,
                            "time_limit": "30 minutos",
                            "certificate": "Fotógrafo Iniciante - Nível 1"
                        }
                    },
                    {
                        "module_title": "O Olhar Fotográfico",
                        "module_description": "Desenvolva sua percepção visual e aprenda a compor imagens interessantes",
                        "estimated_time": "5 semanas",
                        "prerequisites": ["A Câmera e Seus Segredos"],
                        "lessons": [
                            {
                                "lesson_title": "Princípios de Composição",
                                "objectives": "Aprender regras básicas para organizar elementos na fotografia",
                                "steps": [
                                    "Regra dos terços e grade de composição",
                                    "Equilíbrio e proporção",
                                    "Linhas de direção e movimento",
                                    "Enquadramento e espaço negativo"
                                ],
                                "exercises": [
                                    {
                                        "question": "O que acontece quando posicionamos o elemento principal na intersecção das linhas da regra dos terços?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "A foto fica sempre desequilibrada",
                                            "O elemento principal fica muito pequeno",
                                            "Criamos mais interesse visual e dinamismo",
                                            "A foto fica tecnicamente incorreta"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "project": {
                                    "title": "Variações Compositivas",
                                    "description": "Fotografar o mesmo objeto/cena usando pelo menos três princípios de composição diferentes",
                                    "steps": [
                                        "Escolher um objeto ou cena interessante",
                                        "Planejar diferentes abordagens compositivas",
                                        "Fotografar aplicando cada princípio",
                                        "Comparar resultados e avaliar impacto visual"
                                    ],
                                    "estimated_time": "60 minutos"
                                }
                            },
                            {
                                "lesson_title": "A Luz na Fotografia",
                                "objectives": "Entender como a luz afeta a aparência e o clima da fotografia",
                                "steps": [
                                    "Tipos de luz: dura vs. suave, quente vs. fria",
                                    "Direção da luz: frontal, lateral, contraluz",
                                    "Hora dourada e hora azul",
                                    "Sombras como elemento compositivo"
                                ],
                                "project": {
                                    "title": "Estudo de Luz",
                                    "description": "Fotografar o mesmo objeto/pessoa em diferentes condições de luz ao longo do dia"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "História em 5 Fotos",
                            "description": "Criar uma narrativa visual usando cinco fotografias que contem uma história simples",
                            "deliverables": ["Cinco fotos impressas ou digitais", "Breve explicação da narrativa",
                                             "Apresentação oral"],
                            "estimated_time": "2 semanas (incluindo planejamento e execução)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Exposição Fotográfica 'Meu Olhar'",
                    "description": "Criar um conjunto de fotografias que representem sua visão pessoal sobre um tema de sua escolha",
                    "requirements": [
                        "Série de 7-10 fotografias coesas sobre um tema",
                        "Aplicação consciente de princípios de composição",
                        "Atenção à qualidade da luz nas imagens",
                        "Texto curto explicando sua abordagem e intenções",
                        "Participação na montagem de exposição coletiva"
                    ],
                    "rubric": "Avaliação baseada em criatividade, domínio técnico básico, coerência temática e evolução individual",
                    "showcase": "Exposição física ou virtual para comunidade escolar"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos da Fotografia",
                    "format": "Portfólio + teste escrito sobre conceitos básicos",
                    "passing_criteria": "70% no teste e portfólio que demonstre aplicação dos conceitos",
                    "certification": "Fotógrafo Iniciante"
                },
                "suggested_path_forward": ["Técnicas Fotográficas Intermediárias", "Fotografia Digital",
                                           "Edição de Imagens"]
            },
            "intermediario": {
                "description": "Aprofundamento técnico e desenvolvimento de projetos fotográficos mais complexos",
                "age_range": "13-16 anos",
                "modules": [
                    {
                        "module_title": "Controle Manual da Câmera",
                        "module_description": "Aprenda a usar configurações manuais para ter mais controle criativo",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "O Triângulo da Exposição",
                                "objectives": "Compreender a relação entre abertura, velocidade e ISO",
                                "steps": [
                                    "Abertura: profundidade de campo e bokeh",
                                    "Velocidade do obturador: congelamento e movimento",
                                    "ISO: sensibilidade e ruído",
                                    "Balanceamento para exposição correta"
                                ]
                            },
                            {
                                "lesson_title": "Modos de Disparo e Medição",
                                "objectives": "Aprender a utilizar diferentes modos da câmera para situações específicas",
                                "steps": [
                                    "Modos P, A/Av, S/Tv e Manual",
                                    "Sistemas de medição: matricial, pontual, ponderada ao centro",
                                    "Compensação de exposição",
                                    "Bracketing e HDR básico"
                                ],
                                "project": {
                                    "title": "Série Técnica",
                                    "description": "Criar um conjunto de fotos que demonstrem o domínio de diferentes configurações manuais"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Gêneros Fotográficos",
                        "module_description": "Explore diferentes tipos de fotografia e suas técnicas específicas",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Retrato",
                                "objectives": "Aprender técnicas básicas para fotografar pessoas",
                                "steps": [
                                    "Poses e direção de modelos",
                                    "Iluminação para retratos",
                                    "Capturando expressões e emoções",
                                    "Retratos ambientais vs. retratos formais"
                                ]
                            },
                            {
                                "lesson_title": "Fotografia de Paisagem",
                                "objectives": "Capturar a grandeza e beleza de cenários naturais e urbanos",
                                "steps": [
                                    "Composição em paisagens: regra dos terços, linhas, camadas",
                                    "Uso de filtros: polarizador, ND, graduado",
                                    "Hiperfocal e maximização da nitidez",
                                    "Planejamento: horário, luz, condições climáticas"
                                ],
                                "project": {
                                    "title": "Série de Paisagens Locais",
                                    "description": "Criar um conjunto de fotografias que mostrem lugares da região sob uma nova perspectiva"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Explorando Gêneros",
                            "description": "Desenvolver um projeto que combine elementos de pelo menos dois gêneros fotográficos",
                            "deliverables": ["Série fotográfica de 10-15 imagens", "Texto explicativo do conceito",
                                             "Apresentação das técnicas utilizadas"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Fotográfico Autoral",
                    "description": "Desenvolver um ensaio fotográfico sobre um tema social, cultural ou pessoal relevante",
                    "requirements": [
                        "Série coesa de 15-20 fotografias",
                        "Domínio técnico das configurações da câmera",
                        "Estilo visual consistente",
                        "Statement de artista explicando conceito e processo"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de linguagem pessoal e projetos fotográficos autorais",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Iluminação Avançada",
                        "module_description": "Aprenda a controlar e moldar a luz para resultados profissionais",
                        "lessons": [
                            {
                                "lesson_title": "Flash e Iluminação Artificial",
                                "objectives": "Dominar o uso de flash e esquemas de iluminação em estúdio",
                                "steps": [
                                    "TTL vs. Manual: controle de potência do flash",
                                    "Modificadores de luz: softbox, umbrella, refletores",
                                    "Esquemas básicos de iluminação: principal, preenchimento, contraluz",
                                    "Flash remoto e sincronização"
                                ]
                            },
                            {
                                "lesson_title": "Luz Encontrada e Mista",
                                "objectives": "Trabalhar criativamente com iluminação disponível e mista",
                                "steps": [
                                    "Identificação e aproveitamento de fontes de luz existentes",
                                    "Técnicas de baixa luminosidade",
                                    "Balanceamento de luz natural e artificial",
                                    "Criação de mood através da luz"
                                ],
                                "project": {
                                    "title": "Atmosfera Luminosa",
                                    "description": "Criar uma série fotográfica que explore diferentes atmosferas através da luz"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Fotografia Conceitual",
                        "module_description": "Explore a fotografia como meio de expressão de ideias complexas",
                        "lessons": [
                            {
                                "lesson_title": "Da Ideia à Imagem",
                                "objectives": "Desenvolver conceitos e traduzi-los em imagens fotográficas",
                                "steps": [
                                    "Brainstorming e desenvolvimento de conceitos",
                                    "Storyboarding e planejamento visual",
                                    "Fotografia encenada e direção de cena",
                                    "Simbolismo e metáfora visual"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Manifesto Visual",
                            "description": "Criar um ensaio fotográfico que expresse uma posição sobre uma questão social ou cultural"
                        }
                    }
                ],
                "final_project": {
                    "title": "Exposição Individual",
                    "description": "Desenvolver um corpo de trabalho autoral para uma exposição ou publicação",
                    "requirements": [
                        "Série de 20-30 fotografias com forte coesão conceitual e estética",
                        "Textos complementares (statement, títulos, legendas)",
                        "Planejamento completo de exposição (montagem, sequência, tamanhos)",
                        "Estratégia de divulgação (release, convites, redes sociais)"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Fotojornalismo",
                "description": "Documentação fotográfica de eventos, questões sociais e notícias",
                "age_range": "14-17 anos",
                "modules": [
                    "Ética no Fotojornalismo",
                    "Fotografia Documental",
                    "Cobertura de Eventos",
                    "Narrativas Visuais e Ensaios Fotográficos"
                ],
                "final_project": {
                    "title": "Reportagem Visual",
                    "description": "Produzir uma reportagem fotográfica sobre um tema relevante da comunidade local"
                }
            },
            {
                "name": "Fotografia Comercial",
                "description": "Técnicas específicas para fotografia de produtos, publicidade e moda",
                "age_range": "15-17 anos",
                "modules": [
                    "Fotografia de Produto e Still Life",
                    "Iluminação para Publicidade",
                    "Fotografia de Moda e Beleza",
                    "Marketing e Portfólio Comercial"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Fotógrafo de Eventos",
                "Fotojornalista",
                "Fotógrafo de Publicidade",
                "Fotógrafo de Moda",
                "Artista Visual",
                "Editor de Imagens",
                "Diretor de Fotografia (cinema)"
            ],
            "day_in_life": [
                "Um fotógrafo de eventos captura momentos importantes em casamentos, formaturas e festas",
                "Um fotojornalista documenta acontecimentos e conta histórias através de imagens",
                "Um fotógrafo comercial cria imagens para marcas, produtos e campanhas",
                "Um fotógrafo de natureza viaja para documentar paisagens e vida selvagem"
            ],
            "educational_paths": [
                "Graduação em Fotografia ou Artes Visuais",
                "Cursos técnicos especializados",
                "Assistência a fotógrafos profissionais",
                "Workshops e educação continuada",
                "Desenvolvimento de portfólio independente"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Artes visuais básicas"],
            "cross_curricular": ["História", "Geografia", "Sociologia", "Ciências", "Tecnologia"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Fotografia"] = fotografia_subarea
    area_ref.set(area_data)

    return area_data


def setup_artes_teatro_subarea(db):
    """
    Configura a subárea de Teatro dentro da área de Artes e Expressão,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    teatro_subarea = {
        "name": "Teatro",
        "description": "Explore o mundo mágico do teatro, desenvolvendo expressão corporal, oratória, criatividade e trabalho em equipe através da arte de interpretar e contar histórias no palco.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "theater-masks",
        "references": [
            {"title": "Portal do Teatro", "url": "https://www.portaldoteatro.com.br/"},
            {"title": "Drama Resource", "url": "https://www.dramaresource.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos no mundo do teatro, com jogos teatrais e desenvolvimento de expressividade",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Desenvolver consciência corporal e expressão vocal",
                    "Aprender a trabalhar colaborativamente em grupo",
                    "Explorar a criatividade através de jogos e improvisações",
                    "Compreender os elementos básicos da linguagem teatral"
                ],
                "modules": [
                    {
                        "module_title": "Jogos Teatrais",
                        "module_description": "Desperte sua expressividade e criatividade através de jogos e atividades lúdicas",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "muito alto",
                        "lessons": [
                            {
                                "lesson_title": "Descobrindo o Corpo Expressivo",
                                "objectives": "Desenvolver consciência corporal e aprender a se expressar através do movimento",
                                "estimated_time": "60 minutos",
                                "content_summary": "Exploração das possibilidades expressivas do corpo através de jogos e exercícios",
                                "steps": [
                                    "Aquecimento e alongamento para preparação corporal",
                                    "Jogos de espelho e imitação",
                                    "Expressão de emoções através de posturas e gestos",
                                    "Criação de imagens corporais individuais e coletivas"
                                ],
                                "exercises": [
                                    {
                                        "question": "Como você pode expressar 'alegria' apenas com seu corpo, sem usar palavras?",
                                        "type": "open",
                                        "suggested_time": "15 minutos",
                                        "answer": "Resposta pessoal. Podem mencionar postura ereta, braços abertos, movimento ascendente, saltos, sorriso, etc."
                                    },
                                    {
                                        "question": "Por que é importante fazer um aquecimento corporal antes das atividades teatrais?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas para seguir a tradição teatral",
                                            "Para prevenir lesões e preparar o corpo para a expressão",
                                            "Só é necessário para dança, não para teatro",
                                            "Para impressionar os espectadores"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "jogo",
                                        "title": "Escultura Humana",
                                        "description": "Em duplas, um 'esculpe' o corpo do outro para representar uma emoção ou personagem"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Exercícios de Expressão Corporal",
                                     "url": "https://exemplo.com/video_expressao"},
                                    {"type": "artigo", "title": "A Importância do Corpo no Teatro",
                                     "url": "https://exemplo.com/artigo_corpo"}
                                ]
                            },
                            {
                                "lesson_title": "A Voz em Cena",
                                "objectives": "Explorar as possibilidades da voz como instrumento de expressão",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "Respiração e apoio vocal",
                                    "Articulação e dicção",
                                    "Variações de volume, tom e ritmo",
                                    "Criação de personagens usando a voz"
                                ],
                                "exercises": [
                                    {
                                        "question": "Pratique dizer a frase 'O rato roeu a roupa do rei de Roma' de três maneiras diferentes: como alguém muito tímido, como alguém muito irritado e como um apresentador de jornal. Qual foi a diferença na sua voz em cada caso?",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Devem identificar mudanças em volume, velocidade, tom, ênfase em diferentes palavras, etc."
                                    }
                                ],
                                "project": {
                                    "title": "Rádio Teatro",
                                    "description": "Criar uma pequena narrativa usando apenas efeitos vocais e sonoros",
                                    "expected_outcome": "Compreensão do poder expressivo da voz",
                                    "estimated_time": "30 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Mostra de Jogos Teatrais",
                            "format": "Apresentação de jogos aprendidos para os colegas",
                            "passing_score": "Participação ativa e engajamento",
                            "time_limit": "45 minutos",
                            "certificate": "Jogador Teatral - Nível 1"
                        }
                    },
                    {
                        "module_title": "Improvisação",
                        "module_description": "Aprenda a criar cenas e histórias no momento, desenvolvendo criatividade e espontaneidade",
                        "estimated_time": "5 semanas",
                        "prerequisites": ["Jogos Teatrais"],
                        "lessons": [
                            {
                                "lesson_title": "Bases da Improvisação",
                                "objectives": "Aprender os princípios fundamentais para improvisar cenas",
                                "steps": [
                                    "Aceitação e 'sim, e...'",
                                    "Escuta ativa e resposta ao parceiro",
                                    "Estabelecimento de quem, onde e o quê da cena",
                                    "Confiança e superação do medo de errar"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual é o princípio do 'sim, e...' na improvisação?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Dizer sim a tudo que for proposto pelo diretor",
                                            "Aceitar a proposta do parceiro e adicionar algo à cena",
                                            "Sempre dar um final feliz às histórias",
                                            "Evitar conflitos nas cenas"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Cenas a partir de Objetos",
                                    "description": "Improvisar cenas curtas usando objetos aleatórios como inspiração",
                                    "steps": [
                                        "Selecionar objetos variados",
                                        "Formar duplas ou pequenos grupos",
                                        "Integrar o objeto de forma criativa na cena",
                                        "Apresentar para os colegas e receber feedback"
                                    ],
                                    "estimated_time": "45 minutos"
                                }
                            },
                            {
                                "lesson_title": "Construção de Personagens Instantâneos",
                                "objectives": "Desenvolver habilidade de criar e incorporar personagens rapidamente",
                                "steps": [
                                    "Observação e inspiração no cotidiano",
                                    "Transformação física: postura, andar, gestos",
                                    "Criação de vozes e maneirismos",
                                    "Resposta emocional e objetivos do personagem"
                                ],
                                "project": {
                                    "title": "Galeria de Personagens",
                                    "description": "Criar um personagem a partir de uma combinação aleatória de características e apresentá-lo brevemente ao grupo"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Espetáculo de Improvisação",
                            "description": "Realizar uma pequena apresentação de cenas improvisadas baseadas em sugestões da plateia",
                            "deliverables": ["Apresentação ao vivo", "Participação como improvisador e como suporte para colegas"],
                            "estimated_time": "3 sessões de ensaio + 1 apresentação"
                        }
                    }
                ],
                "final_project": {
                    "title": "Cenas Curtas Originais",
                    "description": "Criar e apresentar pequenas cenas teatrais em grupos",
                    "requirements": [
                        "Desenvolvimento colaborativo de uma cena de 3-5 minutos",
                        "Definição clara de personagens e situação",
                        "Utilização de expressão corporal e vocal estudadas",
                        "Ensaios e refinamento da cena",
                        "Apresentação para público (colegas e/ou convidados)"
                    ],
                    "rubric": "Avaliação baseada em criatividade, trabalho em equipe, expressividade e comprometimento",
                    "showcase": "Mostra de Cenas para a comunidade escolar"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Teatro",
                    "format": "Participação na apresentação final + autoavaliação reflexiva",
                    "passing_criteria": "Demonstração de compreensão prática dos elementos teatrais básicos",
                    "certification": "Artista Teatral Iniciante"
                },
                "suggested_path_forward": ["Interpretação Teatral", "Direção Teatral", "Dramaturgia"]
            },
            "intermediario": {
                "description": "Aprofundamento em técnicas de interpretação e montagem de pequenas peças",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Técnicas de Interpretação",
                        "module_description": "Aprenda métodos e ferramentas para a construção de personagens e cenas",
                        "estimated_time": "7 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Construção de Personagem",
                                "objectives": "Aprender a desenvolver personagens tridimensionais",
                                "steps": [
                                    "Análise de texto e subtexto",
                                    "Biografia e circunstâncias dadas",
                                    "Ações físicas e objetivos",
                                    "Arco de desenvolvimento do personagem"
                                ]
                            },
                            {
                                "lesson_title": "Emoção e Verdade Cênica",
                                "objectives": "Desenvolver autenticidade emocional na interpretação",
                                "steps": [
                                    "Memória emotiva e experiências pessoais",
                                    "Resposta emocional às circunstâncias da cena",
                                    "Concentração e presença",
                                    "Equilíbrio entre técnica e espontaneidade"
                                ],
                                "project": {
                                    "title": "Monólogo Emocional",
                                    "description": "Interpretar um monólogo curto explorando uma emoção específica em profundidade"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Processo de Montagem",
                        "module_description": "Experimente as etapas de criação de uma peça teatral",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Do Texto à Cena",
                                "objectives": "Compreender o processo de transformar um texto em montagem teatral",
                                "steps": [
                                    "Leitura dramática e análise de texto",
                                    "Divisão de cenas e marcação básica",
                                    "Ensaios: do mecânico ao orgânico",
                                    "Refinamento e ajustes"
                                ]
                            },
                            {
                                "lesson_title": "Elementos da Encenação",
                                "objectives": "Explorar componentes visuais e sonoros do espetáculo",
                                "steps": [
                                    "Cenografia e objetos de cena",
                                    "Figurino e caracterização",
                                    "Iluminação básica",
                                    "Sonoplastia e trilha sonora"
                                ],
                                "project": {
                                    "title": "Proposta de Design",
                                    "description": "Criar um conceito visual para uma cena ou pequena peça, incluindo esboços e referências"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Cenas Adaptadas",
                            "description": "Montar cenas de peças conhecidas em pequenos grupos",
                            "deliverables": ["Apresentação da cena", "Portfólio do processo criativo", "Reflexão sobre desafios e aprendizados"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Montagem de Peça Curta",
                    "description": "Criar uma apresentação teatral de 15-20 minutos a partir de texto existente ou criação coletiva",
                    "requirements": [
                        "Desenvolvimento completo de personagens",
                        "Ensaios sistemáticos e organizados",
                        "Criação ou adaptação de elementos cênicos",
                        "Apresentação para público externo",
                        "Documentação do processo criativo"
                    ]
                }
            },
            "avancado": {
                "description": "Aprofundamento em criação teatral e desenvolvimento de linguagem própria",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Estilos e Linguagens Teatrais",
                        "module_description": "Explore diferentes abordagens e estéticas teatrais",
                        "lessons": [
                            {
                                "lesson_title": "Do Clássico ao Contemporâneo",
                                "objectives": "Compreender e experimentar diversos estilos teatrais",
                                "steps": [
                                    "Teatro grego e clássico",
                                    "Teatro realista e naturalista",
                                    "Teatro do absurdo e surrealista",
                                    "Performances contemporâneas e teatro pós-dramático"
                                ]
                            },
                            {
                                "lesson_title": "Teatro Físico e Máscaras",
                                "objectives": "Explorar linguagens teatrais centradas no corpo e na transformação",
                                "steps": [
                                    "Commedia dell'Arte e uso de máscaras",
                                    "Mímica e pantomima",
                                    "Viewpoints e composição física",
                                    "Criação de partituras corporais"
                                ],
                                "project": {
                                    "title": "Cena Sem Palavras",
                                    "description": "Criar uma cena que comunique uma história completa apenas com movimento"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Criação Teatral Autoral",
                        "module_description": "Desenvolva seu próprio processo criativo e voz artística",
                        "lessons": [
                            {
                                "lesson_title": "Dramaturgia em Processo",
                                "objectives": "Aprender a criar textos dramáticos e roteiros para cena",
                                "steps": [
                                    "Estrutura dramática e arco narrativo",
                                    "Desenvolvimento de diálogos e personagens",
                                    "Dramaturgia em processo colaborativo",
                                    "Adaptação e criação a partir de outras fontes"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Laboratório de Criação",
                            "description": "Desenvolver um exercício cênico experimental a partir de tema ou estímulo não convencional"
                        }
                    }
                ],
                "final_project": {
                    "title": "Espetáculo Autoral",
                    "description": "Criar e apresentar um espetáculo teatral completo com linguagem própria",
                    "requirements": [
                        "Envolvimento em múltiplas funções (atuação, direção, dramaturgia, etc.)",
                        "Pesquisa aprofundada sobre temas e estéticas",
                        "Processo criativo documentado em portfólio",
                        "Apresentação pública com debate após o espetáculo",
                        "Reflexão crítica sobre o resultado e o processo"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Direção Teatral",
                "description": "Foco na concepção, organização e condução do processo criativo teatral",
                "age_range": "15-17 anos",
                "modules": [
                    "Fundamentos da Direção",
                    "Trabalho com Atores e Condução de Ensaios",
                    "Concepção Visual e Sonora",
                    "Processo Criativo e Metodologias"
                ],
                "final_project": {
                    "title": "Direção de Cena",
                    "description": "Dirigir uma cena ou peça curta, liderando todo o processo criativo"
                }
            },
            {
                "name": "Teatro Musical",
                "description": "Integração de teatro, música e dança em performances completas",
                "age_range": "12-17 anos",
                "modules": [
                    "Canto para Teatro Musical",
                    "Dança e Movimento Cênico",
                    "Interpretação para Musicais",
                    "História e Estilos do Teatro Musical"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Ator/Atriz",
                "Diretor Teatral",
                "Dramaturgo",
                "Cenógrafo",
                "Figurinista",
                "Produtor Cultural",
                "Professor de Teatro",
                "Diretor de Casting"
            ],
            "day_in_life": [
                "Um ator divide seu tempo entre ensaios, apresentações e estudo de novos personagens",
                "Um diretor teatral coordena equipes criativas e técnicas para criar um espetáculo coeso",
                "Um dramaturgo pesquisa, escreve e revisa textos para montagens teatrais",
                "Um produtor cultural organiza aspectos logísticos, financeiros e promocionais do espetáculo"
            ],
            "educational_paths": [
                "Graduação em Artes Cênicas ou Teatro",
                "Cursos técnicos de interpretação",
                "Oficinas e workshops especializados",
                "Participação em grupos de teatro amador e estudantil",
                "Estudos independentes e grupos de pesquisa"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Expressão oral e corporal básica"],
            "cross_curricular": ["Literatura", "História", "Música", "Educação Física", "Sociologia"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Teatro"] = teatro_subarea
    area_ref.set(area_data)

    return area_data


def setup_artes_danca_subarea(db):
    """
    Configura a subárea de Dança dentro da área de Artes e Expressão.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    danca_subarea = {
        "name": "Dança",
        "description": "Explore o maravilhoso mundo da dança, desenvolvendo expressão corporal, consciência espacial, ritmo e criatividade através do movimento.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "footsteps",
        "references": [
            {"title": "Portal da Dança", "url": "https://www.portaldadanca.com.br/"},
            {"title": "Dance Teacher", "url": "https://www.dance-teacher.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos no mundo da dança, com foco na consciência corporal e expressão através do movimento",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Desenvolver consciência corporal e coordenação motora",
                    "Compreender os elementos básicos do movimento: tempo, espaço, peso e fluxo",
                    "Explorar diferentes qualidades de movimento e expressão",
                    "Criar sequências simples de movimento individualmente e em grupo"
                ],
                "modules": [
                    {
                        "module_title": "Descobrindo o Corpo em Movimento",
                        "module_description": "Explore as possibilidades do seu corpo e desenvolva consciência corporal",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Percepção e Consciência Corporal",
                                "objectives": "Desenvolver uma relação consciente com o próprio corpo e suas possibilidades",
                                "estimated_time": "60 minutos",
                                "content_summary": "Exercícios de percepção corporal, respiração e alinhamento postural",
                                "steps": [
                                    "Reconhecimento das partes do corpo e suas articulações",
                                    "Exercícios de respiração e concentração",
                                    "Alinhamento e postura básica",
                                    "Movimentos isolados e integrados do corpo"
                                ],
                                "exercises": [
                                    {
                                        "question": "Como a respiração afeta a qualidade do movimento?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Resposta pessoal. Podem mencionar fluidez, energia, relaxamento, controle, intensidade, sustentação, etc."
                                    },
                                    {
                                        "question": "Qual dos seguintes elementos NÃO faz parte do alinhamento postural básico para dança?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Coluna alongada",
                                            "Ombros para trás e tensos",
                                            "Joelhos alinhados com os pés",
                                            "Distribuição equilibrada do peso"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "exercício prático",
                                        "title": "Mapa Corporal",
                                        "description": "Em duplas, desenhar o contorno do corpo do colega em papel grande e identificar partes do corpo e articulações importantes para o movimento"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Exercícios de Consciência Corporal",
                                     "url": "https://exemplo.com/video_consciencia"},
                                    {"type": "artigo", "title": "A Importância do Alinhamento na Dança",
                                     "url": "https://exemplo.com/artigo_alinhamento"}
                                ]
                            },
                            {
                                "lesson_title": "Explorando o Espaço",
                                "objectives": "Compreender e experimentar as relações entre corpo e espaço",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "Níveis: alto, médio, baixo",
                                    "Direções: frente, trás, diagonais, lados",
                                    "Trajetórias: retas, curvas, circulares, ziguezague",
                                    "Dimensões: grande, pequeno, expandido, recolhido"
                                ],
                                "exercises": [
                                    {
                                        "question": "Crie uma sequência curta de movimentos que utilize os três níveis (alto, médio e baixo). Como a mudança de nível afetou seus movimentos?",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Devem refletir sobre como cada nível proporciona diferentes possibilidades de movimento, equilíbrio, energia, etc."
                                    }
                                ],
                                "project": {
                                    "title": "Desenho no Espaço",
                                    "description": "Criar uma 'dança' que desenhe uma forma específica no espaço (círculo, espiral, estrela, etc.)",
                                    "expected_outcome": "Compreensão prática das trajetórias espaciais",
                                    "estimated_time": "25 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Demonstração de Consciência Corporal",
                            "format": "Apresentação de sequência individual + reflexão oral",
                            "passing_score": "Demonstração de compreensão básica dos conceitos",
                            "time_limit": "5 minutos por estudante",
                            "certificate": "Explorador do Movimento - Nível 1"
                        }
                    },
                    {
                        "module_title": "Ritmo e Expressão",
                        "module_description": "Desenvolva sensibilidade rítmica e expressividade através do movimento",
                        "estimated_time": "5 semanas",
                        "prerequisites": ["Descobrindo o Corpo em Movimento"],
                        "lessons": [
                            {
                                "lesson_title": "Bases Rítmicas",
                                "objectives": "Desenvolver percepção rítmica e sua aplicação no movimento",
                                "steps": [
                                    "Pulsação e contagem musical",
                                    "Relação entre música e movimento",
                                    "Diferentes velocidades e dinâmicas",
                                    "Padrões rítmicos simples"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual é a diferença entre tempo e ritmo na dança?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "São exatamente a mesma coisa",
                                            "Tempo é a velocidade da música, enquanto ritmo é o padrão de acentuações",
                                            "Tempo é para música clássica, ritmo é para música popular",
                                            "Tempo é para solistas, ritmo é para grupos"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Traduções Rítmicas",
                                    "description": "Traduzir diferentes padrões rítmicos em movimentos corporais",
                                    "steps": [
                                        "Escutar atentamente diferentes ritmos",
                                        "Identificar padrões e acentuações",
                                        "Criar movimentos que correspondam aos padrões",
                                        "Apresentar para os colegas e receber feedback"
                                    ],
                                    "estimated_time": "45 minutos"
                                }
                            },
                            {
                                "lesson_title": "Qualidades de Movimento",
                                "objectives": "Explorar diferentes dinâmicas e qualidades expressivas",
                                "steps": [
                                    "Fluido versus fragmentado",
                                    "Leve versus pesado",
                                    "Direto versus indireto",
                                    "Rápido versus lento"
                                ],
                                "project": {
                                    "title": "Opostos em Dança",
                                    "description": "Criar uma pequena coreografia que explore qualidades opostas de movimento"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Mini-Coreografia Expressiva",
                            "description": "Criar uma sequência de 30-60 segundos que explore o tema 'As Quatro Estações'",
                            "deliverables": ["Coreografia apresentada ao vivo", "Breve explicação das escolhas criativas", "Participação na avaliação coletiva"],
                            "estimated_time": "3 aulas para desenvolvimento + apresentação final"
                        }
                    }
                ],
                "final_project": {
                    "title": "Dança Narrativa",
                    "description": "Criar uma coreografia em pequenos grupos que conte uma história simples",
                    "requirements": [
                        "Duração de 2-3 minutos",
                        "Utilização consciente do espaço, níveis e dinâmicas",
                        "Relação clara com a música escolhida",
                        "Narrativa reconhecível através do movimento",
                        "Participação colaborativa de todos os integrantes"
                    ],
                    "rubric": "Avaliação baseada em criatividade, expressividade, consciência corporal e trabalho em equipe",
                    "showcase": "Apresentação para a comunidade escolar"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos da Dança",
                    "format": "Apresentação final + diário de processo criativo",
                    "passing_criteria": "Demonstração de compreensão prática dos elementos básicos da dança",
                    "certification": "Dançarino Iniciante"
                },
                "suggested_path_forward": ["Técnicas de Dança Específicas", "Composição Coreográfica",
                                           "Dança e Tecnologia"]
            },
            "intermediario": {
                "description": "Aprofundamento em técnicas de dança e introdução à composição coreográfica",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Técnicas e Estilos",
                        "module_description": "Explore diferentes estilos de dança e suas técnicas específicas",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Dança Contemporânea Básica",
                                "objectives": "Aprender fundamentos da dança contemporânea",
                                "steps": [
                                    "Princípios de contração e release",
                                    "Trabalho de chão e rolamentos",
                                    "Consciência do centro e fluidez",
                                    "Improvisação estruturada"
                                ]
                            },
                            {
                                "lesson_title": "Elementos de Danças Urbanas",
                                "objectives": "Conhecer movimentos básicos de estilos urbanos",
                                "steps": [
                                    "Fundamentos de hip hop e suas variações",
                                    "Groove e feeling",
                                    "Top rock e footwork básicos",
                                    "Criação de pequenas sequências"
                                ],
                                "project": {
                                    "title": "Fusão de Estilos",
                                    "description": "Criar uma sequência que combine elementos de diferentes estilos de dança"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Composição Coreográfica",
                        "module_description": "Aprenda princípios e ferramentas para criar coreografias",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Ferramentas de Composição",
                                "objectives": "Conhecer métodos para criar e estruturar movimentos",
                                "steps": [
                                    "Desenvolvimento de motivos de movimento",
                                    "Variações: tempo, nível, tamanho, direção",
                                    "Estruturas coreográficas: ABA, rondó, cânone",
                                    "Uníssonos e contrapontos"
                                ]
                            },
                            {
                                "lesson_title": "Do Conceito ao Movimento",
                                "objectives": "Aprender a transformar ideias e conceitos em expressão corporal",
                                "steps": [
                                    "Pesquisa e inspiração para criação",
                                    "Improvisação guiada por temas",
                                    "Seleção e refinamento de material",
                                    "Relação entre movimento e significado"
                                ],
                                "project": {
                                    "title": "Movimento Abstrato",
                                    "description": "Criar uma pequena coreografia baseada em um conceito abstrato (liberdade, tempo, conflito, etc.)"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Composição em Grupo",
                            "description": "Criar uma coreografia para pequeno grupo baseada em estímulo não-dançado (poema, pintura, notícia, etc.)",
                            "deliverables": ["Coreografia de 2-3 minutos", "Diário de processo criativo",
                                             "Apresentação com explicação do conceito"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Coreográfico",
                    "description": "Desenvolver uma coreografia completa para grupo, escolhendo tema e abordagem estética",
                    "requirements": [
                        "Duração de 3-5 minutos",
                        "Utilização consciente de ferramentas de composição",
                        "Coerência entre tema, música e movimentos",
                        "Processo colaborativo documentado",
                        "Apresentação pública com programa explicativo"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de linguagem própria e aprofundamento em pesquisa e criação em dança",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Pesquisa em Movimento",
                        "module_description": "Aprofunde sua pesquisa corporal e desenvolva vocabulário próprio",
                        "lessons": [
                            {
                                "lesson_title": "Laboratório de Movimento",
                                "objectives": "Desenvolver pesquisa corporal sistematizada",
                                "steps": [
                                    "Práticas somáticas e consciência refinada",
                                    "Desconstrução de padrões habituais",
                                    "Criação de partituras corporais",
                                    "Desenvolvimento de assinatura de movimento"
                                ]
                            },
                            {
                                "lesson_title": "Corpo e Identidade",
                                "objectives": "Explorar a relação entre movimento, história pessoal e identidade",
                                "steps": [
                                    "Memória corporal e biografia em movimento",
                                    "Investigação de heranças culturais através da dança",
                                    "Questões sociais e políticas no corpo que dança",
                                    "Autenticidade e voz própria"
                                ],
                                "project": {
                                    "title": "Autobiografia em Movimento",
                                    "description": "Criar um solo que explore aspectos da identidade e história pessoal"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Dança e Interdisciplinaridade",
                        "module_description": "Explore as relações entre dança e outras linguagens artísticas",
                        "lessons": [
                            {
                                "lesson_title": "Dança e Tecnologia",
                                "objectives": "Experimentar interfaces entre dança e recursos tecnológicos",
                                "steps": [
                                    "Videodança: princípios básicos",
                                    "Projeções e cenografia virtual",
                                    "Interação com sensores e ambientes responsivos",
                                    "Documentação e arquivo de processos"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Obra Interdisciplinar",
                            "description": "Criar uma performance que combine dança com pelo menos outra linguagem artística"
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Artístico Autoral",
                    "description": "Desenvolver uma obra coreográfica completa que apresente pesquisa e linguagem próprias",
                    "requirements": [
                        "Concepção, criação e apresentação de obra autoral",
                        "Desenvolvimento de conceito e dramaturgia",
                        "Pesquisa de elementos cênicos integrados",
                        "Documentação completa do processo",
                        "Apresentação pública com debate"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Danças Brasileiras",
                "description": "Estudo e prática de danças tradicionais e contemporâneas brasileiras",
                "age_range": "10-17 anos",
                "modules": [
                    "Danças Folclóricas Regionais",
                    "Danças Afro-brasileiras",
                    "Samba e seus Desdobramentos",
                    "Danças Contemporâneas com Raízes Brasileiras"
                ],
                "final_project": {
                    "title": "Brasil em Movimento",
                    "description": "Criar uma apresentação baseada em pesquisa sobre danças de uma região brasileira"
                }
            },
            {
                "name": "Dança e Performance",
                "description": "Exploração da dança como arte performática e sua relação com espaços alternativos",
                "age_range": "14-17 anos",
                "modules": [
                    "Site Specific e Intervenção Urbana",
                    "Performance e Arte Conceitual",
                    "Processos Colaborativos",
                    "Relação com o Público e Participação"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Bailarino/Dançarino",
                "Coreógrafo",
                "Professor de Dança",
                "Diretor de Companhia",
                "Terapeuta Corporal",
                "Produtor de Dança",
                "Pesquisador em Artes do Corpo"
            ],
            "day_in_life": [
                "Um bailarino profissional dedica horas a treinamento técnico, ensaios e apresentações",
                "Um coreógrafo desenvolve conceitos, dirige ensaios e refina obras em constante processo",
                "Um professor de dança adapta metodologias para diferentes perfis de alunos",
                "Um diretor de companhia equilibra aspectos artísticos, administrativos e de produção"
            ],
            "educational_paths": [
                "Graduação em Dança (Bacharelado ou Licenciatura)",
                "Formação técnica em escolas especializadas",
                "Cursos livres e workshops intensivos",
                "Intercâmbios e residências artísticas",
                "Grupos de pesquisa e companhias jovens"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica"],
            "cross_curricular": ["Música", "História", "Anatomia", "Artes Visuais", "Literatura"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Dança"] = danca_subarea
    area_ref.set(area_data)

    return area_data

def setup_artes_design_subarea(db):
    """
    Configura a subárea de Design dentro da área de Artes e Expressão,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    design_subarea = {
        "name": "Design",
        "description": "Descubra como unir criatividade e funcionalidade para solucionar problemas e criar experiências visuais impactantes através do design.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "pencil-ruler",
        "references": [
            {"title": "Mundo do Design", "url": "https://www.mundododesign.com.br/"},
            {"title": "Design for Kids", "url": "https://www.designforkids.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução aos fundamentos do design e suas aplicações básicas",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os princípios básicos do design (cor, forma, tipografia, etc.)",
                    "Reconhecer diferentes áreas e aplicações do design",
                    "Desenvolver projetos simples que unam função e estética",
                    "Utilizar ferramentas básicas de design, tanto manuais quanto digitais"
                ],
                "modules": [
                    {
                        "module_title": "Introdução ao Mundo do Design",
                        "module_description": "Descubra o que é design e como ele está presente em tudo ao nosso redor",
                        "estimated_time": "3 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "O que é Design?",
                                "objectives": "Compreender o conceito de design e sua importância no nosso dia a dia",
                                "estimated_time": "45 minutos",
                                "content_summary": "Exploração do conceito de design como união entre função e estética para resolver problemas",
                                "steps": [
                                    "Definição de design e sua diferença da arte pura",
                                    "Áreas do design: gráfico, produto, moda, interiores, etc.",
                                    "Design no cotidiano: objetos, embalagens, interfaces",
                                    "O processo de design: do problema à solução"
                                ],
                                "exercises": [
                                    {
                                        "question": "Identifique três objetos do seu dia a dia e explique como o design deles facilita ou dificulta seu uso.",
                                        "type": "open",
                                        "suggested_time": "15 minutos",
                                        "answer": "Resposta pessoal. Podem mencionar smartphones (design de interface intuitiva), cadeiras (ergonomia), embalagens (facilidade de abertura), etc."
                                    },
                                    {
                                        "question": "Qual é a principal diferença entre arte e design?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Arte é criada à mão, design é digital",
                                            "Arte expressa sentimentos, design resolve problemas",
                                            "Arte é antiga, design é moderno",
                                            "Arte é para museus, design para lojas"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "atividade",
                                        "title": "Caça ao Design",
                                        "description": "Em grupos, registrar (fotografar ou desenhar) exemplos de bom e mau design no ambiente escolar"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Design no Nosso Dia a Dia",
                                     "url": "https://exemplo.com/video_design"},
                                    {"type": "infográfico", "title": "As Áreas do Design",
                                     "url": "https://exemplo.com/infografico_design"}
                                ]
                            },
                            {
                                "lesson_title": "Elementos Visuais do Design",
                                "objectives": "Conhecer os componentes básicos da linguagem visual do design",
                                "estimated_time": "60 minutos",
                                "steps": [
                                    "Ponto, linha e forma",
                                    "Cor, textura e espaço",
                                    "Escala e proporção",
                                    "Equilíbrio e hierarquia visual"
                                ],
                                "exercises": [
                                    {
                                        "question": "Como o uso de cores diferentes pode afetar a forma como percebemos um produto ou mensagem?",
                                        "type": "open",
                                        "answer": "Resposta deve abordar como as cores evocam emoções diferentes, criam associações culturais, afetam a visibilidade e legibilidade, e ajudam a estabelecer identidade de marca."
                                    }
                                ],
                                "project": {
                                    "title": "Composição de Elementos",
                                    "description": "Criar composições visuais usando apenas formas geométricas coloridas para expressar emoções diferentes",
                                    "expected_outcome": "Compreensão prática de como os elementos visuais comunicam",
                                    "estimated_time": "30 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Fundamentos do Design",
                            "format": "Perguntas de múltipla escolha + análise de case",
                            "passing_score": 70,
                            "time_limit": "30 minutos",
                            "certificate": "Explorador do Design - Nível 1"
                        }
                    },
                    {
                        "module_title": "Design Gráfico Básico",
                        "module_description": "Aprenda os fundamentos do design gráfico e crie seus primeiros projetos",
                        "estimated_time": "5 semanas",
                        "prerequisites": ["Introdução ao Mundo do Design"],
                        "lessons": [
                            {
                                "lesson_title": "Tipografia para Iniciantes",
                                "objectives": "Aprender os conceitos básicos sobre tipos e seu uso eficaz",
                                "steps": [
                                    "Famílias tipográficas: serifadas, não-serifadas, decorativas",
                                    "Anatomia das letras",
                                    "Legibilidade e leiturabilidade",
                                    "Combinação de fontes e hierarquia tipográfica"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual tipo de fonte é geralmente mais indicada para textos longos?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Fontes decorativas",
                                            "Fontes serifadas",
                                            "Fontes manuscritas",
                                            "Fontes em negrito"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Pôster Tipográfico",
                                    "description": "Criar um pôster usando apenas tipografia para comunicar uma mensagem ou citação inspiradora",
                                    "steps": [
                                        "Escolher uma frase ou citação curta",
                                        "Experimentar diferentes fontes e tamanhos",
                                        "Criar hierarquia e ritmo visual com a tipografia",
                                        "Finalizar o design considerando equilíbrio e composição"
                                    ],
                                    "estimated_time": "60 minutos"
                                }
                            },
                            {
                                "lesson_title": "Criação de Logos Simples",
                                "objectives": "Aprender o processo de design de marcas e logotipos básicos",
                                "steps": [
                                    "O que é uma identidade visual",
                                    "Brainstorming e esboços iniciais",
                                    "Simplificação e refinamento",
                                    "Aplicações e versões do logotipo"
                                ],
                                "project": {
                                    "title": "Minha Marca Pessoal",
                                    "description": "Criar um logotipo simples que represente sua personalidade ou interesses"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Mini Campanha Visual",
                            "description": "Criar uma campanha visual simples (logo, cartaz e folheto) para um evento escolar ou causa social",
                            "deliverables": ["Logo finalizado", "Pôster tamanho A3", "Folheto informativo", "Breve manual de aplicação"],
                            "estimated_time": "3 semanas (trabalho em aula e em casa)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Redesign com Propósito",
                    "description": "Identificar um problema de design no ambiente escolar ou comunidade e propor uma solução",
                    "requirements": [
                        "Documentação do problema identificado (fotos, entrevistas)",
                        "Pesquisa sobre soluções existentes",
                        "Processo de ideação e esboços",
                        "Protótipo ou mockup final",
                        "Apresentação justificando as decisões de design"
                    ],
                    "rubric": "Avaliação baseada em identificação do problema, criatividade da solução, aplicação de conceitos e apresentação",
                    "showcase": "Exposição dos projetos para a comunidade escolar"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Design",
                    "format": "Portfólio digital + projeto final + teste conceitual",
                    "passing_criteria": "Demonstração de compreensão dos princípios básicos e capacidade de aplicá-los",
                    "certification": "Designer Iniciante"
                },
                "suggested_path_forward": ["Design Digital", "UX/UI", "Design de Produto"]
            },
            "intermediario": {
                "description": "Aprofundamento de técnicas de design e introdução a ferramentas digitais mais avançadas",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Design Digital",
                        "module_description": "Aprenda a criar projetos de design usando ferramentas digitais",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Introdução ao Software de Design",
                                "objectives": "Familiarizar-se com ferramentas básicas de design digital",
                                "steps": [
                                    "Interfaces e ferramentas comuns",
                                    "Criação e manipulação de formas vetoriais",
                                    "Edição de cores e efeitos",
                                    "Organização de camadas e artboards"
                                ]
                            },
                            {
                                "lesson_title": "Manipulação de Imagens",
                                "objectives": "Aprender técnicas básicas de edição e composição de imagens",
                                "steps": [
                                    "Ajustes básicos: brilho, contraste, saturação",
                                    "Seleções e máscaras",
                                    "Manipulação não-destrutiva com ajustes e filtros",
                                    "Composição de múltiplos elementos"
                                ],
                                "project": {
                                    "title": "Capa de Revista Conceitual",
                                    "description": "Criar uma capa de revista que combine fotografia, tipografia e elementos gráficos"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Design de Informação",
                        "module_description": "Explore como visualizar dados e informações de forma clara e atrativa",
                        "estimated_time": "5 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Infográficos e Visualização de Dados",
                                "objectives": "Aprender a comunicar informações complexas visualmente",
                                "steps": [
                                    "Tipos de gráficos e quando usá-los",
                                    "Hierarquia e fluxo de informação",
                                    "Uso de ícones e pictogramas",
                                    "Simplificação e foco na mensagem principal"
                                ]
                            },
                            {
                                "lesson_title": "Design de Instruções Visuais",
                                "objectives": "Criar guias visuais que expliquem processos de forma clara",
                                "steps": [
                                    "Análise do público e contexto",
                                    "Sequenciamento lógico de informações",
                                    "Uso de setas, números e indicadores",
                                    "Teste de compreensão com usuários"
                                ],
                                "project": {
                                    "title": "Guia Visual",
                                    "description": "Criar um manual ilustrado para uma atividade ou processo escolhido pelo estudante"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Infográfico Interativo",
                            "description": "Desenvolver um infográfico digital e/ou impresso sobre um tema social ou científico relevante",
                            "deliverables": ["Infográfico finalizado", "Fontes de dados utilizadas", "Documento de processo"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Campanha de Comunicação Visual",
                    "description": "Criar uma campanha completa para uma causa social ou evento, integrando múltiplas peças e plataformas",
                    "requirements": [
                        "Identidade visual consistente",
                        "Aplicações impressas e digitais",
                        "Estratégia de comunicação visual",
                        "Consideração do público-alvo",
                        "Apresentação profissional do projeto"
                    ]
                }
            },
            "avancado": {
                "description": "Projetos complexos de design e introdução ao design centrado no usuário",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Design de Experiência do Usuário",
                        "module_description": "Aprenda a criar produtos digitais centrados nas necessidades das pessoas",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos de UX/UI",
                                "objectives": "Compreender a diferença entre UX e UI e seus princípios básicos",
                                "steps": [
                                    "Introdução à experiência do usuário (UX)",
                                    "Interface do usuário (UI) e seus componentes",
                                    "Pesquisa e personas",
                                    "Jornadas do usuário e pontos de contato"
                                ]
                            },
                            {
                                "lesson_title": "Prototipagem e Testes",
                                "objectives": "Aprender a criar e testar protótipos de interfaces",
                                "steps": [
                                    "Wireframes e fluxos de navegação",
                                    "Prototipagem de baixa e alta fidelidade",
                                    "Testes de usabilidade básicos",
                                    "Iteração baseada em feedback"
                                ],
                                "project": {
                                    "title": "Aplicativo Conceitual",
                                    "description": "Criar protótipo de um aplicativo que resolva um problema específico para jovens"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Design para Impacto Social",
                        "module_description": "Use o design como ferramenta para promover mudanças positivas",
                        "lessons": [
                            {
                                "lesson_title": "Design Thinking",
                                "objectives": "Aplicar a metodologia do design thinking para resolver problemas complexos",
                                "steps": [
                                    "Empatia e imersão no problema",
                                    "Definição e reframing do desafio",
                                    "Ideação e co-criação",
                                    "Prototipagem e testes no mundo real"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Laboratório de Inovação Social",
                            "description": "Utilizar o design thinking para desenvolver soluções para um desafio da comunidade local"
                        }
                    }
                ],
                "final_project": {
                    "title": "Portfólio de Design Completo",
                    "description": "Desenvolver um portfólio profissional com projetos de design diversos e uma identidade pessoal",
                    "requirements": [
                        "Mínimo de três projetos completos com documentação de processo",
                        "Identidade visual pessoal (logo, cores, tipografia)",
                        "Formato digital e impresso",
                        "Estratégia de apresentação e narrativa dos projetos",
                        "Consideração de público-alvo (faculdades, empregadores potenciais)"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Design de Jogos",
                "description": "Foco na criação de jogos analógicos e digitais, desde o conceito até o protótipo",
                "age_range": "13-17 anos",
                "modules": [
                    "Fundamentos do Game Design",
                    "Mecânicas e Dinâmicas de Jogo",
                    "Design de Níveis e Interfaces de Jogos",
                    "Prototipagem e Testes"
                ],
                "final_project": {
                    "title": "Jogo Original",
                    "description": "Criar e testar um jogo completo, digital ou analógico"
                }
            },
            {
                "name": "Design de Produto",
                "description": "Criação de objetos e produtos que unem forma e função",
                "age_range": "14-17 anos",
                "modules": [
                    "Desenho Técnico e Modelagem 3D Básica",
                    "Materiais e Sustentabilidade",
                    "Ergonomia e Usabilidade",
                    "Prototipagem e Fabricação"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Designer Gráfico",
                "UI/UX Designer",
                "Designer de Produto",
                "Designer de Moda",
                "Designer de Interiores",
                "Diretor de Arte",
                "Designer de Jogos",
                "Empreendedor em Design"
            ],
            "day_in_life": [
                "Um designer gráfico cria peças visuais para diferentes plataformas seguindo briefings específicos",
                "Um UX designer pesquisa comportamento de usuários e cria protótipos para testar soluções",
                "Um designer de produto desenvolve objetos que aliam estética, função e viabilidade técnica",
                "Um diretor de arte coordena equipes criativas para garantir coesão visual em campanhas e projetos"
            ],
            "educational_paths": [
                "Graduação em Design (Gráfico, Produto, Digital, Moda)",
                "Cursos técnicos especializados",
                "Bootcamps e workshops intensivos",
                "Aprendizado autodidata com tutoriais e projetos pessoais",
                "Estágios e experiências práticas em agências e estúdios"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Artes Visuais básicas"],
            "cross_curricular": ["Tecnologia", "Matemática", "Comunicação", "Empreendedorismo", "Ciências Sociais"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Design"] = design_subarea
    area_ref.set(area_data)

    return area_data

def setup_artes_escrita_criativa_subarea(db):
    """
    Configura a subárea de Escrita Criativa dentro da área de Artes e Expressão,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    escrita_criativa_subarea = {
        "name": "Escrita Criativa",
        "description": "Explore o poder das palavras para criar histórias, poemas e outros textos literários, desenvolvendo sua voz autoral e habilidade de expressão escrita.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "pen-fancy",
        "references": [
            {"title": "Oficina da Escrita", "url": "https://www.oficinadeescrita.com.br/"},
            {"title": "Creative Writing Now", "url": "https://www.creative-writing-now.com/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos na escrita criativa, com foco em exploração e experimentação textual",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Desenvolver hábito de escrita e superar o bloqueio criativo",
                    "Explorar diferentes gêneros literários e suas características",
                    "Criar personagens, cenários e tramas simples",
                    "Aprender técnicas básicas de revisão e aprimoramento de texto"
                ],
                "modules": [
                    {
                        "module_title": "Despertando o Escritor Interior",
                        "module_description": "Descubra seu potencial criativo e vença o medo da página em branco",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "A Magia das Palavras",
                                "objectives": "Perder o medo de escrever e estimular a criatividade literária",
                                "estimated_time": "50 minutos",
                                "content_summary": "Exercícios de escrita livre e jogos literários para superar bloqueios",
                                "steps": [
                                    "Escrita livre e contínua: escrever sem autocensura",
                                    "Explorando os sentidos na escrita: descrições vívidas",
                                    "Jogos de palavras e associações",
                                    "Transformando memórias em histórias"
                                ],
                                "exercises": [
                                    {
                                        "question": "Escolha um objeto do seu dia a dia e escreva durante 5 minutos continuamente sobre ele, sem levantar a caneta do papel. O que você descobriu?",
                                        "type": "open",
                                        "suggested_time": "15 minutos",
                                        "answer": "Resposta pessoal. O objetivo é perceber como a escrita contínua pode levar a ideias e associações inesperadas."
                                    },
                                    {
                                        "question": "Qual é o objetivo principal da técnica de escrita livre?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Produzir textos gramaticalmente perfeitos",
                                            "Superar bloqueios criativos e gerar ideias sem autocensura",
                                            "Escrever o mais rápido possível para aumentar produtividade",
                                            "Criar histórias completas em pouco tempo"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "jogo",
                                        "title": "Cadáver Delicado",
                                        "description": "Criação coletiva de texto onde cada participante escreve uma parte sem ver o que veio antes"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Como Vencer o Bloqueio Criativo",
                                     "url": "https://exemplo.com/video_bloqueio"},
                                    {"type": "artigo", "title": "Exercícios para Estimular a Criatividade Literária",
                                     "url": "https://exemplo.com/artigo_criatividade"}
                                ]
                            },
                            {
                                "lesson_title": "Observar e Transformar",
                                "objectives": "Desenvolver o olhar atento e a capacidade de transformar observações em material literário",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "A importância da observação para o escritor",
                                    "Diário de escritor: registrando impressões e ideias",
                                    "Transformando cenas do cotidiano em narrativas",
                                    "O poder das perguntas 'E se...?'"
                                ],
                                "exercises": [
                                    {
                                        "question": "Observe uma pessoa desconhecida em um local público (ou imagine uma). Crie uma biografia fictícia curta para ela baseada em detalhes que você observa ou imagina.",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Devem criar uma pequena história baseada em detalhes observáveis ou imaginados."
                                    }
                                ],
                                "project": {
                                    "title": "Caderno de Observações",
                                    "description": "Criar um diário de escritor para registrar observações, ideias e fragmentos de texto por uma semana",
                                    "expected_outcome": "Criação de hábito de observação e registro como ferramenta para escrita criativa",
                                    "estimated_time": "10-15 minutos diários por uma semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Minicontos a partir de Estímulos",
                            "format": "Criação de três minicontos a partir de estímulos diferentes",
                            "passing_score": "Participação e entrega das histórias",
                            "time_limit": "90 minutos",
                            "certificate": "Explorador de Histórias - Nível 1"
                        }
                    },
                    {
                        "module_title": "Elementos Narrativos",
                        "module_description": "Descubra as ferramentas básicas para construir histórias envolventes",
                        "estimated_time": "6 semanas",
                        "prerequisites": ["Despertando o Escritor Interior"],
                        "lessons": [
                            {
                                "lesson_title": "Criando Personagens Memoráveis",
                                "objectives": "Aprender a desenvolver personagens tridimensionais e interessantes",
                                "steps": [
                                    "Dimensões do personagem: física, social, psicológica",
                                    "Desejos, medos e conflitos internos",
                                    "Backstory e motivações",
                                    "Mostrando vs. contando: revelando personalidade através de ações"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que personagens com falhas e contradições tendem a ser mais interessantes?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Porque são mais realistas e identificáveis",
                                            "Porque são mais fáceis de escrever",
                                            "Porque permitem histórias mais curtas",
                                            "Porque agradam mais aos leitores jovens"
                                        ],
                                        "correct_answer": 0
                                    }
                                ],
                                "project": {
                                    "title": "Perfil de Personagem",
                                    "description": "Criar um perfil completo de um personagem original, incluindo aparência, personalidade, história de fundo e conflitos",
                                    "steps": [
                                        "Brainstorming de ideias para personagem",
                                        "Desenvolvimento das três dimensões",
                                        "Criação de história de fundo",
                                        "Escrever uma cena curta que revele o personagem através de ações"
                                    ],
                                    "estimated_time": "90 minutos (divididos em várias sessões)"
                                }
                            },
                            {
                                "lesson_title": "Construindo Mundos",
                                "objectives": "Aprender a criar e descrever cenários e ambientações convincentes",
                                "steps": [
                                    "A importância do cenário para a história",
                                    "Descrições sensoriais: além do visual",
                                    "Mundo real vs. mundos fantásticos",
                                    "Integrando cenário e trama"
                                ],
                                "project": {
                                    "title": "Mapa e Guia",
                                    "description": "Criar um mapa e um pequeno guia descritivo para um mundo ou lugar fictício"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Encontro de Personagens",
                            "description": "Escrever uma cena curta onde dois personagens (seu próprio e de um colega) se encontram em um cenário específico",
                            "deliverables": ["Texto de 1-2 páginas", "Breve explicação das escolhas narrativas", "Leitura compartilhada"],
                            "estimated_time": "2 semanas (incluindo desenvolvimento, escrita e revisão)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Minha Primeira História Completa",
                    "description": "Escrever um conto curto completo, aplicando os elementos narrativos aprendidos",
                    "requirements": [
                        "Texto de 3-5 páginas com começo, meio e fim",
                        "Personagens desenvolvidos com motivações claras",
                        "Ambientação bem descrita e relevante para a história",
                        "Revisão e reescrita do texto baseado em feedback",
                        "Apresentação oral ou leitura para a turma"
                    ],
                    "rubric": "Avaliação baseada em estrutura narrativa, desenvolvimento de personagens, originalidade e progresso individual",
                    "showcase": "Antologia digital ou impressa com as histórias da turma"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos da Escrita Criativa",
                    "format": "Portfólio com seleção de textos + história final + autoavaliação",
                    "passing_criteria": "Demonstração de compreensão dos elementos básicos da narrativa e evolução na escrita",
                    "certification": "Escritor Iniciante"
                },
                "suggested_path_forward": ["Técnicas Narrativas Avançadas", "Poesia", "Escrita de Roteiros"]
            },
            "intermediario": {
                "description": "Aprofundamento nas técnicas narrativas e experimentação com diferentes gêneros literários",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Estrutura e Estilo",
                        "module_description": "Explore diferentes estruturas narrativas e desenvolva seu estilo próprio",
                        "estimated_time": "7 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Arco Narrativo",
                                "objectives": "Compreender e aplicar os elementos da jornada do herói e outras estruturas narrativas",
                                "steps": [
                                    "Exposição, conflito, clímax e resolução",
                                    "A jornada do herói e suas etapas",
                                    "Estruturas alternativas: não-lineares, em mídia res",
                                    "Subtramas e sua relação com a trama principal"
                                ]
                            },
                            {
                                "lesson_title": "Voz e Estilo",
                                "objectives": "Desenvolver uma voz autoral única e consciente",
                                "steps": [
                                    "Análise de estilos de diferentes autores",
                                    "Tom, ritmo e escolhas lexicais",
                                    "Experimentação com diferentes vozes narrativas",
                                    "Encontrando seu estilo próprio"
                                ],
                                "project": {
                                    "title": "Metamorfose Estilística",
                                    "description": "Reescrever um mesmo trecho em três estilos completamente diferentes"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Explorando Gêneros",
                        "module_description": "Experimente diferentes gêneros literários e suas convenções",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Fantasia e Ficção Científica",
                                "objectives": "Aprender a criar mundos especulativos consistentes",
                                "steps": [
                                    "Worldbuilding: regras, sistemas e culturas",
                                    "Consistência interna vs. verossimilhança",
                                    "Convenções e subversões dos gêneros",
                                    "Equilibrando o familiar e o estranho"
                                ]
                            },
                            {
                                "lesson_title": "Poesia e Prosa Poética",
                                "objectives": "Explorar a fronteira entre poesia e prosa",
                                "steps": [
                                    "Ritmo, sonoridade e musicalidade do texto",
                                    "Linguagem figurada: metáforas, símiles, etc.",
                                    "Formas poéticas tradicionais e livres",
                                    "Prosa poética e suas características"
                                ],
                                "project": {
                                    "title": "Coleção Poética",
                                    "description": "Criar um pequeno conjunto de poemas explorando diferentes formas e temas"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Crossover de Gêneros",
                            "description": "Escrever uma história que combine elementos de dois ou mais gêneros literários distintos",
                            "deliverables": ["Texto de 5-8 páginas", "Análise dos elementos de gênero utilizados", "Revisão por pares"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Literário Pessoal",
                    "description": "Desenvolver um projeto de escrita mais ambicioso no gênero de sua escolha",
                    "requirements": [
                        "Planejamento detalhado do projeto (outline, mapas, etc.)",
                        "Texto de 10-15 páginas ou conjunto de textos relacionados",
                        "Aplicação consciente de técnicas narrativas estudadas",
                        "Processo de revisão documentado",
                        "Apresentação criativa para público"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de projetos literários complexos e aperfeiçoamento da voz autoral",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Técnicas Avançadas de Narrativa",
                        "module_description": "Explore técnicas sofisticadas de construção literária",
                        "lessons": [
                            {
                                "lesson_title": "Subtexto e Camadas de Significado",
                                "objectives": "Aprender a criar profundidade narrativa através de camadas de significado",
                                "steps": [
                                    "Subtexto, simbolismo e motivos recorrentes",
                                    "Técnicas de foreshadowing e payoff",
                                    "Ironia dramática e sua utilização",
                                    "Criando múltiplos níveis de leitura"
                                ]
                            },
                            {
                                "lesson_title": "Perspectivas e Pontos de Vista",
                                "objectives": "Dominar diferentes pontos de vista narrativos e seus efeitos",
                                "steps": [
                                    "Primeira, segunda e terceira pessoa: efeitos e limitações",
                                    "Narrador onisciente vs. limitado vs. não confiável",
                                    "Múltiplos pontos de vista em uma narrativa",
                                    "Escolhendo o POV ideal para sua história"
                                ],
                                "project": {
                                    "title": "Caleidoscópio Narrativo",
                                    "description": "Escrever uma mesma cena a partir de três pontos de vista diferentes"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Da Concepção à Publicação",
                        "module_description": "Aprenda o processo completo de criação literária, do conceito à finalização",
                        "lessons": [
                            {
                                "lesson_title": "Planejamento e Processo Criativo",
                                "objectives": "Desenvolver métodos pessoais de organização e criação literária",
                                "steps": [
                                    "Técnicas de planejamento: outline, snowflake, descoberta",
                                    "Estabelecimento de rotina de escrita",
                                    "Superando bloqueios em projetos longos",
                                    "Documentação e organização do processo criativo"
                                ]
                            },
                            {
                                "lesson_title": "Revisão e Edição Avançada",
                                "objectives": "Aprender técnicas de auto-edição e refinamento textual",
                                "steps": [
                                    "Níveis de revisão: estrutural, por cena, linha a linha",
                                    "Identificação e solução de problemas comuns",
                                    "Feedback: como obter e implementar",
                                    "Preparação de manuscrito para compartilhamento"
                                ],
                                "project": {
                                    "title": "Workshop de Revisão",
                                    "description": "Trocar textos com colegas para revisão detalhada e feedback estruturado"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Projeto Editorial Coletivo",
                            "description": "Organizar, editar e produzir uma antologia ou revista literária com trabalhos da turma",
                            "deliverables": ["Publicação finalizada (impressa ou digital)", "Documentação do processo editorial"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Obra Literária Original",
                    "description": "Desenvolver um projeto literário substancial que demonstre domínio das técnicas estudadas",
                    "requirements": [
                        "Obra literária original com extensão significativa (novela, coleção de contos, etc.)",
                        "Documentação do processo criativo",
                        "Revisão e edição profunda do manuscrito",
                        "Criação de materiais complementares (sinopse, biografa do autor, etc.)",
                        "Evento de lançamento ou leitura pública"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Escrita para Mídias Digitais",
                "description": "Foco na criação de conteúdo para blogs, redes sociais e outras plataformas digitais",
                "age_range": "13-17 anos",
                "modules": [
                    "Escrita para Web e SEO",
                    "Storytelling Digital e Transmídia",
                    "Criação de Conteúdo para Redes Sociais",
                    "Narrativas Interativas"
                ],
                "final_project": {
                    "title": "Projeto Digital Narrativo",
                    "description": "Criar um projeto narrativo que utilize recursos digitais e interativos"
                }
            },
            {
                "name": "Roteiro e Dramaturgia",
                "description": "Técnicas específicas para escrita de roteiros para teatro, cinema, TV e outras mídias",
                "age_range": "14-17 anos",
                "modules": [
                    "Fundamentos de Roteiro",
                    "Diálogos e Subtexto",
                    "Estrutura Dramática",
                    "Adaptação entre Mídias"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Escritor/Autor",
                "Roteirista",
                "Editor",
                "Redator Publicitário",
                "Jornalista",
                "Professor de Escrita Criativa",
                "Ghostwriter",
                "Produtor de Conteúdo Digital"
            ],
            "day_in_life": [
                "Um autor divide seu tempo entre escrita criativa, pesquisa, revisão e relacionamento com editores",
                "Um roteirista desenvolve histórias para mídia visual trabalhando em equipe",
                "Um editor analisa manuscritos, fornece feedback e acompanha o desenvolvimento de obras",
                "Um redator publicitário cria textos persuasivos e criativos para campanhas"
            ],
            "educational_paths": [
                "Graduação em Letras, Comunicação ou áreas afins",
                "Oficinas e cursos especializados de escrita",
                "Participação em grupos de escrita e feedback",
                "Leitura constante e estudo de técnicas narrativas",
                "Publicação independente e construção de portfólio"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Português e Literatura básica"],
            "cross_curricular": ["Literatura", "História", "Psicologia", "Comunicação", "Artes Visuais"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Escrita Criativa"] = escrita_criativa_subarea
    area_ref.set(area_data)

    return area_data


def setup_artes_cinema_audiovisual_subarea(db):
    """
    Configura a subárea de Cinema e Audiovisual dentro da área de Artes e Expressão.
    """
    area_ref = db.collection("learning_paths").document("Artes e Expressão")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Artes e Expressão",
            "description": "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    cinema_audiovisual_subarea = {
        "name": "Cinema e Audiovisual",
        "description": "Explore o fascinante mundo do cinema e das produções audiovisuais, aprendendo a contar histórias através de imagens em movimento e som.",
        "estimated_time": "3-12 meses (dependendo da dedicação)",
        "icon": "film",
        "references": [
            {"title": "Portal do Cinema", "url": "https://www.portaldocinema.com.br/"},
            {"title": "Film Education", "url": "https://www.filmeducation.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução ao mundo do cinema e criação de pequenos projetos audiovisuais",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os elementos básicos da linguagem cinematográfica",
                    "Desenvolver olhar crítico para análise de produções audiovisuais",
                    "Criar pequenos vídeos utilizando recursos acessíveis",
                    "Trabalhar colaborativamente em projetos audiovisuais simples"
                ],
                "modules": [
                    {
                        "module_title": "Descobrindo a Linguagem do Cinema",
                        "module_description": "Conheça os elementos fundamentais que compõem um filme",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "A Magia das Imagens em Movimento",
                                "objectives": "Entender como surgiu o cinema e seus elementos básicos",
                                "estimated_time": "60 minutos",
                                "content_summary": "Uma viagem pela história do cinema e introdução aos elementos fundamentais da linguagem cinematográfica",
                                "steps": [
                                    "Breve história do cinema: dos irmãos Lumière ao digital",
                                    "Como funciona a ilusão do movimento: persistência retiniana",
                                    "Do cinema mudo ao som, às cores e aos efeitos especiais",
                                    "Os diferentes tipos de produções audiovisuais hoje"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que o cinema é considerado uma arte coletiva?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Resposta pessoal. Devem mencionar os diferentes profissionais envolvidos (diretor, atores, fotógrafos, roteiristas, etc.) e como a colaboração entre eles é essencial para o resultado final."
                                    },
                                    {
                                        "question": "Qual dos seguintes NÃO é um elemento básico da linguagem cinematográfica?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Enquadramento",
                                            "Montagem",
                                            "Som",
                                            "Animação 3D"
                                        ],
                                        "correct_answer": 3
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "demonstração",
                                        "title": "Taumatrópio",
                                        "description": "Criar um taumatrópio simples para entender o princípio da persistência retiniana"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "A História do Cinema em 5 Minutos",
                                     "url": "https://exemplo.com/video_cinema"},
                                    {"type": "artigo", "title": "Como o Cinema Mudou o Mundo",
                                     "url": "https://exemplo.com/artigo_cinema"}
                                ]
                            },
                            {
                                "lesson_title": "Enquadramentos e Movimentos",
                                "objectives": "Aprender os tipos de planos e movimentos de câmera",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "Tipos de planos: geral, médio, close, detalhe",
                                    "Ângulos de câmera e seu significado",
                                    "Movimentos: panorâmica, travelling, zoom",
                                    "Composição dentro do quadro"
                                ],
                                "exercises": [
                                    {
                                        "question": "Assista a uma cena de um filme ou série e identifique pelo menos três tipos diferentes de planos utilizados. Que efeito eles causam na narrativa?",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Devem identificar planos e relacioná-los com o efeito narrativo ou emocional na cena."
                                    }
                                ],
                                "project": {
                                    "title": "Álbum de Enquadramentos",
                                    "description": "Criar um álbum (digital ou físico) com exemplos de diferentes tipos de enquadramentos",
                                    "expected_outcome": "Compreensão visual dos diferentes tipos de planos",
                                    "estimated_time": "Tarefa para casa - 1 semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Análise de Cena",
                            "format": "Análise escrita ou oral de uma cena de filme identificando elementos visuais",
                            "passing_score": "Identificação correta de pelo menos 5 elementos técnicos",
                            "time_limit": "30 minutos",
                            "certificate": "Observador Cinematográfico - Nível 1"
                        }
                    },
                    {
                        "module_title": "Meu Primeiro Filme",
                        "module_description": "Aprenda a criar pequenos vídeos com equipamento básico",
                        "estimated_time": "6 semanas",
                        "prerequisites": ["Descobrindo a Linguagem do Cinema"],
                        "lessons": [
                            {
                                "lesson_title": "Do Roteiro à Tela",
                                "objectives": "Aprender a planejar um vídeo antes de filmar",
                                "steps": [
                                    "Ideia, argumento e roteiro simplificado",
                                    "Storyboard: visualizando seu filme no papel",
                                    "Planejamento de filmagem: locações, equipamentos, elenco",
                                    "Organização da equipe e funções"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que é importante fazer um storyboard antes de filmar?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas para filmes com muitos efeitos especiais",
                                            "Para visualizar a sequência de planos e economizar tempo durante a filmagem",
                                            "Porque é uma regra obrigatória do cinema",
                                            "Apenas para mostrar aos atores como eles devem se parecer"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Mini-roteiro e Storyboard",
                                    "description": "Criar um roteiro simples de 1-2 páginas e storyboard para um vídeo de 1-2 minutos",
                                    "steps": [
                                        "Desenvolver uma ideia simples com começo, meio e fim",
                                        "Escrever diálogos (se houver) e descrições de cenas",
                                        "Desenhar storyboard com 10-15 quadros principais",
                                        "Planejar equipamentos e locações necessários"
                                    ],
                                    "estimated_time": "90 minutos"
                                }
                            },
                            {
                                "lesson_title": "Filmando com o que Você Tem",
                                "objectives": "Aprender técnicas básicas de filmagem com equipamentos acessíveis",
                                "steps": [
                                    "Utilizando smartphones e câmeras básicas de forma eficiente",
                                    "Iluminação caseira: aproveitando luz natural e lâmpadas comuns",
                                    "Áudio: importância e técnicas simples de captação",
                                    "Dicas para estabilidade e enquadramento"
                                ],
                                "project": {
                                    "title": "Experimentos de Câmera",
                                    "description": "Criar uma série de testes filmando o mesmo objeto com diferentes enquadramentos e iluminação"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Vídeo de 1 Minuto",
                            "description": "Criar em grupos pequenos um vídeo de aproximadamente 1 minuto sobre tema livre",
                            "deliverables": ["Roteiro e storyboard", "Vídeo finalizado",
                                             "Breve apresentação sobre o processo"],
                            "estimated_time": "3 semanas (incluindo planejamento, filmagem e edição básica)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Curta-metragem Colaborativo",
                    "description": "Criar em equipe um curta-metragem de 3-5 minutos",
                    "requirements": [
                        "Roteiro original desenvolvido pela equipe",
                        "Storyboard completo do filme",
                        "Planejamento de produção (cronograma, locações, etc.)",
                        "Filmagem com atenção à composição e enquadramento",
                        "Edição básica com trilha sonora e/ou efeitos sonoros",
                        "Exibição para público (colegas, familiares, comunidade)"
                    ],
                    "rubric": "Avaliação baseada em narrativa, composição visual, trabalho em equipe e criatividade",
                    "showcase": "Festival de curtas da turma aberto à comunidade escolar"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Audiovisual",
                    "format": "Portfólio digital + projeto final + análise crítica de filme",
                    "passing_criteria": "Demonstração de compreensão dos elementos básicos da linguagem audiovisual",
                    "certification": "Cineasta Iniciante"
                },
                "suggested_path_forward": ["Técnicas de Edição", "Roteiro Avançado", "Animação Básica"]
            },
            "intermediario": {
                "description": "Aprofundamento nas técnicas audiovisuais e desenvolvimento de projetos mais complexos",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Narrativa Audiovisual",
                        "module_description": "Aprenda a contar histórias eficientes através do meio audiovisual",
                        "estimated_time": "7 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Estrutura Narrativa para Audiovisual",
                                "objectives": "Compreender como adaptar princípios de storytelling para o formato audiovisual",
                                "steps": [
                                    "Três atos: apresentação, desenvolvimento, resolução",
                                    "Personagens e arcos de transformação",
                                    "Conflito e tensão dramática",
                                    "Show, don't tell: visual storytelling"
                                ]
                            },
                            {
                                "lesson_title": "Roteiro para Audiovisual",
                                "objectives": "Aprender a escrever roteiros em formato padrão",
                                "steps": [
                                    "Estrutura e formatação de roteiro",
                                    "Escrevendo cenas e sequências",
                                    "Diálogos eficientes e naturais",
                                    "Descrições visuais e indicações técnicas"
                                ],
                                "project": {
                                    "title": "Roteiro de Curta",
                                    "description": "Escrever um roteiro completo para um curta-metragem de 5-10 minutos"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Produção e Pós-produção",
                        "module_description": "Aprofunde seus conhecimentos sobre as etapas de produção de um filme",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Direção e Produção",
                                "objectives": "Compreender o papel do diretor e as etapas de produção",
                                "steps": [
                                    "Funções na equipe de produção audiovisual",
                                    "Preparação: breakdown do roteiro e planejamento",
                                    "Dirigindo atores e equipe técnica",
                                    "Solução de problemas durante a filmagem"
                                ]
                            },
                            {
                                "lesson_title": "Edição e Finalização",
                                "objectives": "Aprender técnicas de montagem e finalização de vídeos",
                                "steps": [
                                    "Princípios de montagem e ritmo",
                                    "Software de edição não-linear básico",
                                    "Correção de cor e tratamento visual",
                                    "Som e trilha sonora"
                                ],
                                "project": {
                                    "title": "Remix Visual",
                                    "description": "Reeditar uma cena de filme ou material existente criando uma nova narrativa"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Trailer Criativo",
                            "description": "Criar um trailer para um filme imaginário ou adaptar uma obra literária",
                            "deliverables": ["Roteiro e storyboard do trailer", "Trailer finalizado de 1-2 minutos",
                                             "Pôster do filme"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Curta-metragem Autoral",
                    "description": "Desenvolver um curta-metragem de 5-8 minutos com maior complexidade técnica e narrativa",
                    "requirements": [
                        "Desenvolvimento completo do roteiro",
                        "Planejamento detalhado de produção",
                        "Direção consciente dos aspectos visuais e sonoros",
                        "Edição com ritmo e coerência narrativa",
                        "Finalização com tratamento de cor e som",
                        "Exibição e discussão com público"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de projetos audiovisuais autorais e exploração de formatos e estéticas",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Estética e Linguagem Cinematográfica",
                        "module_description": "Explore movimentos cinematográficos e desenvolva sua visão estética",
                        "lessons": [
                            {
                                "lesson_title": "História e Movimentos do Cinema",
                                "objectives": "Compreender os principais movimentos e suas características estéticas",
                                "steps": [
                                    "Cinema clássico e linguagem estabelecida",
                                    "Cinema expressionista, nouvelle vague, neorrealismo",
                                    "Cinema contemporâneo e novas tendências",
                                    "Diretores e suas assinaturas visuais"
                                ]
                            },
                            {
                                "lesson_title": "Desenvolvendo Estilo Visual",
                                "objectives": "Criar uma abordagem visual própria e consistente",
                                "steps": [
                                    "Construção da paleta de cores e mood boards",
                                    "Criação de linguagem visual coerente",
                                    "Técnicas avançadas de fotografia e iluminação",
                                    "Referências visuais e influências"
                                ],
                                "project": {
                                    "title": "Estudo de Estilo",
                                    "description": "Criar um curto exercício visual emulando o estilo de um diretor admirado, mas com tema original"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Novas Mídias e Formatos",
                        "module_description": "Explore formas inovadoras de criação audiovisual",
                        "lessons": [
                            {
                                "lesson_title": "Narrativas Transmídia",
                                "objectives": "Compreender e criar histórias que se estendem por múltiplas plataformas",
                                "steps": [
                                    "Conceito de transmídia e suas aplicações",
                                    "Planejamento de universos narrativos expandidos",
                                    "Adaptação de conteúdo para diferentes formatos",
                                    "Estratégias de engajamento do público"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Projeto Transmídia",
                            "description": "Desenvolver um projeto narrativo que se estenda por pelo menos três plataformas diferentes"
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Audiovisual de Portfólio",
                    "description": "Criar uma obra audiovisual mais ambiciosa que demonstre visão autoral e domínio técnico",
                    "requirements": [
                        "Desenvolvimento de projeto original com proposta estética clara",
                        "Execução com atenção à qualidade técnica e artística",
                        "Documentação completa do processo criativo",
                        "Estratégia de divulgação e exibição",
                        "Preparação para festivais ou portfólio profissional"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Animação",
                "description": "Técnicas de criação de animações em diferentes estilos",
                "age_range": "12-17 anos",
                "modules": [
                    "Princípios da Animação",
                    "Stop Motion",
                    "Animação 2D Digital Básica",
                    "Narrativas para Animação"
                ],
                "final_project": {
                    "title": "Curta Animado",
                    "description": "Criar um curta-metragem de animação de 1-3 minutos"
                }
            },
            {
                "name": "Documentário",
                "description": "Técnicas e abordagens para contar histórias reais através do audiovisual",
                "age_range": "14-17 anos",
                "modules": [
                    "Fundamentos do Documentário",
                    "Pesquisa e Preparação",
                    "Entrevistas e Cinema Verdade",
                    "Ética e Responsabilidade no Documentário"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Diretor",
                "Roteirista",
                "Produtor",
                "Diretor de Fotografia",
                "Editor de Vídeo",
                "Sound Designer",
                "Produtor de Conteúdo Digital",
                "Documentarista"
            ],
            "day_in_life": [
                "Um diretor coordena equipes criativas e técnicas para realizar sua visão em um projeto audiovisual",
                "Um editor organiza e monta material bruto para criar narrativas coerentes e impactantes",
                "Um diretor de fotografia trabalha com luz e composição para criar a estética visual de um filme",
                "Um produtor gerencia aspectos logísticos, financeiros e organizacionais de uma produção"
            ],
            "educational_paths": [
                "Graduação em Cinema, Audiovisual ou Comunicação",
                "Cursos técnicos específicos (edição, fotografia, roteiro)",
                "Workshops e oficinas especializadas",
                "Aprendizado prático em sets e produções",
                "Desenvolvimento de portfólio através de projetos independentes"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Artes Visuais básicas"],
            "cross_curricular": ["Literatura", "História", "Tecnologia", "Sociologia", "Música"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Cinema e Audiovisual"] = cinema_audiovisual_subarea
    area_ref.set(area_data)

    return area_data


def setup_musica_instrumentos_musicais_subarea(db):
    """
    Configura a subárea de Instrumentos Musicais dentro da área de Música e Performance,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Música e Performance")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Música e Performance",
            "description": "Descubra o universo dos sons, ritmos e melodias! Aprenda a tocar instrumentos, cantar, compor músicas, mixar, produzir e se apresentar no palco.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    instrumentos_musicais_subarea = {
        "name": "Instrumentos Musicais",
        "description": "Aprenda a tocar e se expressar através de diferentes instrumentos musicais, desenvolvendo técnicas, sensibilidade musical e habilidades de performance.",
        "estimated_time": "6-24 meses (dependendo da dedicação e instrumento escolhido)",
        "icon": "guitar",
        "references": [
            {"title": "Portal da Música", "url": "https://www.portaldemusica.com.br/"},
            {"title": "Music Theory", "url": "https://www.musictheory.net/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos no mundo dos instrumentos musicais, com foco em conceitos básicos e prática inicial",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os princípios básicos da produção sonora nos instrumentos",
                    "Desenvolver coordenação motora e técnicas iniciais de execução",
                    "Ler notação musical básica e tocar melodias simples",
                    "Criar pequenas frases musicais e improvisos simples"
                ],
                "modules": [
                    {
                        "module_title": "Explorando o Mundo dos Instrumentos",
                        "module_description": "Conheça diferentes famílias de instrumentos e suas características",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Famílias de Instrumentos",
                                "objectives": "Conhecer as principais famílias de instrumentos e como produzem som",
                                "estimated_time": "60 minutos",
                                "content_summary": "Exploração das diferentes famílias de instrumentos, suas características e modos de produção sonora",
                                "steps": [
                                    "Cordas: violão, violino, baixo, etc.",
                                    "Sopros: flauta, saxofone, trompete, etc.",
                                    "Percussão: bateria, pandeiro, cajón, etc.",
                                    "Teclados e eletrônicos: piano, sintetizador, etc."
                                ],
                                "exercises": [
                                    {
                                        "question": "Escolha um instrumento de cada família e descreva como o som é produzido nele.",
                                        "type": "open",
                                        "suggested_time": "15 minutos",
                                        "answer": "Resposta pessoal. Exemplos: Violão (cordas) - vibração das cordas amplificada pela caixa de ressonância; Flauta (sopro) - vibração da coluna de ar através do tubo; Tambor (percussão) - vibração da membrana ao ser golpeada; Piano (teclas) - martelinho que golpeia cordas ao pressionar as teclas."
                                    },
                                    {
                                        "question": "Qual dessas características NÃO é comum a todos os instrumentos musicais?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Produzem som",
                                            "Podem ser usados para tocar músicas",
                                            "Possuem cordas",
                                            "Têm algum tipo de controle de altura (grave/agudo)"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "demonstração",
                                        "title": "Feira de Instrumentos",
                                        "description": "Exploração guiada de diferentes instrumentos disponíveis, com demonstração de como produzir som em cada um"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Instrumentos da Orquestra",
                                     "url": "https://exemplo.com/video_orquestra"},
                                    {"type": "infográfico", "title": "Famílias de Instrumentos",
                                     "url": "https://exemplo.com/infografico_instrumentos"}
                                ]
                            },
                            {
                                "lesson_title": "Escolhendo um Instrumento",
                                "objectives": "Orientar na escolha de um instrumento que seja adequado aos interesses e condições do estudante",
                                "estimated_time": "45 minutos",
                                "steps": [
                                    "Considerando seus interesses musicais: estilos e sonoridades",
                                    "Aspectos práticos: custo, tamanho, volume sonoro",
                                    "Características físicas e ergonomia",
                                    "Experimentação e primeira impressão"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são os três fatores mais importantes para você na escolha de um instrumento musical? Por quê?",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Podem mencionar interesse no som, facilidade de aprendizado, custo, transportabilidade, espaço disponível em casa, etc."
                                    }
                                ],
                                "project": {
                                    "title": "Meu Instrumento Ideal",
                                    "description": "Pesquisar e apresentar um relatório sobre o instrumento que mais interessa ao estudante",
                                    "expected_outcome": "Decisão informada sobre qual instrumento começar a estudar",
                                    "estimated_time": "Tarefa para casa - 1 semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Conhecimento de Instrumentos",
                            "format": "Teste de múltipla escolha + identificação auditiva de instrumentos",
                            "passing_score": 70,
                            "time_limit": "30 minutos",
                            "certificate": "Conhecedor de Instrumentos - Nível 1"
                        }
                    },
                    {
                        "module_title": "Primeiros Passos no Instrumento",
                        "module_description": "Aprenda a base técnica e musical para começar a tocar um instrumento",
                        "estimated_time": "8 semanas",
                        "prerequisites": ["Explorando o Mundo dos Instrumentos"],
                        "lessons": [
                            {
                                "lesson_title": "Conhecendo Seu Instrumento",
                                "objectives": "Familiarizar-se com as partes, manuseio e cuidados básicos do instrumento escolhido",
                                "steps": [
                                    "Anatomia do instrumento e nomenclatura das partes",
                                    "Postura correta e ergonomia",
                                    "Produção dos primeiros sons",
                                    "Manutenção e cuidados básicos"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que a postura correta é importante ao tocar um instrumento?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas para ter uma aparência profissional",
                                            "Para prevenir lesões e facilitar a técnica",
                                            "Só é importante para instrumentistas clássicos",
                                            "Não tem importância real na prática"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Diário do Instrumento",
                                    "description": "Criar um guia visual das partes do instrumento e rotina de cuidados básicos",
                                    "steps": [
                                        "Desenhar ou fotografar o instrumento e identificar suas partes",
                                        "Pesquisar e listar os cuidados necessários",
                                        "Criar uma rotina de manutenção",
                                        "Compartilhar com colegas para feedback"
                                    ],
                                    "estimated_time": "60 minutos"
                                }
                            },
                            {
                                "lesson_title": "Leitura Musical Básica",
                                "objectives": "Aprender os fundamentos da notação musical para seu instrumento",
                                "steps": [
                                    "Notas musicais e sua localização no instrumento",
                                    "Pauta, claves e figuras básicas de duração",
                                    "Compassos simples e contagem",
                                    "Aplicação prática: lendo melodias simples"
                                ],
                                "project": {
                                    "title": "Meu Primeiro Repertório",
                                    "description": "Montar uma pasta com 5 músicas simples para praticar, incluindo partituras ou tablaturas adaptadas"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Recital de Iniciação",
                            "description": "Preparar e apresentar uma peça musical muito simples para colegas ou família",
                            "deliverables": ["Apresentação ao vivo ou gravada", "Breve explicação sobre a peça escolhida", "Reflexão sobre a experiência"],
                            "estimated_time": "Preparação de 3 semanas + apresentação"
                        }
                    }
                ],
                "final_project": {
                    "title": "Meu Primeiro Repertório Musical",
                    "description": "Preparar e apresentar um pequeno conjunto de peças musicais básicas",
                    "requirements": [
                        "Domínio técnico básico do instrumento escolhido",
                        "Execução de 3-5 peças simples com diferentes características",
                        "Demonstração de leitura musical básica",
                        "Apresentação para pequeno público (colegas, familiares)",
                        "Reflexão sobre o processo de aprendizado"
                    ],
                    "rubric": "Avaliação baseada em técnica básica, musicalidade, progresso individual e dedicação",
                    "showcase": "Recital coletivo dos estudantes"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Instrumento",
                    "format": "Performance das peças + teste teórico básico + autoavaliação",
                    "passing_criteria": "Demonstração de domínio técnico básico e compreensão musical fundamental",
                    "certification": "Instrumentista Iniciante"
                },
                "suggested_path_forward": ["Técnicas Intermediárias", "Teoria Musical Aplicada", "Prática em Conjunto"]
            },
            "intermediario": {
                "description": "Aprofundamento técnico no instrumento e desenvolvimento de repertório mais complexo",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Desenvolvimento Técnico",
                        "module_description": "Aprimore sua técnica instrumental e expanda suas possibilidades expressivas",
                        "estimated_time": "12 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Técnicas Específicas do Instrumento",
                                "objectives": "Dominar técnicas intermediárias específicas para seu instrumento",
                                "steps": [
                                    "Exercícios técnicos progressivos",
                                    "Articulações e expressividade",
                                    "Ampliação da extensão e controle dinâmico",
                                    "Resolução de dificuldades técnicas comuns"
                                ]
                            },
                            {
                                "lesson_title": "Sonoridade e Expressão",
                                "objectives": "Desenvolver qualidade sonora e expressividade musical",
                                "steps": [
                                    "Controle tímbrico e sonoro",
                                    "Fraseado e respiração musical",
                                    "Expressão de diferentes caracteres e emoções",
                                    "Desenvolvimento de estilo pessoal"
                                ],
                                "project": {
                                    "title": "Estudo Expressivo",
                                    "description": "Preparar uma peça com foco na expressividade e qualidade sonora"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Ampliação de Repertório",
                        "module_description": "Explore diferentes estilos e períodos musicais através do seu instrumento",
                        "estimated_time": "16 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Explorando Gêneros Musicais",
                                "objectives": "Conhecer e praticar diferentes estilos no seu instrumento",
                                "steps": [
                                    "Características e técnicas de cada gênero",
                                    "Repertório representativo adaptado ao nível",
                                    "Audição crítica de referências",
                                    "Adaptação estilística e interpretativa"
                                ]
                            },
                            {
                                "lesson_title": "Montagem de Repertório",
                                "objectives": "Aprender a estudar e preparar peças de forma eficiente",
                                "steps": [
                                    "Estratégias de estudo eficiente",
                                    "Divisão em seções e progressão gradual",
                                    "Solução de trechos difíceis",
                                    "Memorização e preparação para performance"
                                ],
                                "project": {
                                    "title": "Recital Temático",
                                    "description": "Preparar um pequeno conjunto de peças de um gênero ou período específico"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Meu Repertório Diversificado",
                            "description": "Montar e apresentar um programa com peças de diferentes períodos ou estilos",
                            "deliverables": ["Performance ao vivo ou gravada", "Notas de programa com contextualização", "Reflexão sobre os desafios de cada estilo"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Recital Intermediário",
                    "description": "Preparar e apresentar um recital com repertório de nível intermediário",
                    "requirements": [
                        "Programa de 15-20 minutos com peças variadas",
                        "Demonstração de domínio técnico adequado ao nível",
                        "Expressividade e compreensão estilística",
                        "Notas de programa com contextualização das obras",
                        "Apresentação formal para público convidado"
                    ]
                }
            },
            "avancado": {
                "description": "Refinamento técnico-musical e desenvolvimento de projetos artísticos pessoais",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Técnica Avançada",
                        "module_description": "Refine sua técnica instrumental para enfrentar desafios de repertório avançado",
                        "lessons": [
                            {
                                "lesson_title": "Virtuosismo e Complexidade",
                                "objectives": "Dominar técnicas avançadas necessárias para repertório desafiador",
                                "steps": [
                                    "Técnicas estendidas e especializadas",
                                    "Velocidade, precisão e resistência",
                                    "Passagens complexas: estratégias de estudo",
                                    "Polirritmos e coordenação avançada"
                                ]
                            },
                            {
                                "lesson_title": "Refinamento Interpretativo",
                                "objectives": "Desenvolver profundidade interpretativa e maturidade musical",
                                "steps": [
                                    "Análise musical como ferramenta interpretativa",
                                    "Tradições performáticas e pesquisa histórica",
                                    "Gravação e autoavaliação crítica",
                                    "Construção de interpretação pessoal fundamentada"
                                ],
                                "project": {
                                    "title": "Estudo Comparativo",
                                    "description": "Analisar diferentes interpretações de uma mesma obra e desenvolver versão própria"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Projetos Musicais Autorais",
                        "module_description": "Desenvolva sua voz musical através de projetos criativos",
                        "lessons": [
                            {
                                "lesson_title": "Da Interpretação à Criação",
                                "objectives": "Explorar a ponte entre interpretação e criação musical",
                                "steps": [
                                    "Improvisação estruturada e livre",
                                    "Arranjos e adaptações",
                                    "Composição para seu instrumento",
                                    "Experimentação sonora e técnicas estendidas"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Projeto Artístico Pessoal",
                            "description": "Criar um projeto que reflita sua identidade musical, envolvendo interpretação, arranjo ou composição"
                        }
                    }
                ],
                "final_project": {
                    "title": "Recital Solo",
                    "description": "Preparar e apresentar um recital solo completo com repertório avançado",
                    "requirements": [
                        "Programa de 30-45 minutos mostrando versatilidade",
                        "Inclusão de obras tecnicamente desafiadoras",
                        "Domínio técnico e interpretativo de alto nível",
                        "Produção completa: programação, divulgação, apresentação",
                        "Gravação profissional para portfólio"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Piano e Teclados",
                "description": "Técnicas e repertório específicos para instrumentos de teclas",
                "age_range": "10-17 anos",
                "modules": [
                    "Técnica Pianística Fundamental",
                    "Repertório Clássico para Piano",
                    "Piano em Música Popular",
                    "Acompanhamento e Harmonia Aplicada"
                ],
                "final_project": {
                    "title": "Recital de Piano",
                    "description": "Preparar um recital com obras representativas de diferentes períodos e estilos"
                }
            },
            {
                "name": "Violão e Cordas Dedilhadas",
                "description": "Técnicas e repertório para violão, guitarra e instrumentos similares",
                "age_range": "10-17 anos",
                "modules": [
                    "Técnicas de Mão Direita e Esquerda",
                    "Harmonia Aplicada ao Violão",
                    "Estilos e Gêneros no Violão",
                    "Arranjos e Transcrições"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Instrumentista Solista",
                "Músico de Orquestra/Banda",
                "Professor de Música",
                "Músico de Estúdio",
                "Arranjador",
                "Compositor",
                "Luthier/Técnico de Instrumentos",
                "Produtor Musical"
            ],
            "day_in_life": [
                "Um instrumentista profissional divide seu tempo entre prática individual, ensaios em grupo e apresentações",
                "Um professor de instrumento planeja aulas, desenvolve material didático e acompanha o progresso dos alunos",
                "Um músico de estúdio precisa ler e interpretar partituras com precisão e adaptar-se rapidamente a diferentes estilos",
                "Um luthier trabalha na construção, reparo e manutenção de instrumentos, combinando habilidades artesanais e conhecimento acústico"
            ],
            "educational_paths": [
                "Conservatórios e escolas de música",
                "Graduação em Música (Bacharelado em Instrumento)",
                "Cursos livres e workshops especializados",
                "Aulas particulares com mestres reconhecidos",
                "Festivais e masterclasses"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Música básica"],
            "cross_curricular": ["Física (acústica)", "História", "Matemática", "Educação Física (coordenação motora)"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Instrumentos Musicais"] = instrumentos_musicais_subarea
    area_ref.set(area_data)

    return area_data


def setup_musica_canto_vocal_subarea(db):
    """
    Configura a subárea de Canto e Técnica Vocal dentro da área de Música e Performance,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Música e Performance")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Música e Performance",
            "description": "Descubra o universo dos sons, ritmos e melodias! Aprenda a tocar instrumentos, cantar, compor músicas, mixar, produzir e se apresentar no palco.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    canto_vocal_subarea = {
        "name": "Canto e Técnica Vocal",
        "description": "Descubra e desenvolva seu potencial vocal através de técnicas e práticas que ajudarão você a cantar com mais qualidade, expressividade e saúde vocal.",
        "estimated_time": "6-18 meses (dependendo da dedicação)",
        "icon": "microphone",
        "references": [
            {"title": "Academia de Canto", "url": "https://www.academiadecanto.com.br/"},
            {"title": "Vocalist.org", "url": "https://www.vocalist.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos na descoberta e desenvolvimento da voz cantada",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os fundamentos da produção vocal e do aparelho fonador",
                    "Desenvolver consciência corporal e respiratória para o canto",
                    "Explorar diferentes qualidades e possibilidades vocais",
                    "Cantar melodias simples com afinação e expressividade básicas"
                ],
                "modules": [
                    {
                        "module_title": "Descobrindo sua Voz",
                        "module_description": "Explore o funcionamento da voz e comece a desenvolver sua consciência vocal",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Como Funciona a Voz",
                                "objectives": "Compreender o mecanismo de produção vocal e cuidados básicos",
                                "estimated_time": "60 minutos",
                                "content_summary": "Introdução ao aparelho fonador e funcionamento básico da voz cantada",
                                "steps": [
                                    "Anatomia básica da voz: pregas vocais, laringe, aparelho respiratório",
                                    "Como o som é produzido e amplificado no corpo",
                                    "Diferenças entre voz falada e cantada",
                                    "Higiene e saúde vocal para iniciantes"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são as três partes principais do sistema que produz nossa voz?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Boca, nariz e orelhas",
                                            "Sistema respiratório, laringe (pregas vocais) e ressoadores",
                                            "Pulmões, coração e garganta",
                                            "Língua, dentes e lábios"
                                        ],
                                        "correct_answer": 1
                                    },
                                    {
                                        "question": "Descreva dois hábitos que prejudicam a saúde vocal e dois que a beneficiam.",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Respostas podem incluir: Prejudiciais - gritar, falar muito alto, pigarrear, não beber água suficiente, fumar, bebidas com cafeína/álcool. Benéficos - hidratação adequada, descanso vocal, aquecimento vocal antes de cantar, boa postura, evitar alimentos que causam refluxo."
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "demonstração",
                                        "title": "Explorando Vibrações",
                                        "description": "Sentir as vibrações vocais em diferentes partes do corpo com exercícios guiados"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Como sua Voz Funciona",
                                     "url": "https://exemplo.com/video_voz"},
                                    {"type": "infográfico", "title": "Mapa do Sistema Vocal",
                                     "url": "https://exemplo.com/infografico_voz"}
                                ]
                            },
                            {
                                "lesson_title": "Respiração para o Canto",
                                "objectives": "Aprender a respirar de forma eficiente para sustentar o canto",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "Respiração diafragmática vs. respiração de peito",
                                    "Exercícios para desenvolver controle respiratório",
                                    "Apoio e sustentação do som",
                                    "Gerenciamento do ar durante frases musicais"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que a respiração diafragmática é mais eficiente para cantar do que a respiração alta (de peito)?",
                                        "type": "open",
                                        "answer": "A respiração diafragmática permite maior capacidade de ar, melhor controle da expiração, maior estabilidade vocal, menos tensão na região da garganta e maior sustentação de notas."
                                    }
                                ],
                                "project": {
                                    "title": "Diário da Respiração",
                                    "description": "Praticar exercícios respiratórios diariamente por uma semana e registrar sensações e progressos",
                                    "expected_outcome": "Maior consciência e controle respiratório para o canto",
                                    "estimated_time": "10 minutos diários por uma semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Fundamentos da Voz",
                            "format": "Demonstração prática + quiz sobre conhecimentos básicos",
                            "passing_score": "Demonstração de compreensão dos conceitos básicos",
                            "time_limit": "30 minutos",
                            "certificate": "Explorador Vocal - Nível 1"
                        }
                    },
                    {
                        "module_title": "Primeiros Passos no Canto",
                        "module_description": "Desenvolva habilidades básicas para começar a cantar com mais segurança",
                        "estimated_time": "6 semanas",
                        "prerequisites": ["Descobrindo sua Voz"],
                        "lessons": [
                            {
                                "lesson_title": "Afinação e Percepção Musical",
                                "objectives": "Desenvolver a capacidade de cantar afinado e reconhecer alturas",
                                "steps": [
                                    "Como ouvir e reproduzir notas com precisão",
                                    "Exercícios para melhorar a percepção de afinação",
                                    "Relação entre audição e produção vocal",
                                    "Estratégias para corrigir problemas comuns de afinação"
                                ],
                                "exercises": [
                                    {
                                        "question": "Que estratégias você pode usar quando percebe que está cantando desafinado em uma determinada passagem?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Cantar mais forte para mascarar o problema",
                                            "Desistir da música e escolher outra mais fácil",
                                            "Isolar a passagem, diminuir o andamento e praticar com um instrumento de referência",
                                            "Pedir para alguém cantar por você nessa parte"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "project": {
                                    "title": "Diário de Afinação",
                                    "description": "Gravar-se cantando uma melodia simples diariamente por uma semana, analisando e ajustando a afinação a cada dia",
                                    "steps": [
                                        "Escolher uma melodia simples e familiar",
                                        "Gravar a performance vocal diariamente",
                                        "Ouvir com atenção e identificar áreas para melhorar",
                                        "Ajustar e regravar, comparando os resultados"
                                    ],
                                    "estimated_time": "15 minutos diários por uma semana"
                                }
                            },
                            {
                                "lesson_title": "Articulação e Dicção",
                                "objectives": "Melhorar a clareza das palavras cantadas",
                                "steps": [
                                    "Exercícios para fortalecimento e flexibilidade da língua e lábios",
                                    "Pronúncia clara de vogais e consoantes",
                                    "Desafios comuns na articulação durante o canto",
                                    "Equilíbrio entre articulação e fluxo melódico"
                                ],
                                "project": {
                                    "title": "Ginástica Articulatória",
                                    "description": "Criar uma rotina pessoal de exercícios de articulação usando trava-línguas e textos desafiadores"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Minha Primeira Canção",
                            "description": "Preparar e apresentar uma canção simples aplicando os conceitos aprendidos",
                            "deliverables": ["Apresentação ao vivo ou gravada da canção", "Análise escrita do processo de preparação", "Identificação de pontos fortes e desafios"],
                            "estimated_time": "3 semanas de preparação + apresentação"
                        }
                    }
                ],
                "final_project": {
                    "title": "Mini-Recital Vocal",
                    "description": "Preparar e apresentar um conjunto de 2-3 canções que demonstrem o desenvolvimento vocal básico",
                    "requirements": [
                        "Seleção de canções adequadas ao nível e tipo vocal",
                        "Demonstração de respiração adequada e postura",
                        "Afinação consistente nas melodias simples",
                        "Articulação clara do texto",
                        "Expressividade vocal básica"
                    ],
                    "rubric": "Avaliação baseada em técnica básica, afinação, articulação, expressividade e progresso individual",
                    "showcase": "Apresentação para pequeno público (colegas, familiares)"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Canto",
                    "format": "Performance das canções + demonstração de exercícios básicos + autoavaliação",
                    "passing_criteria": "Demonstração de compreensão dos fundamentos e progresso vocal individual",
                    "certification": "Cantor Iniciante"
                },
                "suggested_path_forward": ["Técnica Vocal Intermediária", "Estilos Vocais", "Canto em Grupo"]
            },
            "intermediario": {
                "description": "Aprofundamento técnico e expressivo da voz cantada, com expansão de repertório",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Técnica Vocal Intermediária",
                        "module_description": "Aprofunde sua compreensão e domínio da técnica vocal",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Registros Vocais e Passagens",
                                "objectives": "Compreender e integrar os diferentes registros da voz",
                                "steps": [
                                    "Identificação dos registros: peito, misto e cabeça",
                                    "Exercícios para suavizar as passagens entre registros",
                                    "Desenvolvimento da voz mista",
                                    "Expansão da extensão vocal com segurança"
                                ]
                            },
                            {
                                "lesson_title": "Ressonância e Projeção",
                                "objectives": "Desenvolver uma voz mais rica e projetada",
                                "steps": [
                                    "Compreensão dos ressoadores faciais e corporais",
                                    "Exercícios para ativar diferentes espaços de ressonância",
                                    "Equilíbrio entre brilho e corpo na voz",
                                    "Projeção vocal saudável sem esforço"
                                ],
                                "project": {
                                    "title": "Mapa de Ressonância",
                                    "description": "Explorar e documentar como diferentes vogais e técnicas afetam a ressonância vocal"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Expressão e Interpretação",
                        "module_description": "Desenvolva sua capacidade de comunicar emoções e histórias através da voz",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Dinâmica e Coloratura Vocal",
                                "objectives": "Explorar a gama de cores e intensidades da voz",
                                "steps": [
                                    "Controle de dinâmicas: do piano ao forte",
                                    "Variações timbrísticas para expressão",
                                    "Técnicas de coloratura e ornamentação básica",
                                    "Aplicação expressiva em diferentes contextos musicais"
                                ]
                            },
                            {
                                "lesson_title": "Interpretação e Presença",
                                "objectives": "Desenvolver a capacidade de interpretar canções com profundidade",
                                "steps": [
                                    "Análise de letra e contexto da música",
                                    "Conexão emocional com o material",
                                    "Comunicação não-verbal e presença de palco",
                                    "Equilíbrio entre técnica e entrega emocional"
                                ],
                                "project": {
                                    "title": "Estudo Interpretativo",
                                    "description": "Preparar duas versões contrastantes da mesma canção, explorando diferentes abordagens interpretativas"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Performance Temática",
                            "description": "Criar uma pequena performance baseada em um tema ou conceito, com 2-3 canções relacionadas",
                            "deliverables": ["Performance ao vivo ou gravada", "Texto explicativo do conceito", "Análise das escolhas interpretativas"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Recital Intermediário",
                    "description": "Preparar e apresentar um recital com repertório variado que demonstre desenvolvimento técnico e expressivo",
                    "requirements": [
                        "Programa de 15-20 minutos com pelo menos 4 canções",
                        "Demonstração de controle técnico intermediário",
                        "Variedade estilística e expressiva",
                        "Presença cênica e comunicação com o público",
                        "Notas de programa contextualizando as obras"
                    ]
                }
            },
            "avancado": {
                "description": "Refinamento técnico-vocal e desenvolvimento de projetos artísticos vocais mais complexos",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Técnica Vocal Avançada",
                        "module_description": "Refine sua técnica vocal para enfrentar desafios de repertório mais complexo",
                        "lessons": [
                            {
                                "lesson_title": "Controle e Virtuosidade",
                                "objectives": "Desenvolver controle refinado sobre todos os aspectos da voz",
                                "steps": [
                                    "Agilidade e coloratura avançada",
                                    "Controle refinado de vibrato",
                                    "Extensão vocal expandida",
                                    "Equilíbrio e homogeneidade em toda a extensão"
                                ]
                            },
                            {
                                "lesson_title": "Técnicas Específicas de Estilo",
                                "objectives": "Dominar técnicas vocais específicas para diferentes gêneros musicais",
                                "steps": [
                                    "Técnicas para música popular: belting, riff, twang",
                                    "Técnicas para música clássica: legato, messa di voce",
                                    "Técnicas para música étnica e world music",
                                    "Adaptação vocal para demandas estilísticas"
                                ],
                                "project": {
                                    "title": "Versatilidade Estilística",
                                    "description": "Preparar uma demonstração de diferentes técnicas vocais aplicadas em estilos contrastantes"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Projetos Artísticos Vocais",
                        "module_description": "Desenvolva projetos vocais originais que reflitam sua identidade artística",
                        "lessons": [
                            {
                                "lesson_title": "Identidade Vocal e Autoria",
                                "objectives": "Desenvolver uma assinatura vocal e expressiva pessoal",
                                "steps": [
                                    "Identificação de características vocais únicas",
                                    "Experimentação e definição de preferências estilísticas",
                                    "Adaptação e arranjo de repertório para sua voz",
                                    "Composição ou co-criação de material original"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Showcase Autoral",
                            "description": "Criar uma performance que destaque sua identidade vocal, incluindo pelo menos uma peça original ou arranjo próprio",
                            "deliverables": ["Performance gravada ou ao vivo", "Documentação do processo criativo", "Reflexão sobre a jornada vocal"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Recital Solo",
                    "description": "Preparar e apresentar um recital solo completo que demonstre domínio técnico e artístico da voz",
                    "requirements": [
                        "Programa de 30-45 minutos com repertório diversificado",
                        "Domínio técnico avançado apropriado ao estilo",
                        "Coerência artística e proposta conceitual",
                        "Produção completa: programação, divulgação, apresentação",
                        "Gravação profissional para portfólio"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Canto Popular",
                "description": "Técnicas e repertório específicos para estilos populares como pop, rock, MPB, jazz e blues",
                "age_range": "12-17 anos",
                "modules": [
                    "Estilos e Técnicas da Música Popular",
                    "Microfone e Amplificação",
                    "Improviso e Scat",
                    "Backing Vocals e Harmonização"
                ],
                "final_project": {
                    "title": "Show de Música Popular",
                    "description": "Montar um show com repertório de música popular demonstrando domínio estilístico"
                }
            },
            {
                "name": "Canto Coral",
                "description": "Desenvolvimento de habilidades específicas para canto em grupo e coral",
                "age_range": "10-17 anos",
                "modules": [
                    "Técnica Vocal para Coro",
                    "Afinação e Blend Coral",
                    "Repertório Coral Diversificado",
                    "Performance Coral e Movimentação Cênica"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Cantor Solista",
                "Cantor de Coro/Grupo Vocal",
                "Professor de Canto",
                "Preparador Vocal",
                "Dublador",
                "Compositor/Letrista",
                "Diretor Vocal",
                "Terapeuta Vocal"
            ],
            "day_in_life": [
                "Um cantor profissional dedica tempo diário à manutenção vocal, estudo de repertório e ensaios",
                "Um professor de canto avalia as necessidades individuais de cada aluno e cria planos de desenvolvimento vocal personalizados",
                "Um cantor de grupo vocal trabalha no blend e harmonia com outros cantores e adapta sua voz para o conjunto",
                "Um preparador vocal para teatro musical ou coral trabalha com aspectos técnicos e interpretativos para preparar cantores para performances específicas"
            ],
            "educational_paths": [
                "Conservatórios e escolas de música com foco em canto",
                "Graduação em Música (Bacharelado em Canto)",
                "Cursos livres e workshops especializados em técnica vocal",
                "Formação em pedagogia vocal",
                "Estudo com professores particulares especializados"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Música básica"],
            "cross_curricular": ["Literatura (interpretação de texto)", "Teatro", "Biologia (aparelho fonador)", "Idiomas"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Canto e Técnica Vocal"] = canto_vocal_subarea
    area_ref.set(area_data)

    return area_data



def setup_musica_producao_musical_subarea(db):
    """
    Configura a subárea de Produção Musical dentro da área de Música e Performance,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Música e Performance")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Música e Performance",
            "description": "Descubra o universo dos sons, ritmos e melodias! Aprenda a tocar instrumentos, cantar, compor músicas, mixar, produzir e se apresentar no palco.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    producao_musical_subarea = {
        "name": "Produção Musical",
        "description": "Aprenda a gravar, mixar e produzir música em ambiente digital, combinando tecnologia e criatividade para transformar ideias musicais em produções finalizadas.",
        "estimated_time": "6-18 meses (dependendo da dedicação)",
        "icon": "sliders",
        "references": [
            {"title": "Portal da Produção Musical", "url": "https://www.portaldaproducao.com.br/"},
            {"title": "Music Production Academy", "url": "https://www.musicproductionacademy.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Primeiros passos no mundo da produção musical digital",
                "age_range": "12-14 anos",
                "learning_outcomes": [
                    "Compreender os fundamentos básicos da produção musical digital",
                    "Operar software de produção musical (DAW) em nível básico",
                    "Capturar e editar áudio e MIDI de forma simples",
                    "Criar pequenos arranjos e beats utilizando loops e samples"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos da Produção Musical",
                        "module_description": "Conheça os conceitos básicos e ferramentas da produção musical moderna",
                        "estimated_time": "4 semanas",
                        "difficulty": "médio",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Introdução ao Estúdio Digital",
                                "objectives": "Compreender os componentes básicos de um estúdio digital e home studio",
                                "estimated_time": "60 minutos",
                                "content_summary": "Visão geral do mundo da produção musical digital e suas possibilidades",
                                "steps": [
                                    "O que é uma DAW (Digital Audio Workstation) e suas funções",
                                    "Equipamentos essenciais: computador, interface de áudio, monitores, fones, MIDI",
                                    "Fluxo de trabalho básico: do conceito à produção finalizada",
                                    "Possibilidades criativas da produção digital"
                                ],
                                "exercises": [
                                    {
                                        "question": "Explique a diferença entre áudio e MIDI em um ambiente de produção musical.",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Áudio é o som gravado (ondas sonoras capturadas e digitalizadas), enquanto MIDI é uma linguagem de comunicação musical que não contém som, apenas instruções sobre quais notas tocar, com qual intensidade, duração, etc. O MIDI precisa ser associado a um instrumento virtual ou hardware para produzir som."
                                    },
                                    {
                                        "question": "Qual dos seguintes NÃO é um componente típico de um home studio básico?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Interface de áudio",
                                            "Microfone",
                                            "Câmara de reverberação analógica",
                                            "Fones de ouvido"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "demonstração",
                                        "title": "Tour Virtual pelo Estúdio",
                                        "description": "Exploração guiada dos componentes de um estúdio digital, com demonstração de suas funções"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Montando seu Primeiro Home Studio",
                                     "url": "https://exemplo.com/video_homestudio"},
                                    {"type": "infográfico", "title": "Anatomia de uma DAW",
                                     "url": "https://exemplo.com/infografico_daw"}
                                ]
                            },
                            {
                                "lesson_title": "Primeiros Passos na DAW",
                                "objectives": "Aprender a navegar e utilizar funções básicas de uma DAW",
                                "estimated_time": "75 minutos",
                                "steps": [
                                    "Interface e navegação básica na DAW",
                                    "Criação de projeto: configurações iniciais",
                                    "Trabalhando com faixas, regiões e eventos",
                                    "Ferramentas básicas de edição e navegação temporal"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que é importante definir o tempo (BPM) e a tonalidade do seu projeto logo no início?",
                                        "type": "open",
                                        "answer": "Definir o tempo e a tonalidade no início ajuda a manter a consistência musical, facilita o trabalho com loops e samples que se adaptarão automaticamente, possibilita o uso de ferramentas de quantização e correção, e simplifica a integração de instrumentos virtuais e MIDI."
                                    }
                                ],
                                "project": {
                                    "title": "Exploração da DAW",
                                    "description": "Criar um novo projeto e experimentar diferentes funcionalidades básicas da DAW escolhida",
                                    "expected_outcome": "Familiarização com a interface e operações básicas",
                                    "estimated_time": "45 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Quiz: Fundamentos da Produção",
                            "format": "Teste prático na DAW + perguntas sobre conceitos básicos",
                            "passing_score": "Demonstração de compreensão dos conceitos básicos",
                            "time_limit": "45 minutos",
                            "certificate": "Produtor Iniciante - Nível 1"
                        }
                    },
                    {
                        "module_title": "Criando sua Primeira Música",
                        "module_description": "Aprenda a construir uma música usando loops, samples e instrumentos virtuais",
                        "estimated_time": "6 semanas",
                        "prerequisites": ["Fundamentos da Produção Musical"],
                        "lessons": [
                            {
                                "lesson_title": "Trabalhando com Loops e Samples",
                                "objectives": "Aprender a utilizar material pré-gravado para construir beats e arranjos",
                                "steps": [
                                    "Tipos de loops: bateria, baixo, melodia, efeitos",
                                    "Biblioteca de loops e organização de samples",
                                    "Manipulação básica: corte, repetição, pitch, tempo",
                                    "Construção de grooves e seções usando loops"
                                ],
                                "exercises": [
                                    {
                                        "question": "Que critérios você deve considerar ao escolher loops para usar em um projeto?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas a duração do loop",
                                            "Tonalidade, tempo (BPM) e estilo musical",
                                            "Apenas o volume do loop",
                                            "A marca da empresa que criou o loop"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Beat com Loops",
                                    "description": "Criar um beat de 8 compassos utilizando loops de bateria, baixo e outros elementos",
                                    "steps": [
                                        "Selecionar loops compatíveis em tonalidade e estilo",
                                        "Organizar em camadas (bateria, baixo, harmonia, melodia)",
                                        "Aplicar edições básicas para criar variações",
                                        "Estruturar em uma sequência musical coerente"
                                    ],
                                    "estimated_time": "90 minutos"
                                }
                            },
                            {
                                "lesson_title": "Instrumentos Virtuais Básicos",
                                "objectives": "Aprender a usar instrumentos virtuais e criar partes MIDI simples",
                                "steps": [
                                    "O que são instrumentos virtuais e como funcionam",
                                    "Criação e edição básica de MIDI",
                                    "Piano roll e sequenciamento de notas",
                                    "Seleção de sons e presets adequados"
                                ],
                                "project": {
                                    "title": "Melodia com MIDI",
                                    "description": "Criar uma linha melódica simples usando instrumento virtual e edição MIDI"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Miniprodução Musical",
                            "description": "Criar uma música curta (1-2 minutos) combinando loops e partes de instrumentos virtuais",
                            "deliverables": ["Arquivo do projeto na DAW", "Exportação em MP3 da música finalizada", "Documentação do processo criativo"],
                            "estimated_time": "3 semanas (incluindo planejamento, produção e finalização)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Minha Primeira Produção Completa",
                    "description": "Criar uma música original de 2-3 minutos utilizando as técnicas aprendidas",
                    "requirements": [
                        "Utilização adequada de loops e samples",
                        "Inclusão de pelo menos uma parte criada com instrumento virtual (MIDI)",
                        "Estrutura musical clara (introdução, versos, refrão, etc.)",
                        "Edição básica para criar interesse e variação",
                        "Mixagem simples com níveis de volume equilibrados",
                        "Exportação em formato de áudio de alta qualidade"
                    ],
                    "rubric": "Avaliação baseada em criatividade, estrutura musical, uso técnico das ferramentas e qualidade sonora básica",
                    "showcase": "Compilação das produções da turma em um álbum digital"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos da Produção Musical",
                    "format": "Projeto final + demonstração prática de habilidades + autoavaliação",
                    "passing_criteria": "Demonstração de compreensão dos fundamentos e capacidade de criar uma produção simples",
                    "certification": "Produtor Musical Iniciante"
                },
                "suggested_path_forward": ["Técnicas de Gravação", "Mixagem Básica", "Produção em Estilos Específicos"]
            },
            "intermediario": {
                "description": "Aprofundamento em técnicas de gravação, edição e arranjo para produções mais sofisticadas",
                "age_range": "13-16 anos",
                "modules": [
                    {
                        "module_title": "Gravação e Edição de Áudio",
                        "module_description": "Aprenda a capturar e manipular áudio com qualidade",
                        "estimated_time": "7 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos da Gravação",
                                "objectives": "Compreender e aplicar técnicas básicas de gravação de áudio",
                                "steps": [
                                    "Tipos de microfones e suas aplicações",
                                    "Posicionamento de microfones para diferentes fontes",
                                    "Configuração de níveis e prevenção de distorção",
                                    "Criação de ambiente adequado para gravação"
                                ]
                            },
                            {
                                "lesson_title": "Edição de Áudio Avançada",
                                "objectives": "Dominar ferramentas e técnicas de edição para refinar gravações",
                                "steps": [
                                    "Corte e montagem precisa de regiões de áudio",
                                    "Correção de timing e pitch",
                                    "Remoção de ruídos e imperfeições",
                                    "Comping: combinando as melhores partes de múltiplas tomadas"
                                ],
                                "project": {
                                    "title": "Sessão de Gravação",
                                    "description": "Gravar um instrumento ou voz e aplicar técnicas de edição para refinamento"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Arranjo e Produção",
                        "module_description": "Desenvolva habilidades para criar arranjos musicais completos",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Elementos do Arranjo Musical",
                                "objectives": "Compreender os componentes que formam um arranjo eficaz",
                                "steps": [
                                    "Funções dos instrumentos no arranjo",
                                    "Camadas sonoras: base, harmonia, melodia, ornamentos",
                                    "Desenvolvimento de seções e estrutura musical",
                                    "Criação de interesse e dinâmica através do arranjo"
                                ]
                            },
                            {
                                "lesson_title": "Produção em Diferentes Gêneros",
                                "objectives": "Aprender características de produção específicas para diferentes estilos musicais",
                                "steps": [
                                    "Elementos característicos de gêneros populares",
                                    "Escolha de instrumentos e timbres apropriados ao estilo",
                                    "Técnicas de produção específicas por gênero",
                                    "Referências e análise de produções profissionais"
                                ],
                                "project": {
                                    "title": "Produção Estilística",
                                    "description": "Criar uma produção curta dentro de um gênero específico, seguindo suas convenções"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Remake de uma Música",
                            "description": "Criar uma nova versão ou interpretação de uma música existente, com arranjo e produção original",
                            "deliverables": ["Projeto completo na DAW", "Áudio exportado em alta qualidade", "Análise comparativa com a versão original"]
                        }
                    }
                ],
                "final_project": {
                    "title": "EP de Produção Original",
                    "description": "Criar uma coleção de 2-3 músicas originais que demonstrem habilidades de produção e arranjo",
                    "requirements": [
                        "Composições originais ou colaborativas",
                        "Gravação de elementos reais (voz ou instrumentos)",
                        "Arranjos completos com múltiplas camadas e seções",
                        "Edição refinada e atenção aos detalhes",
                        "Mixagem básica com processamento de efeitos",
                        "Conceito unificador entre as faixas"
                    ]
                }
            },
            "avancado": {
                "description": "Domínio das técnicas de mixagem, masterização e produção profissional",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Mixagem Avançada",
                        "module_description": "Aprenda a transformar gravações brutas em mixagens polidas e balanceadas",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos da Mixagem",
                                "objectives": "Compreender os princípios e ferramentas essenciais da mixagem",
                                "steps": [
                                    "Preparação da sessão para mixagem",
                                    "Balanceamento de volumes e panorama",
                                    "EQ: moldando o espectro de frequências",
                                    "Compressão: controle de dinâmica e caráter"
                                ]
                            },
                            {
                                "lesson_title": "Processamento de Efeitos",
                                "objectives": "Utilizar efeitos para criar profundidade e interesse na mixagem",
                                "steps": [
                                    "Reverb: criando espaço e profundidade",
                                    "Delay: ecos, repetições e efeitos rítmicos",
                                    "Modulação: chorus, flanger, phaser",
                                    "Automação de efeitos para movimento e evolução"
                                ],
                                "project": {
                                    "title": "Mixagem Detalhada",
                                    "description": "Realizar a mixagem completa de uma música multifaixa, aplicando técnicas avançadas"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Produção Profissional",
                        "module_description": "Desenvolva projetos de nível profissional e prepare-se para o mercado",
                        "lessons": [
                            {
                                "lesson_title": "Masterização Básica",
                                "objectives": "Aprender os fundamentos do processo final de polimento do áudio",
                                "steps": [
                                    "O que é masterização e seu propósito",
                                    "Ferramentas básicas: EQ, compressão, limitação",
                                    "Considerações de loudness e dinâmica",
                                    "Preparação para diferentes plataformas e formatos"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Portfólio de Produção",
                            "description": "Criar um showcase de produções finalizadas em diferentes estilos e aplicações",
                            "deliverables": ["3-5 produções em diferentes contextos", "Apresentação profissional do trabalho", "Documentação técnica do processo"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Produção Profissional",
                    "description": "Realizar a produção completa de um projeto musical substancial com qualidade profissional",
                    "requirements": [
                        "Planejamento completo da produção",
                        "Gravações de alta qualidade",
                        "Arranjos sofisticados e detalhados",
                        "Edição meticulosa e refinada",
                        "Mixagem profissional com uso avançado de processamento",
                        "Masterização adequada para o meio de distribuição pretendido",
                        "Documentação completa do processo"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Beatmaking e Produção Eletrônica",
                "description": "Foco na criação de beats, bases e música eletrônica utilizando técnicas digitais",
                "age_range": "13-17 anos",
                "modules": [
                    "Fundamentos do Beatmaking",
                    "Sound Design e Síntese",
                    "Ritmos e Programação de Bateria",
                    "Arranjo Eletrônico"
                ],
                "final_project": {
                    "title": "EP de Música Eletrônica",
                    "description": "Criar um EP original de música eletrônica demonstrando técnicas avançadas de produção"
                }
            },
            {
                "name": "Produção para Mídia e Trilhas Sonoras",
                "description": "Produção musical voltada para audiovisual, jogos e outras mídias",
                "age_range": "14-17 anos",
                "modules": [
                    "Música para Imagem",
                    "Sound Design para Mídia",
                    "Técnicas de Composição para Trilhas",
                    "Produção e Implementação"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Produtor Musical",
                "Engenheiro de Som",
                "Compositor para Mídia",
                "Beatmaker",
                "Sound Designer",
                "Técnico de Estúdio",
                "DJ/Remixer",
                "Produtor de Podcast/Áudio"
            ],
            "day_in_life": [
                "Um produtor musical coordena sessões de gravação, trabalha nos arranjos e supervisiona todo o processo criativo",
                "Um engenheiro de som configura equipamentos de gravação, opera a mesa de som e otimiza a qualidade sonora",
                "Um beatmaker cria bases instrumentais, programa ritmos e desenvolve o fundamento sonoro de uma música",
                "Um sound designer cria, grava e manipula efeitos sonoros e ambientes para produções audiovisuais ou jogos"
            ],
            "educational_paths": [
                "Graduação em Produção Musical, Engenharia de Som ou Música",
                "Cursos técnicos de produção e áudio",
                "Workshops e cursos online especializados",
                "Estágios em estúdios e produtoras",
                "Aprendizado autodidata através de projetos pessoais"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Música básica", "Tecnologia básica"],
            "cross_curricular": ["Tecnologia", "Física (acústica)", "Artes", "Matemática (ritmo e proporções)"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Produção Musical"] = producao_musical_subarea
    area_ref.set(area_data)

    return area_data
def setup_esportes_coletivos_subarea(db):
    """
    Configura a subárea de Esportes Coletivos dentro da área de Esportes e Atividades Físicas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Esportes e Atividades Físicas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Esportes e Atividades Físicas",
            "description": "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    esportes_coletivos_subarea = {
        "name": "Esportes Coletivos",
        "description": "Aprenda e pratique diversos esportes coletivos, desenvolvendo habilidades técnicas, táticas, trabalho em equipe e espírito esportivo através de atividades colaborativas e competitivas.",
        "estimated_time": "3-24 meses (dependendo da dedicação e esportes escolhidos)",
        "icon": "volleyball-ball",
        "references": [
            {"title": "Portal dos Esportes", "url": "https://www.portaldosesportes.com.br/"},
            {"title": "Team Sports Academy", "url": "https://www.teamsportsacademy.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução aos fundamentos básicos de diversos esportes coletivos",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender as regras básicas de diferentes esportes coletivos",
                    "Desenvolver habilidades motoras fundamentais para a prática esportiva",
                    "Aprender a jogar cooperativamente em um ambiente de equipe",
                    "Entender os valores do esporte: respeito, fair play e trabalho coletivo"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos dos Esportes Coletivos",
                        "module_description": "Explore habilidades básicas e conceitos comuns a diversos esportes de equipe",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Habilidades Fundamentais",
                                "objectives": "Desenvolver coordenação motora e habilidades básicas presentes em vários esportes",
                                "estimated_time": "60 minutos",
                                "content_summary": "Prática de movimentos e habilidades transferíveis entre diferentes esportes coletivos",
                                "steps": [
                                    "Habilidades de locomoção: correr, saltar, mudar de direção",
                                    "Manipulação de bola: passar, receber, arremessar, chutar",
                                    "Coordenação olho-mão e olho-pé",
                                    "Jogos pré-desportivos para desenvolvimento motor"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que é importante desenvolver habilidades fundamentais antes de se especializar em um esporte específico?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "O desenvolvimento de habilidades fundamentais proporciona uma base motora diversificada, facilita a transferência de aprendizado entre esportes, previne especialização precoce e possíveis lesões, além de permitir maior versatilidade e adaptabilidade em diferentes contextos esportivos."
                                    },
                                    {
                                        "question": "Qual das seguintes habilidades NÃO é considerada fundamental para a maioria dos esportes coletivos?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Correr e mudar de direção rapidamente",
                                            "Capacidade de comunicação com os companheiros",
                                            "Executar uma cambalhota para trás",
                                            "Passar e receber objetos em movimento"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "circuito",
                                        "title": "Circuito de Habilidades",
                                        "description": "Estações com diferentes desafios de coordenação, passe, recepção e movimentação"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Desenvolvimento Motor através do Esporte",
                                     "url": "https://exemplo.com/video_desenvolvimento"},
                                    {"type": "infográfico", "title": "Habilidades Transferíveis entre Esportes",
                                     "url": "https://exemplo.com/infografico_habilidades"}
                                ]
                            },
                            {
                                "lesson_title": "Entendendo o Jogo Coletivo",
                                "objectives": "Compreender conceitos básicos de cooperação, espaço e posicionamento",
                                "estimated_time": "60 minutos",
                                "steps": [
                                    "Comunicação e cooperação entre jogadores",
                                    "Ocupação de espaços e noções de posicionamento",
                                    "Transição entre ataque e defesa",
                                    "Tomada de decisão básica: quando passar, quando finalizar"
                                ],
                                "exercises": [
                                    {
                                        "question": "Durante um jogo, quais são os sinais (verbais e não-verbais) que você pode usar para se comunicar com seus companheiros de equipe?",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Podem mencionar: chamadas verbais ('Estou livre!', 'Passa!', 'Cuidado!'), gestos com as mãos indicando direções ou pedindo a bola, contato visual, apontando para espaços ou oponentes, posicionamento corporal indicando intenções, etc."
                                    }
                                ],
                                "project": {
                                    "title": "Mini-Torneio de Jogos Simplificados",
                                    "description": "Participação em jogos reduzidos que enfatizam cooperação e ocupação de espaço",
                                    "expected_outcome": "Compreensão prática dos conceitos básicos de jogo coletivo",
                                    "estimated_time": "45 minutos"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Avaliação de Habilidades Fundamentais",
                            "format": "Circuito prático + quiz sobre conceitos básicos",
                            "passing_score": "Demonstração de coordenação básica e compreensão dos conceitos",
                            "time_limit": "45 minutos",
                            "certificate": "Atleta Fundamental - Nível 1"
                        }
                    },
                    {
                        "module_title": "Iniciação Multiesportiva",
                        "module_description": "Conheça diferentes esportes coletivos e suas características específicas",
                        "estimated_time": "8 semanas",
                        "prerequisites": ["Fundamentos dos Esportes Coletivos"],
                        "lessons": [
                            {
                                "lesson_title": "Futebol Básico",
                                "objectives": "Aprender fundamentos e regras básicas do futebol",
                                "steps": [
                                    "Controle de bola: domínio, condução e passe",
                                    "Chute a gol: técnica básica e precisão",
                                    "Regras fundamentais e dimensões do jogo",
                                    "Posições básicas e objetivo do jogo"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são as principais superfícies de contato do pé utilizadas para passar a bola no futebol?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Somente a parte interna do pé",
                                            "Parte interna, externa e peito do pé",
                                            "Apenas o bico do pé (ponta)",
                                            "Somente o calcanhar"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Jogo de Futebol Modificado",
                                    "description": "Participar de um jogo com regras adaptadas para facilitar o sucesso e a participação de todos",
                                    "steps": [
                                        "Jogos com número reduzido de jogadores (3x3, 4x4)",
                                        "Espaço adequado ao nível dos participantes",
                                        "Regras modificadas para maior participação",
                                        "Reflexão após o jogo sobre as aprendizagens"
                                    ],
                                    "estimated_time": "30 minutos"
                                }
                            },
                            {
                                "lesson_title": "Basquetebol Básico",
                                "objectives": "Aprender fundamentos e regras básicas do basquetebol",
                                "steps": [
                                    "Controle de bola: manejo, drible e passe",
                                    "Arremesso: técnica básica da bandeja e lance livre",
                                    "Regras fundamentais: passos, dribles, faltas",
                                    "Posicionamento básico e objetivo do jogo"
                                ],
                                "project": {
                                    "title": "Desafios de Basquete",
                                    "description": "Participar de uma série de mini-jogos e desafios específicos de basquetebol"
                                }
                            },
                            {
                                "lesson_title": "Voleibol Básico",
                                "objectives": "Aprender fundamentos e regras básicas do voleibol",
                                "steps": [
                                    "Toque por cima e manchete: técnica básica",
                                    "Saque por baixo: precisão e consistência",
                                    "Regras fundamentais: rotação, pontuação, toques",
                                    "Posicionamento básico e objetivo do jogo"
                                ],
                                "project": {
                                    "title": "Voleibol Adaptado",
                                    "description": "Jogo com regras modificadas: bola mais leve, rede mais baixa, permissão para segurar a bola"
                                }
                            },
                            {
                                "lesson_title": "Handebol Básico",
                                "objectives": "Aprender fundamentos e regras básicas do handebol",
                                "steps": [
                                    "Manejo de bola: recepção e diferentes tipos de passe",
                                    "Arremesso: técnica básica parado e em movimento",
                                    "Regras fundamentais: passos, área do goleiro, faltas",
                                    "Posicionamento básico e objetivo do jogo"
                                ],
                                "project": {
                                    "title": "Mini-Handebol",
                                    "description": "Jogo simplificado com ênfase na participação e fundamentos básicos"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Festival Multiesportivo",
                            "description": "Participar de um evento com diferentes estações de jogos coletivos adaptados",
                            "deliverables": ["Participação ativa em todos os esportes", "Autoavaliação de desempenho e preferências", "Reflexão sobre a experiência multiesportiva"],
                            "estimated_time": "Evento de 3-4 horas (ou dividido em múltiplas sessões)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Torneio das Equipes",
                    "description": "Participar de um torneio interno envolvendo os diferentes esportes estudados",
                    "requirements": [
                        "Formação de equipes mistas e balanceadas",
                        "Participação em pelo menos três modalidades esportivas diferentes",
                        "Demonstração de habilidades técnicas básicas",
                        "Aplicação de conceitos de jogo coletivo",
                        "Manifestação de espírito esportivo e respeito aos colegas"
                    ],
                    "rubric": "Avaliação baseada em participação, trabalho em equipe, desenvolvimento técnico e atitude esportiva",
                    "showcase": "Evento esportivo com premiação de participação para todos"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos dos Esportes Coletivos",
                    "format": "Combinação de avaliação prática (circuito de habilidades) + teste teórico básico + autoavaliação",
                    "passing_criteria": "Demonstração de desenvolvimento motor adequado à idade e compreensão básica dos esportes",
                    "certification": "Atleta Multiesportivo - Nível Iniciante"
                },
                "suggested_path_forward": ["Especialização em um Esporte Específico", "Competições Escolares", "Arbitragem Básica"]
            },
            "intermediario": {
                "description": "Aprofundamento técnico-tático em esportes coletivos específicos",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Especialização Esportiva Inicial",
                        "module_description": "Desenvolva habilidades mais avançadas em um ou dois esportes coletivos de sua escolha",
                        "estimated_time": "12 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Técnica Específica Avançada",
                                "objectives": "Aprimorar os fundamentos específicos do esporte escolhido",
                                "steps": [
                                    "Refinamento técnico dos fundamentos básicos",
                                    "Introdução a fundamentos técnicos mais complexos",
                                    "Combinação de fundamentos em sequências",
                                    "Execução técnica sob pressão e em movimento"
                                ]
                            },
                            {
                                "lesson_title": "Introdução à Tática",
                                "objectives": "Compreender conceitos táticos básicos do esporte escolhido",
                                "steps": [
                                    "Sistemas básicos de jogo: posicionamento e funções",
                                    "Táticas ofensivas simples: criação de espaços, desmarcação",
                                    "Táticas defensivas simples: marcação, coberturas",
                                    "Transições ataque-defesa e vice-versa"
                                ],
                                "project": {
                                    "title": "Análise Tática Simplificada",
                                    "description": "Assistir a um jogo e identificar elementos táticos básicos estudados"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Preparação Física para Esportes Coletivos",
                        "module_description": "Desenvolva capacidades físicas específicas para melhorar seu desempenho",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Componentes do Condicionamento Físico",
                                "objectives": "Entender e desenvolver diferentes capacidades físicas para esportes coletivos",
                                "steps": [
                                    "Resistência aeróbica e anaeróbica para esportes intermitentes",
                                    "Velocidade, agilidade e tempo de reação",
                                    "Força e potência para movimentos esportivos",
                                    "Flexibilidade e mobilidade para prevenção de lesões"
                                ]
                            },
                            {
                                "lesson_title": "Treinamento Integrado",
                                "objectives": "Aprender a treinar habilidades técnicas e capacidades físicas de forma integrada",
                                "steps": [
                                    "Circuitos técnico-físicos",
                                    "Jogos condicionados com objetivos físicos",
                                    "Periodização básica do treinamento",
                                    "Recuperação e prevenção de lesões"
                                ],
                                "project": {
                                    "title": "Meu Programa de Treinamento",
                                    "description": "Criar e executar um plano de treinamento básico para duas semanas"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Competição Interna",
                            "description": "Participar de uma competição do esporte escolhido, aplicando conhecimentos técnicos, táticos e físicos",
                            "deliverables": ["Participação ativa na competição", "Análise do desempenho individual e coletivo", "Identificação de pontos fortes e áreas para melhoria"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Esportivo em Equipe",
                    "description": "Organizar e participar de um projeto esportivo colaborativo",
                    "requirements": [
                        "Formação de equipe para esporte específico",
                        "Planejamento de sessões de treinamento",
                        "Definição de sistema e estratégia de jogo",
                        "Participação em competição formal ou amistosa",
                        "Análise e reflexão sobre o processo e resultados"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de alto nível em esportes coletivos específicos e liderança esportiva",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Tática Avançada e Sistemas de Jogo",
                        "module_description": "Aprenda estratégias e sistemas complexos no esporte coletivo escolhido",
                        "lessons": [
                            {
                                "lesson_title": "Sistemas de Jogo Avançados",
                                "objectives": "Compreender e aplicar diferentes sistemas táticos",
                                "steps": [
                                    "Sistemas ofensivos e defensivos específicos do esporte",
                                    "Adaptação tática conforme o adversário",
                                    "Variações táticas durante o jogo",
                                    "Leitura de jogo e tomada de decisão avançada"
                                ]
                            },
                            {
                                "lesson_title": "Funções Específicas e Especialização",
                                "objectives": "Desenvolver conhecimentos e habilidades para funções específicas",
                                "steps": [
                                    "Características e demandas de cada posição/função",
                                    "Treinamento específico por posição",
                                    "Interação e coordenação entre diferentes funções",
                                    "Versatilidade tática entre posições"
                                ],
                                "project": {
                                    "title": "Dossiê Tático",
                                    "description": "Criar uma análise detalhada de uma posição específica no esporte escolhido"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Liderança Esportiva e Treinamento",
                        "module_description": "Desenvolva habilidades para liderar equipes e auxiliar no treinamento",
                        "lessons": [
                            {
                                "lesson_title": "Liderança no Esporte Coletivo",
                                "objectives": "Aprender a liderar equipes e promover ambiente positivo",
                                "steps": [
                                    "Tipos de liderança no contexto esportivo",
                                    "Comunicação efetiva entre atletas",
                                    "Motivação individual e coletiva",
                                    "Gestão de conflitos e construção de equipe"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Projeto de Monitoria",
                            "description": "Atuar como auxiliar/monitor em treinamentos para atletas iniciantes, desenvolvendo habilidades de liderança e ensino",
                            "deliverables": ["Planejamento de sessões", "Condução de atividades sob supervisão", "Feedback aos atletas iniciantes", "Relatório reflexivo sobre a experiência"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Esportivo Completo",
                    "description": "Desenvolver um projeto completo envolvendo treinamento, competição e análise em nível avançado",
                    "requirements": [
                        "Planejamento de temporada ou ciclo de treinamento",
                        "Implementação de sistema tático avançado",
                        "Liderança de equipe em ambiente competitivo",
                        "Análise técnico-tática de jogos",
                        "Apresentação de projeto com fundamentação teórica e prática"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Futebol Avançado",
                "description": "Especialização em aspectos técnicos, táticos e físicos do futebol",
                "age_range": "12-17 anos",
                "modules": [
                    "Fundamentos Técnicos Avançados",
                    "Sistemas Táticos no Futebol",
                    "Preparação Física Específica",
                    "Análise de Jogo e Estratégia"
                ],
                "final_project": {
                    "title": "Projeto Futebolístico",
                    "description": "Desenvolver um projeto completo envolvendo treinamento, tática e competição"
                }
            },
            {
                "name": "Basquetebol Avançado",
                "description": "Desenvolvimento de habilidades técnico-táticas específicas do basquetebol",
                "age_range": "12-17 anos",
                "modules": [
                    "Técnica Individual Ofensiva e Defensiva",
                    "Sistemas de Ataque e Defesa",
                    "Preparação Física para Basquete",
                    "Leitura de Jogo e Tomada de Decisão"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Atleta Profissional",
                "Treinador/Técnico Esportivo",
                "Preparador Físico",
                "Analista de Desempenho",
                "Gestor Esportivo",
                "Árbitro/Oficial",
                "Scout/Olheiro",
                "Professor de Educação Física"
            ],
            "day_in_life": [
                "Um atleta profissional divide seu tempo entre treinamentos técnicos, táticos, físicos e preparação mental",
                "Um treinador planeja sessões, analisa oponentes, desenvolve estratégias e gerencia atletas",
                "Um analista de desempenho coleta e interpreta dados de jogos e treinos para otimizar estratégias",
                "Um árbitro estuda constantemente as regras, mantém boa forma física e gerencia pressões em competições"
            ],
            "educational_paths": [
                "Graduação em Educação Física, Ciências do Esporte ou Treinamento Esportivo",
                "Cursos de formação específica nas federações esportivas",
                "Certificações de treinador em diferentes níveis",
                "Especialização em Ciências do Esporte, Fisiologia, Biomecânica, etc.",
                "Formação em arbitragem e regras oficiais"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica"],
            "cross_curricular": ["Biologia (corpo humano)", "Física (movimento)", "Matemática (estatísticas)", "Psicologia (trabalho em equipe)"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Esportes Coletivos"] = esportes_coletivos_subarea
    area_ref.set(area_data)

    return area_data

def setup_esportes_individuais_subarea(db):
    """
    Configura a subárea de Esportes Individuais dentro da área de Esportes e Atividades Físicas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Esportes e Atividades Físicas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Esportes e Atividades Físicas",
            "description": "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    esportes_individuais_subarea = {
        "name": "Esportes Individuais",
        "description": "Explore e pratique diversos esportes individuais, desenvolvendo habilidades específicas, autodisciplina, concentração e superação pessoal através de modalidades onde você é o protagonista da sua performance.",
        "estimated_time": "3-24 meses (dependendo da dedicação e esportes escolhidos)",
        "icon": "running",
        "references": [
            {"title": "Academia de Esportes Individuais", "url": "https://www.esportesindividuais.com.br/"},
            {"title": "Individual Sports Foundation", "url": "https://www.individualsportsfoundation.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução às habilidades básicas e conceitos fundamentais de diversos esportes individuais",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Desenvolver coordenação motora e habilidades específicas para diferentes esportes individuais",
                    "Compreender regras básicas e princípios de várias modalidades individuais",
                    "Cultivar autodisciplina, foco e determinação através da prática esportiva individual",
                    "Desenvolver autoconhecimento e reconhecer limites e potenciais pessoais"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos dos Esportes Individuais",
                        "module_description": "Explore as bases comuns e desenvolvimento motor para diferentes modalidades individuais",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Preparação Física Fundamental",
                                "objectives": "Desenvolver capacidades físicas básicas necessárias para esportes individuais",
                                "estimated_time": "60 minutos",
                                "content_summary": "Atividades que desenvolvem as capacidades físicas essenciais para a prática de esportes individuais",
                                "steps": [
                                    "Resistência aeróbica: corridas e exercícios contínuos de baixa intensidade",
                                    "Força básica: exercícios com peso corporal (agachamentos, flexões modificadas)",
                                    "Flexibilidade: alongamentos dinâmicos e estáticos básicos",
                                    "Coordenação e equilíbrio: circuitos e estações de desafios motores"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que a flexibilidade é importante para a maioria dos esportes individuais?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "A flexibilidade permite maior amplitude de movimentos, melhora a eficiência técnica, reduz o risco de lesões, contribui para uma melhor postura e alinhamento corporal durante a prática esportiva, e pode melhorar a recuperação muscular após o esforço."
                                    },
                                    {
                                        "question": "Qual componente físico é mais importante para um corredor de longa distância?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Força explosiva",
                                            "Resistência aeróbica",
                                            "Velocidade máxima",
                                            "Flexibilidade extrema"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "circuito",
                                        "title": "Circuito de Capacidades",
                                        "description": "Estações com diferentes desafios físicos para desenvolver as capacidades fundamentais"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Preparação Física para Jovens Atletas",
                                     "url": "https://exemplo.com/video_prepfisica"},
                                    {"type": "infográfico", "title": "Componentes do Condicionamento Físico",
                                     "url": "https://exemplo.com/infografico_condicionamento"}
                                ]
                            },
                            {
                                "lesson_title": "Mentalidade do Atleta Individual",
                                "objectives": "Compreender e desenvolver os aspectos mentais essenciais para esportes individuais",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "Foco e concentração: exercícios práticos de atenção plena",
                                    "Estabelecimento de metas: do longo ao curto prazo",
                                    "Superação de desafios: lidar com frustração e perseverança",
                                    "Rotinas pré-performance e visualização básica"
                                ],
                                "exercises": [
                                    {
                                        "question": "Crie três metas pessoais para um esporte individual que você gostaria de praticar: uma para curto prazo (uma semana), uma para médio prazo (um mês) e uma para longo prazo (seis meses).",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Devem demonstrar compreensão da progressão de objetivos e especificidade (metas mensuráveis, realistas, relevantes, com prazo definido)."
                                    }
                                ],
                                "project": {
                                    "title": "Diário do Atleta",
                                    "description": "Criar e manter por uma semana um diário com metas, reflexões e progresso na prática esportiva",
                                    "expected_outcome": "Desenvolvimento de autodisciplina e autoconhecimento",
                                    "estimated_time": "10-15 minutos diários por uma semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Avaliação de Fundamentos",
                            "format": "Testes práticos de capacidades físicas + reflexão sobre mentalidade",
                            "passing_score": "Demonstração de desenvolvimento adequado para idade e nível",
                            "time_limit": "45 minutos",
                            "certificate": "Atleta Fundamental - Nível 1"
                        }
                    },
                    {
                        "module_title": "Exploração Multiesportiva Individual",
                        "module_description": "Conheça diferentes esportes individuais e suas características específicas",
                        "estimated_time": "8 semanas",
                        "prerequisites": ["Fundamentos dos Esportes Individuais"],
                        "lessons": [
                            {
                                "lesson_title": "Atletismo Básico",
                                "objectives": "Aprender fundamentos das principais provas de atletismo",
                                "steps": [
                                    "Corridas: técnica básica de corrida e saída",
                                    "Saltos: fundamentos do salto em distância e altura",
                                    "Arremesso: técnica básica do arremesso de peso adaptado",
                                    "Provas combinadas: circuito com diferentes habilidades"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são os elementos técnicos mais importantes para uma corrida eficiente?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas correr o mais rápido possível sem técnica",
                                            "Postura, movimentação dos braços, passada e apoio do pé",
                                            "Usar tênis de marca famosa e roupas adequadas",
                                            "Respirar apenas pela boca durante toda a corrida"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Mini-Olimpíada",
                                    "description": "Participar de um evento com provas adaptadas de atletismo",
                                    "steps": [
                                        "Treinamento específico para as provas",
                                        "Estabelecimento de metas pessoais",
                                        "Participação nas provas escolhidas",
                                        "Reflexão sobre a experiência e resultados"
                                    ],
                                    "estimated_time": "2 sessões de treino + evento final"
                                }
                            },
                            {
                                "lesson_title": "Introdução à Ginástica",
                                "objectives": "Aprender movimentos básicos da ginástica e desenvolvimento corporal",
                                "steps": [
                                    "Fundamentos de postura e alinhamento corporal",
                                    "Elementos básicos de solo: rolamentos, posições estáticas",
                                    "Força e flexibilidade específicas para ginástica",
                                    "Combinação de elementos simples em uma pequena série"
                                ],
                                "project": {
                                    "title": "Minha Série de Solo",
                                    "description": "Criar e apresentar uma pequena série de solo com elementos básicos"
                                }
                            },
                            {
                                "lesson_title": "Fundamentos de Tênis/Badminton",
                                "objectives": "Aprender habilidades básicas dos esportes de raquete",
                                "steps": [
                                    "Empunhadura e posição básica de espera",
                                    "Golpes fundamentais: forehand, backhand, saque",
                                    "Deslocamentos na quadra e posicionamento",
                                    "Regras básicas e contagem de pontos"
                                ],
                                "project": {
                                    "title": "Jogo Adaptado",
                                    "description": "Participar de jogos com quadra e regras adaptadas para iniciantes"
                                }
                            },
                            {
                                "lesson_title": "Introdução ao Xadrez/Esportes da Mente",
                                "objectives": "Aprender fundamentos dos esportes mentais",
                                "steps": [
                                    "Regras básicas e movimentação das peças",
                                    "Princípios fundamentais de estratégia",
                                    "Desenvolvimento do pensamento lógico e antecipação",
                                    "Etiqueta e conduta no esporte mental"
                                ],
                                "project": {
                                    "title": "Torneio Amistoso",
                                    "description": "Participar de pequeno torneio interno de xadrez ou outro esporte mental"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Festival de Esportes Individuais",
                            "description": "Participar de um evento com estações de diferentes esportes individuais",
                            "deliverables": ["Participação em pelo menos 4 modalidades diferentes", "Registro de desempenho e experiência em cada uma", "Identificação de preferências e aptidões pessoais"],
                            "estimated_time": "Evento de 3-4 horas (ou dividido em múltiplas sessões)"
                        }
                    }
                ],
                "final_project": {
                    "title": "Meu Esporte Individual",
                    "description": "Escolher um esporte individual para aprofundamento e apresentação de habilidades",
                    "requirements": [
                        "Escolha de uma modalidade individual de interesse",
                        "Treinamento específico das habilidades por 2-3 semanas",
                        "Demonstração prática das habilidades desenvolvidas",
                        "Apresentação sobre as regras e características do esporte",
                        "Reflexão sobre o processo de aprendizagem e desafios superados"
                    ],
                    "rubric": "Avaliação baseada em empenho, desenvolvimento técnico, compreensão do esporte e capacidade de reflexão",
                    "showcase": "Mostra de habilidades com apresentações individuais para a turma"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Esportes Individuais Básicos",
                    "format": "Demonstração prática + teste teórico sobre esportes + apresentação do projeto final",
                    "passing_criteria": "Demonstração de desenvolvimento adequado ao nível e idade, e compreensão básica dos esportes abordados",
                    "certification": "Atleta Multimodal - Nível Iniciante"
                },
                "suggested_path_forward": ["Especialização em um Esporte Individual", "Competições Escolares", "Treinamento Físico Específico"]
            },
            "intermediario": {
                "description": "Aprofundamento técnico em esportes individuais específicos e desenvolvimento de treinamento sistemático",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Especialização Inicial",
                        "module_description": "Aprofunde seus conhecimentos e habilidades em um esporte individual escolhido",
                        "estimated_time": "12 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Técnica Específica Avançada",
                                "objectives": "Desenvolver técnicas mais refinadas do esporte escolhido",
                                "steps": [
                                    "Análise técnica dos fundamentos principais",
                                    "Correção de erros e refinamento do movimento",
                                    "Técnicas específicas intermediárias",
                                    "Consistência e precisão na execução"
                                ]
                            },
                            {
                                "lesson_title": "Estratégia Competitiva Básica",
                                "objectives": "Aprender a abordagem estratégica para treinos e competições",
                                "steps": [
                                    "Análise de pontos fortes e fracos pessoais",
                                    "Construção de estratégias básicas para competições",
                                    "Adaptação tática conforme o oponente/situação",
                                    "Planejamento de competições e gerenciamento de energia"
                                ],
                                "project": {
                                    "title": "Plano Estratégico",
                                    "description": "Criar um plano estratégico para uma competição ou desafio específico"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Treinamento Sistemático",
                        "module_description": "Aprenda a estruturar e organizar seu treinamento para resultados melhores",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Princípios de Treinamento",
                                "objectives": "Compreender os fundamentos científicos do treinamento esportivo",
                                "steps": [
                                    "Princípios básicos: sobrecarga, especificidade, progressão",
                                    "Periodização simples: organizando ciclos de treinamento",
                                    "Equilíbrio entre volume e intensidade",
                                    "Recuperação e prevenção de overtraining"
                                ]
                            },
                            {
                                "lesson_title": "Preparação Física Específica",
                                "objectives": "Desenvolver capacidades físicas específicas para o esporte escolhido",
                                "steps": [
                                    "Análise das demandas físicas do esporte",
                                    "Exercícios específicos para as capacidades principais",
                                    "Testes e avaliações para monitorar progresso",
                                    "Ajustes no treinamento conforme resposta individual"
                                ],
                                "project": {
                                    "title": "Meu Programa de Treinamento",
                                    "description": "Criar e executar um plano de treinamento de 4 semanas para o esporte escolhido"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Competição ou Desafio",
                            "description": "Preparar-se e participar de uma competição ou desafio específico do esporte escolhido",
                            "deliverables": ["Plano de preparação executado", "Participação no evento", "Análise de desempenho e reflexão sobre a experiência"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Desenvolvimento Atlético",
                    "description": "Criar e implementar um projeto de desenvolvimento no esporte individual escolhido",
                    "requirements": [
                        "Avaliação inicial de habilidades e capacidades",
                        "Estabelecimento de metas e objetivos específicos",
                        "Planejamento e execução de programa de treinamento (6-8 semanas)",
                        "Participação em competição ou demonstração de habilidades",
                        "Relatório detalhado do processo e resultados"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de alto nível em um esporte individual específico e introdução à ciência do esporte",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Performance Avançada",
                        "module_description": "Desenvolva técnicas de alta performance e refinamento para competições",
                        "lessons": [
                            {
                                "lesson_title": "Técnica de Elite",
                                "objectives": "Refinar técnicas específicas para nível avançado",
                                "steps": [
                                    "Análise biomecânica do movimento técnico",
                                    "Correções finas e otimização da técnica",
                                    "Adaptações individuais baseadas em características pessoais",
                                    "Consistência em condições variáveis e sob pressão"
                                ]
                            },
                            {
                                "lesson_title": "Preparação Mental Avançada",
                                "objectives": "Desenvolver habilidades psicológicas para alta performance",
                                "steps": [
                                    "Técnicas avançadas de concentração e foco",
                                    "Gerenciamento de estresse e ansiedade competitiva",
                                    "Rotinas mentais pré, durante e pós-competição",
                                    "Visualização e prática mental sistemática"
                                ],
                                "project": {
                                    "title": "Plano Mental",
                                    "description": "Criar e implementar um plano de treinamento mental para competições"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Ciência do Esporte Aplicada",
                        "module_description": "Aprenda a utilizar conhecimentos científicos para otimizar o desempenho",
                        "lessons": [
                            {
                                "lesson_title": "Monitoramento e Análise do Treinamento",
                                "objectives": "Utilizar métodos científicos para avaliar e melhorar o treinamento",
                                "steps": [
                                    "Utilização de métricas e medidas objetivas",
                                    "Análise de dados de treinamento e competição",
                                    "Ajustes baseados em evidências científicas",
                                    "Tecnologias e recursos para análise de performance"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Análise Científica de Performance",
                            "description": "Realizar uma análise detalhada do próprio desempenho utilizando métodos científicos",
                            "deliverables": ["Coleta sistemática de dados", "Análise e interpretação dos resultados", "Recomendações baseadas em evidências para melhorias", "Apresentação científica dos resultados"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Atlético de Alto Rendimento",
                    "description": "Desenvolver um projeto completo visando performance de alto nível",
                    "requirements": [
                        "Avaliação multidimensional: técnica, física, mental, tática",
                        "Planejamento periodizado para ciclo competitivo",
                        "Implementação de estratégias avançadas de treinamento",
                        "Participação em competições de nível avançado",
                        "Análise científica e reflexão crítica sobre resultados"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Atletismo Avançado",
                "description": "Especialização em provas de atletismo: corridas, saltos ou arremessos",
                "age_range": "12-17 anos",
                "modules": [
                    "Técnica Especializada por Prova",
                    "Condicionamento Específico para Atletismo",
                    "Periodização e Planejamento para Competições",
                    "Estratégias Avançadas e Análise de Performance"
                ],
                "final_project": {
                    "title": "Ciclo Competitivo de Atletismo",
                    "description": "Preparar e executar um ciclo completo de treinamento visando competições específicas"
                }
            },
            {
                "name": "Tênis/Esportes de Raquete",
                "description": "Desenvolvimento avançado em tênis, badminton ou outros esportes de raquete",
                "age_range": "12-17 anos",
                "modules": [
                    "Técnica Avançada de Golpes",
                    "Tática e Estratégia de Jogo",
                    "Condicionamento Específico para Esportes de Raquete",
                    "Preparação Mental para Confrontos Individuais"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Atleta Profissional",
                "Treinador Pessoal/Técnico Esportivo",
                "Preparador Físico",
                "Psicólogo do Esporte",
                "Fisiologista do Exercício",
                "Biomecânico",
                "Árbitro/Juiz",
                "Gestor de Eventos Esportivos"
            ],
            "day_in_life": [
                "Um atleta profissional segue uma rotina rigorosa combinando treinamento técnico, físico, recuperação e preparação mental",
                "Um treinador de esportes individuais analisa movimentos, corrige técnicas e planeja progressões individualizadas para cada atleta",
                "Um psicólogo do esporte trabalha aspectos mentais com atletas, como controle da ansiedade, foco e motivação",
                "Um biomecânico analisa padrões de movimento para otimizar técnicas e prevenir lesões"
            ],
            "educational_paths": [
                "Graduação em Educação Física ou Ciências do Esporte",
                "Especialização em modalidades específicas através de federações",
                "Cursos de treinamento esportivo e certificações por nível",
                "Pós-graduação em áreas específicas: Biomecânica, Fisiologia do Exercício, Psicologia do Esporte",
                "Formação em arbitragem específica por modalidade"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica"],
            "cross_curricular": ["Biologia (corpo humano)", "Física (biomecânica)", "Matemática (estatísticas)", "Psicologia (mentalidade)"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Esportes Individuais"] = esportes_individuais_subarea
    area_ref.set(area_data)

    return area_data


def setup_artes_marciais_subarea(db):
    """
    Configura a subárea de Artes Marciais dentro da área de Esportes e Atividades Físicas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Esportes e Atividades Físicas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Esportes e Atividades Físicas",
            "description": "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    artes_marciais_subarea = {
        "name": "Artes Marciais",
        "description": "Explore e pratique diferentes artes marciais, desenvolvendo habilidades físicas, mentais e espirituais através de disciplinas que combinam técnicas de combate, filosofia e desenvolvimento pessoal.",
        "estimated_time": "6-36 meses (dependendo da dedicação e arte marcial escolhida)",
        "icon": "hand-rock",
        "references": [
            {"title": "Academia de Artes Marciais", "url": "https://www.academiadeartesmarciais.com.br/"},
            {"title": "Martial Arts Education Foundation", "url": "https://www.martialartsed.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução aos fundamentos básicos e princípios gerais das artes marciais",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os princípios filosóficos e éticos básicos das artes marciais",
                    "Desenvolver postura, equilíbrio e fundamentos corporais para diferentes artes marciais",
                    "Aprender técnicas básicas de defesa pessoal e movimentos fundamentais",
                    "Cultivar disciplina, respeito e autocontrole através da prática marcial"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos das Artes Marciais",
                        "module_description": "Explore os princípios básicos e preparação corporal comuns a várias artes marciais",
                        "estimated_time": "6 semanas",
                        "difficulty": "moderado",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Filosofia e Ética Marcial",
                                "objectives": "Compreender os princípios fundamentais que guiam a prática das artes marciais",
                                "estimated_time": "60 minutos",
                                "content_summary": "Introdução aos conceitos filosóficos, código de conduta e valores presentes nas artes marciais",
                                "steps": [
                                    "História e origem das artes marciais tradicionais",
                                    "Valores fundamentais: respeito, disciplina, perseverança, autocontrole",
                                    "Etiqueta no dojo/academia e hierarquia tradicional",
                                    "O propósito das artes marciais: além do combate"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que o respeito é considerado um valor tão importante na prática das artes marciais?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "O respeito é fundamental nas artes marciais pois estabelece um ambiente seguro para aprendizagem de técnicas potencialmente perigosas, honra a linhagem e tradição do conhecimento transmitido, reconhece o esforço e dedicação dos praticantes mais experientes, e desenvolve humildade e consideração pelos outros, transformando o treinamento em uma prática de desenvolvimento pessoal além das habilidades físicas."
                                    },
                                    {
                                        "question": "Qual dos seguintes NÃO é geralmente considerado um dos principais valores cultivados nas artes marciais tradicionais?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Disciplina e autocontrole",
                                            "Competitividade a qualquer custo",
                                            "Respeito pelos outros e humildade",
                                            "Perseverança e superação de desafios"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "discussão",
                                        "title": "Círculo de Valores",
                                        "description": "Discussão em grupo sobre como os valores marciais podem ser aplicados no dia a dia"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Os Princípios das Artes Marciais",
                                     "url": "https://exemplo.com/video_principios"},
                                    {"type": "artigo", "title": "Artes Marciais como Caminho de Vida",
                                     "url": "https://exemplo.com/artigo_caminho"}
                                ]
                            },
                            {
                                "lesson_title": "Preparação Corporal e Postura",
                                "objectives": "Desenvolver consciência corporal, alinhamento e preparação física básica",
                                "estimated_time": "75 minutos",
                                "steps": [
                                    "Aquecimento específico para artes marciais",
                                    "Posições básicas e alinhamento corporal",
                                    "Exercícios de equilíbrio, força e flexibilidade",
                                    "Respiração coordenada com o movimento"
                                ],
                                "exercises": [
                                    {
                                        "question": "Como a respiração adequada pode influenciar seu desempenho nas artes marciais?",
                                        "type": "open",
                                        "answer": "A respiração adequada nas artes marciais melhora o controle e potência dos movimentos, aumenta a estabilidade e equilíbrio, otimiza o gasto energético, favorece a concentração e foco, ajuda no controle emocional durante situações de pressão, e contribui para a recuperação entre esforços intensos."
                                    }
                                ],
                                "project": {
                                    "title": "Rotina Pessoal de Preparação",
                                    "description": "Criar uma rotina diária de 10 minutos com exercícios de preparação corporal para artes marciais",
                                    "expected_outcome": "Desenvolvimento de disciplina e preparação física básica",
                                    "estimated_time": "10 minutos diários por duas semanas"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Avaliação de Fundamentos",
                            "format": "Demonstração de posturas básicas + teste sobre princípios filosóficos",
                            "passing_score": "Demonstração adequada de postura e compreensão dos valores",
                            "time_limit": "30 minutos",
                            "certificate": "Iniciante em Artes Marciais - Fundamentos"
                        }
                    },
                    {
                        "module_title": "Técnicas Básicas e Defesa Pessoal",
                        "module_description": "Aprenda movimentos fundamentais e técnicas iniciais de defesa",
                        "estimated_time": "8 semanas",
                        "prerequisites": ["Fundamentos das Artes Marciais"],
                        "lessons": [
                            {
                                "lesson_title": "Posições e Deslocamentos",
                                "objectives": "Aprender as posições fundamentais e formas de se movimentar no espaço",
                                "steps": [
                                    "Posições básicas comuns em diferentes artes marciais",
                                    "Deslocamentos fundamentais: passos, giros, recuos",
                                    "Transições entre posições com fluidez e equilíbrio",
                                    "Aplicações práticas das posições em situações de defesa"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que é importante manter o centro de gravidade baixo em muitas posições de artes marciais?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Apenas por tradição e estética",
                                            "Para maior estabilidade, equilíbrio e potência",
                                            "Para parecer mais intimidador ao oponente",
                                            "Para facilitar saltos e movimentos aéreos"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Sequência de Posições",
                                    "description": "Criar e praticar uma sequência de transições entre diferentes posições",
                                    "steps": [
                                        "Selecionar 4-5 posições fundamentais",
                                        "Praticar transições fluidas entre elas",
                                        "Adicionar deslocamentos direcionais",
                                        "Executar a sequência completa com precisão"
                                    ],
                                    "estimated_time": "Prática de 15 minutos diários por uma semana"
                                }
                            },
                            {
                                "lesson_title": "Técnicas de Mão e Braço",
                                "objectives": "Aprender técnicas básicas de ataque e defesa com membros superiores",
                                "steps": [
                                    "Posicionamento adequado das mãos para proteção",
                                    "Técnicas de golpe básicas: soco direto, gancho, bloqueios",
                                    "Técnicas de defesa: bloqueios, desvios, esquivas",
                                    "Combinações simples de ataque e defesa"
                                ],
                                "project": {
                                    "title": "Combinações Básicas",
                                    "description": "Praticar sequências combinando defesa e contra-ataque"
                                }
                            },
                            {
                                "lesson_title": "Técnicas de Perna",
                                "objectives": "Aprender técnicas básicas utilizando os membros inferiores",
                                "steps": [
                                    "Posicionamento e alinhamento correto das pernas",
                                    "Chutes básicos: frontal, lateral, circular",
                                    "Movimentação e equilíbrio para técnicas de perna",
                                    "Integração de técnicas de perna com deslocamentos"
                                ],
                                "project": {
                                    "title": "Circuito de Técnicas",
                                    "description": "Participar de um circuito com estações para praticar diferentes técnicas de perna"
                                }
                            },
                            {
                                "lesson_title": "Defesa Pessoal Básica",
                                "objectives": "Aprender princípios fundamentais de defesa pessoal e segurança",
                                "steps": [
                                    "Princípios de prevenção e conscientização situacional",
                                    "Técnicas básicas para libertar-se de agarramentos",
                                    "Resposta a empurrões e puxões comuns",
                                    "Simulações práticas em ambiente controlado"
                                ],
                                "project": {
                                    "title": "Cenários de Segurança",
                                    "description": "Participar de simulações de situações cotidianas aplicando princípios de segurança"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Apresentação de Técnicas",
                            "description": "Preparar e demonstrar uma sequência prática integrando diferentes técnicas aprendidas",
                            "deliverables": ["Demonstração da sequência", "Explicação das técnicas utilizadas", "Aplicações práticas dos movimentos"],
                            "estimated_time": "3 semanas de preparação + apresentação"
                        }
                    }
                ],
                "final_project": {
                    "title": "Introdução às Artes Marciais",
                    "description": "Explorar diferentes artes marciais e seus aspectos fundamentais, culminando em uma apresentação prática",
                    "requirements": [
                        "Pesquisa sobre pelo menos três diferentes artes marciais",
                        "Demonstração de posturas e técnicas básicas",
                        "Apresentação sobre aspectos filosóficos e valores",
                        "Execução de uma sequência de movimentos de defesa pessoal",
                        "Reflexão sobre o aprendizado e valores adquiridos"
                    ],
                    "rubric": "Avaliação baseada em execução técnica, compreensão dos princípios, esforço e desenvolvimento pessoal",
                    "showcase": "Demonstração pública para colegas e familiares"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos das Artes Marciais",
                    "format": "Demonstração prática + teste escrito sobre princípios + autoavaliação de desenvolvimento",
                    "passing_criteria": "Execução adequada das técnicas básicas e compreensão dos valores marciais",
                    "certification": "Praticante Iniciante de Artes Marciais"
                },
                "suggested_path_forward": ["Escolha de Arte Marcial Específica", "Treinamento Regular", "Participação em Eventos"]
            },
            "intermediario": {
                "description": "Aprofundamento em uma arte marcial específica e desenvolvimento técnico-filosófico",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Especialização em Arte Marcial",
                        "module_description": "Aprofunde-se nos aspectos técnicos e filosóficos de uma arte marcial específica",
                        "estimated_time": "16 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Sistema Técnico Específico",
                                "objectives": "Compreender e praticar o sistema técnico da arte marcial escolhida",
                                "steps": [
                                    "Técnicas fundamentais específicas da modalidade",
                                    "Terminologia e classificação de movimentos",
                                    "Progressão técnica e sistema de graduação",
                                    "Formas/katas/poomsaes básicos e intermediários"
                                ]
                            },
                            {
                                "lesson_title": "Filosofia e Tradição",
                                "objectives": "Aprofundar a compreensão da filosofia específica da arte marcial escolhida",
                                "steps": [
                                    "Origens históricas e desenvolvimento da arte",
                                    "Princípios filosóficos e código de conduta específicos",
                                    "Tradições, rituais e protocolo da arte marcial",
                                    "Aplicação dos princípios na vida cotidiana"
                                ],
                                "project": {
                                    "title": "Ensaio Filosófico",
                                    "description": "Escrever um breve ensaio conectando um princípio filosófico da arte marcial com experiências pessoais"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Aplicações Práticas",
                        "module_description": "Desenvolva aplicações das técnicas em contextos realistas e dinâmicos",
                        "estimated_time": "12 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Aplicações de Combate",
                                "objectives": "Aprender a aplicar técnicas em situações de troca técnica controlada",
                                "steps": [
                                    "Exercícios de um passo (aplicação técnica específica)",
                                    "Exercícios de múltiplos passos (combinações)",
                                    "Treinamento com parceiros em cenários predefinidos",
                                    "Introdução ao combate livre controlado (sparring leve)"
                                ]
                            },
                            {
                                "lesson_title": "Defesa Pessoal Avançada",
                                "objectives": "Aprofundar as aplicações de defesa pessoal com técnicas específicas",
                                "steps": [
                                    "Resposta a diferentes tipos de ataques",
                                    "Defesa contra múltiplos agressores",
                                    "Uso de objetos cotidianos para defesa",
                                    "Aspectos legais e éticos da defesa pessoal"
                                ],
                                "project": {
                                    "title": "Manual de Segurança",
                                    "description": "Criar um pequeno manual com dicas e técnicas de segurança e defesa pessoal"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Demonstração Técnica",
                            "description": "Preparar uma demonstração técnica individual ou em grupo da arte marcial estudada",
                            "deliverables": ["Roteiro da demonstração", "Apresentação técnica", "Explicação das aplicações práticas"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Caminho do Praticante",
                    "description": "Desenvolver um projeto de médio prazo que demonstre progressão técnica e filosófica",
                    "requirements": [
                        "Treinamento regular documentado (diário de treino)",
                        "Domínio de um conjunto específico de técnicas",
                        "Apresentação de forma/kata com aplicações práticas",
                        "Demonstração de valores marciais na prática e conduta",
                        "Reflexão sobre o crescimento pessoal através da arte marcial"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento avançado, instrução inicial e aplicações profundas da arte marcial",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Maestria Técnica",
                        "module_description": "Refine técnicas avançadas e desenvolva expressão pessoal na arte marcial",
                        "lessons": [
                            {
                                "lesson_title": "Técnicas Avançadas",
                                "objectives": "Dominar técnicas de nível avançado da arte marcial escolhida",
                                "steps": [
                                    "Técnicas complexas e suas variações",
                                    "Combinações avançadas e transições refinadas",
                                    "Adaptação das técnicas para diferentes contextos",
                                    "Desenvolvimento de timing e sensibilidade"
                                ]
                            },
                            {
                                "lesson_title": "Expressão Pessoal",
                                "objectives": "Desenvolver estilo pessoal dentro da tradição da arte marcial",
                                "steps": [
                                    "Identificação de pontos fortes e afinidades técnicas",
                                    "Personalização de aplicações respeitando princípios tradicionais",
                                    "Criação ou adaptação de formas e sequências",
                                    "Balanço entre tradição e expressão individual"
                                ],
                                "project": {
                                    "title": "Criação Técnica",
                                    "description": "Desenvolver uma sequência técnica original baseada nos princípios tradicionais"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Liderança e Instrução",
                        "module_description": "Desenvolva habilidades para transmitir conhecimento e liderar na comunidade marcial",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos da Instrução",
                                "objectives": "Aprender princípios básicos para ensinar artes marciais",
                                "steps": [
                                    "Metodologia de ensino específica da arte marcial",
                                    "Progressão pedagógica e adaptação por nível e idade",
                                    "Comunicação efetiva e demonstração técnica",
                                    "Feedback construtivo e correções respeitosas"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Projeto de Mentoria",
                            "description": "Atuar como assistente de instrução para praticantes iniciantes",
                            "deliverables": ["Plano de aulas assistidas", "Condução de segmentos específicos de treino", "Feedback dos instruídos e instrutores principais"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Desenvolvimento Marcial",
                    "description": "Desenvolver um projeto abrangente que integre aspectos técnicos, filosóficos e sociais da arte marcial",
                    "requirements": [
                        "Demonstração técnica de alto nível",
                        "Ensino e compartilhamento de conhecimento",
                        "Elaboração de material instrutivo (escrito, visual)",
                        "Aplicação da filosofia marcial em projetos comunitários",
                        "Reflexão profunda sobre o impacto da arte marcial no desenvolvimento pessoal"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Artes Marciais Orientais Tradicionais",
                "description": "Estudo aprofundado de artes marciais como Karatê, Kung Fu, Taekwondo ou Judô",
                "age_range": "10-17 anos",
                "modules": [
                    "Sistema Técnico Tradicional",
                    "Formas e Katas Avançados",
                    "Filosofia Oriental e Valores Marciais",
                    "Aplicações Práticas e Combate"
                ],
                "final_project": {
                    "title": "Demonstração de Arte Tradicional",
                    "description": "Preparar uma demonstração completa dos aspectos técnicos e filosóficos da arte marcial escolhida"
                }
            },
            {
                "name": "Artes Marciais Modernas e Mistas",
                "description": "Foco em sistemas marciais contemporâneos como MMA, Kickboxing ou Defesa Pessoal Moderna",
                "age_range": "14-17 anos",
                "modules": [
                    "Sistemas de Combate Multidisciplinar",
                    "Condicionamento Físico Específico",
                    "Estratégia e Tática de Combate",
                    "Desenvolvimento Mental e Preparação"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Instrutor de Artes Marciais",
                "Atleta Profissional de Competição",
                "Especialista em Defesa Pessoal",
                "Coach de Desenvolvimento Pessoal",
                "Terapeuta Corporal",
                "Coordenador de Programas Juvenis",
                "Preparador Físico Especializado",
                "Especialista em Prevenção de Bullying"
            ],
            "day_in_life": [
                "Um instrutor de artes marciais divide seu dia entre treino pessoal, preparação de aulas e ensino para diferentes níveis",
                "Um atleta competitivo segue uma rotina rigorosa de treinamento técnico, físico, tático e mental",
                "Um especialista em defesa pessoal pode trabalhar com grupos específicos como mulheres, crianças ou profissionais de segurança",
                "Um terapeuta que utiliza princípios de artes marciais trabalha integrando movimento, respiração e concentração para bem-estar"
            ],
            "educational_paths": [
                "Formação técnica em federações e associações de artes marciais",
                "Graduação em Educação Física com especialização em artes marciais",
                "Certificações específicas por estilo e nível",
                "Estudos complementares em áreas como psicologia, pedagogia ou terapia corporal",
                "Intercâmbios culturais e técnicos em países de origem das artes"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica"],
            "cross_curricular": ["História (cultura oriental)", "Filosofia", "Ética", "Psicologia", "Geografia"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Artes Marciais"] = artes_marciais_subarea
    area_ref.set(area_data)

    return area_data

def setup_treinamento_fisico_condicionamento_subarea(db):
    """
    Configura a subárea de Treinamento Físico e Condicionamento dentro da área de Esportes e Atividades Físicas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Esportes e Atividades Físicas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Esportes e Atividades Físicas",
            "description": "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    treinamento_fisico_subarea = {
        "name": "Treinamento Físico e Condicionamento",
        "description": "Desenvolva suas capacidades físicas, aprenda a treinar com eficiência e segurança, e entenda como o corpo responde ao exercício físico para alcançar seus objetivos de saúde e performance.",
        "estimated_time": "3-18 meses (dependendo da dedicação)",
        "icon": "dumbbell",
        "references": [
            {"title": "Academia do Treinamento", "url": "https://www.academiadotreinamento.com.br/"},
            {"title": "Fitness Education Foundation", "url": "https://www.fitnesseducation.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução aos princípios básicos do treinamento físico e desenvolvimento de rotinas simples",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Compreender os componentes básicos da aptidão física e seus benefícios para a saúde",
                    "Executar exercícios fundamentais com técnica adequada e segura",
                    "Desenvolver uma rotina básica de atividade física balanceada",
                    "Entender a importância da nutrição e recuperação para o condicionamento físico"
                ],
                "modules": [
                    {
                        "module_title": "Fundamentos da Aptidão Física",
                        "module_description": "Descubra os componentes do condicionamento físico e seus benefícios para a saúde",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Componentes da Aptidão Física",
                                "objectives": "Compreender os diferentes aspectos que compõem um corpo saudável e condicionado",
                                "estimated_time": "60 minutos",
                                "content_summary": "Exploração dos principais componentes da aptidão física e sua importância para a saúde e qualidade de vida",
                                "steps": [
                                    "Resistência cardiorrespiratória: funcionamento e benefícios",
                                    "Força e resistência muscular: tipos e importância",
                                    "Flexibilidade e mobilidade articular",
                                    "Composição corporal e sua relação com a saúde"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que é importante desenvolver todos os componentes da aptidão física, e não apenas um deles?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Desenvolver todos os componentes da aptidão física proporciona um equilíbrio que beneficia a saúde integral, pois cada componente tem funções específicas que se complementam. Um desenvolvimento equilibrado previne lesões, melhora a capacidade funcional para atividades cotidianas, contribui para a saúde metabólica e cardiovascular, e permite melhor qualidade de vida e longevidade. Focar em apenas um componente pode criar desequilíbrios e limitar os benefícios gerais do exercício físico."
                                    },
                                    {
                                        "question": "Qual dos seguintes exercícios é mais indicado para desenvolver a resistência cardiorrespiratória?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Flexões de braço",
                                            "Corrida contínua de 20 minutos",
                                            "Alongamento de isquiotibiais",
                                            "Levantamento de peso máximo"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "avaliação",
                                        "title": "Meu Perfil de Aptidão",
                                        "description": "Autoavaliação simplificada dos diferentes componentes da aptidão física"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Componentes da Aptidão Física Explicados",
                                     "url": "https://exemplo.com/video_aptidao"},
                                    {"type": "infográfico", "title": "Benefícios do Condicionamento Físico",
                                     "url": "https://exemplo.com/infografico_beneficios"}
                                ]
                            },
                            {
                                "lesson_title": "Exercício e Saúde",
                                "objectives": "Entender como a atividade física regular impacta diversos sistemas do corpo",
                                "estimated_time": "55 minutos",
                                "steps": [
                                    "Benefícios para o sistema cardiovascular",
                                    "Efeitos nos sistemas muscular e esquelético",
                                    "Impacto na saúde mental e bem-estar emocional",
                                    "Influência no metabolismo e controle de peso"
                                ],
                                "exercises": [
                                    {
                                        "question": "Liste três benefícios do exercício físico regular para a saúde mental e bem-estar emocional.",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Podem incluir: redução do estresse e ansiedade, melhora do humor através da liberação de endorfinas, melhoria da qualidade do sono, aumento da autoestima e autoconfiança, maior capacidade de concentração, redução de sintomas depressivos, sensação de realização e propósito, etc."
                                    }
                                ],
                                "project": {
                                    "title": "Diário de Atividade e Bem-estar",
                                    "description": "Manter um registro diário de atividades físicas e percepções de bem-estar por uma semana",
                                    "expected_outcome": "Compreensão da relação entre exercício e sensação de bem-estar",
                                    "estimated_time": "5-10 minutos diários por uma semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Avaliação de Conhecimentos Básicos",
                            "format": "Questionário + reflexão sobre hábitos pessoais",
                            "passing_score": "70% de acertos no questionário",
                            "time_limit": "30 minutos",
                            "certificate": "Fundamentos da Aptidão Física - Nível 1"
                        }
                    },
                    {
                        "module_title": "Exercícios Fundamentais",
                        "module_description": "Aprenda a executar corretamente exercícios básicos para diferentes partes do corpo",
                        "estimated_time": "6 semanas",
                        "prerequisites": ["Fundamentos da Aptidão Física"],
                        "lessons": [
                            {
                                "lesson_title": "Treinamento de Corpo Inteiro",
                                "objectives": "Aprender exercícios básicos que trabalham grandes grupos musculares",
                                "steps": [
                                    "Exercícios para membros inferiores: agachamento, afundo",
                                    "Exercícios para parte superior: flexões modificadas, remadas",
                                    "Exercícios para core: prancha, superman",
                                    "Técnica correta e alinhamento postural"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais são os erros mais comuns na execução do agachamento e como corrigi-los?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "O único erro possível é não agachar suficientemente",
                                            "Joelhos para dentro, elevação dos calcanhares, e inclinação excessiva do tronco - corrigidos com atenção ao alinhamento e possivelmente redução da amplitude",
                                            "Agachar além do paralelo - corrigido limitando a amplitude",
                                            "Usar peso adicional - corrigido sempre fazendo sem peso"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Circuito Básico",
                                    "description": "Criar e executar um circuito simples com 5-6 exercícios para corpo inteiro",
                                    "steps": [
                                        "Selecionar exercícios para diferentes partes do corpo",
                                        "Definir número de repetições ou tempo adequados",
                                        "Organizar a sequência lógica de exercícios",
                                        "Executar o circuito 2-3 vezes com intervalos"
                                    ],
                                    "estimated_time": "45 minutos para criação + 30 minutos para execução"
                                }
                            },
                            {
                                "lesson_title": "Treinamento Cardiovascular Básico",
                                "objectives": "Aprender diferentes formas de desenvolver a resistência cardiorrespiratória",
                                "steps": [
                                    "Caminhada e corrida: técnica e progressão",
                                    "Ciclismo e natação: fundamentos básicos",
                                    "Exercícios cardiovasculares com o peso corporal",
                                    "Monitoramento da intensidade (percepção de esforço, frequência cardíaca)"
                                ],
                                "project": {
                                    "title": "Programa Cardio",
                                    "description": "Criar um programa simples de treinamento cardiovascular para duas semanas"
                                }
                            },
                            {
                                "lesson_title": "Flexibilidade e Mobilidade",
                                "objectives": "Aprender técnicas para melhorar a amplitude de movimento",
                                "steps": [
                                    "Diferença entre flexibilidade e mobilidade",
                                    "Alongamentos estáticos principais para grandes grupos musculares",
                                    "Mobilidade dinâmica para principais articulações",
                                    "Incorporação na rotina diária e aquecimento"
                                ],
                                "project": {
                                    "title": "Rotina de Mobilidade",
                                    "description": "Criar uma rotina curta de mobilidade para ser feita diariamente"
                                }
                            },
                            {
                                "lesson_title": "Nutrição Básica para Atividade Física",
                                "objectives": "Compreender os princípios fundamentais da alimentação para o exercício",
                                "steps": [
                                    "Macronutrientes e sua função no exercício",
                                    "Hidratação antes, durante e após a atividade",
                                    "Alimentação pré e pós-treino",
                                    "Mitos comuns sobre nutrição esportiva"
                                ],
                                "project": {
                                    "title": "Diário Alimentar",
                                    "description": "Registrar alimentação por três dias e analisar relação com atividades físicas"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Minha Primeira Semana de Treino",
                            "description": "Planejar e executar uma semana completa de treinos balanceados",
                            "deliverables": ["Plano semanal detalhado", "Registro da execução dos treinos", "Reflexão sobre a experiência"],
                            "estimated_time": "1 semana para execução + planejamento"
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Condicionamento Físico Pessoal",
                    "description": "Desenvolver e implementar um programa pessoal de 4 semanas para melhorar a aptidão física",
                    "requirements": [
                        "Avaliação inicial de condicionamento (testes simples)",
                        "Definição de objetivos SMART (específicos, mensuráveis, atingíveis, relevantes, temporais)",
                        "Planejamento semanal balanceado incluindo todos os componentes da aptidão",
                        "Execução consistente do programa",
                        "Avaliação final e reflexão sobre resultados e aprendizados"
                    ],
                    "rubric": "Avaliação baseada em planejamento adequado, consistência na execução, compreensão dos princípios e progresso individual",
                    "showcase": "Apresentação dos resultados e aprendizados para a turma"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos do Treinamento Físico",
                    "format": "Teste teórico + demonstração prática de exercícios + apresentação do projeto final",
                    "passing_criteria": "70% de acertos no teste teórico, técnica adequada nos exercícios e projeto completo",
                    "certification": "Condicionamento Físico Básico"
                },
                "suggested_path_forward": ["Treinamento Específico", "Nutrição Esportiva", "Prevenção de Lesões"]
            },
            "intermediario": {
                "description": "Aprofundamento em métodos de treinamento e princípios avançados de condicionamento físico",
                "age_range": "13-16 anos",
                "modules": [
                    {
                        "module_title": "Princípios da Ciência do Treinamento",
                        "module_description": "Compreenda os fundamentos científicos que regem o treinamento eficaz",
                        "estimated_time": "6 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Princípios de Treinamento",
                                "objectives": "Aprender os princípios que determinam a eficácia do treinamento físico",
                                "steps": [
                                    "Especificidade: treinando para objetivos específicos",
                                    "Sobrecarga progressiva: o princípio do desafio crescente",
                                    "Variação: evitando estagnação e adaptações",
                                    "Recuperação: o papel do descanso no desenvolvimento"
                                ]
                            },
                            {
                                "lesson_title": "Periodização Básica",
                                "objectives": "Entender como estruturar o treinamento em ciclos para otimizar resultados",
                                "steps": [
                                    "Conceitos de microciclo, mesociclo e macrociclo",
                                    "Fases de treinamento: preparatória, específica, competitiva, transição",
                                    "Manipulação de volume e intensidade",
                                    "Estruturação do ano de treinamento"
                                ],
                                "project": {
                                    "title": "Meu Plano Periodizado",
                                    "description": "Criar um plano de treinamento periodizado de 12 semanas para um objetivo específico"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Métodos de Treinamento Avançados",
                        "module_description": "Aprenda diferentes métodos para treinar capacidades físicas específicas",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Métodos de Treinamento de Força",
                                "objectives": "Conhecer diferentes abordagens para desenvolver força muscular",
                                "steps": [
                                    "Treinamento com pesos livres vs. máquinas",
                                    "Sistemas de treinamento: séries múltiplas, pirâmide, superset",
                                    "Parâmetros de treinamento: séries, repetições, intervalos, velocidade",
                                    "Progressão e sobrecarga no treinamento de força"
                                ]
                            },
                            {
                                "lesson_title": "Métodos de Treinamento Cardiorrespiratório",
                                "objectives": "Explorar diferentes protocolos para melhorar o condicionamento cardiovascular",
                                "steps": [
                                    "Treinamento contínuo vs. intervalado",
                                    "HIIT (Treinamento Intervalado de Alta Intensidade)",
                                    "Treinamento de limiar: reconhecendo e trabalhando nas zonas",
                                    "Periodização do treinamento cardiorrespiratório"
                                ],
                                "project": {
                                    "title": "Programa HIIT Personalizado",
                                    "description": "Desenvolver e testar um programa de HIIT adaptado às necessidades pessoais"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Treinamento Específico para Objetivo",
                            "description": "Desenvolver e implementar um programa de 4 semanas para um objetivo específico",
                            "deliverables": ["Plano detalhado com justificativa dos métodos escolhidos", "Registro do treinamento", "Avaliação de resultados com métricas objetivas"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Performance Física",
                    "description": "Planejar, executar e avaliar um programa de treinamento específico visando a melhoria de um aspecto da performance",
                    "requirements": [
                        "Seleção de um objetivo específico de performance",
                        "Avaliações iniciais adequadas ao objetivo",
                        "Planejamento periodizado de 8-12 semanas",
                        "Aplicação de métodos de treinamento específicos",
                        "Monitoramento de progresso e ajustes necessários",
                        "Avaliação final e análise crítica dos resultados"
                    ]
                }
            },
            "avancado": {
                "description": "Treinamento especializado, preparação física avançada e fundamentos de prescrição de exercícios",
                "age_range": "15-17 anos",
                "modules": [
                    {
                        "module_title": "Avaliação e Prescrição de Exercícios",
                        "module_description": "Aprenda a avaliar condicionamento físico e prescrever exercícios de forma individualizada",
                        "lessons": [
                            {
                                "lesson_title": "Testes e Avaliações Físicas",
                                "objectives": "Aprender a administrar e interpretar avaliações físicas",
                                "steps": [
                                    "Protocolos de avaliação para diferentes capacidades físicas",
                                    "Testes de campo vs. testes laboratoriais",
                                    "Interpretação de resultados e criação de perfil físico",
                                    "Utilização de dados para prescrição individualizada"
                                ]
                            },
                            {
                                "lesson_title": "Prescrição Individualizada",
                                "objectives": "Desenvolver habilidades para criar programas personalizados",
                                "steps": [
                                    "Análise de necessidades e objetivos individuais",
                                    "Adaptações para diferentes níveis de condicionamento",
                                    "Modificações para limitações e condições específicas",
                                    "Progressão adequada baseada em respostas individuais"
                                ],
                                "project": {
                                    "title": "Estudo de Caso",
                                    "description": "Criar um programa personalizado para um colega com base em avaliação completa"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Preparação Física Especializada",
                        "module_description": "Desenvolva conhecimentos para o treinamento direcionado a objetivos específicos",
                        "lessons": [
                            {
                                "lesson_title": "Preparação Física para Esportes",
                                "objectives": "Aprender a desenvolver programas específicos para diferentes modalidades esportivas",
                                "steps": [
                                    "Análise das demandas físicas por esporte",
                                    "Periodização conforme calendário competitivo",
                                    "Desenvolvimento de capacidades físicas determinantes",
                                    "Integração entre preparação física e técnico-tática"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Programa de Preparação Esportiva",
                            "description": "Desenvolver um programa completo de preparação física para um esporte específico",
                            "deliverables": ["Análise das demandas do esporte", "Programa periodizado de uma temporada", "Estratégias de monitoramento e avaliação"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Integrado de Condicionamento Físico",
                    "description": "Desenvolver um projeto abrangente demonstrando conhecimentos avançados em treinamento físico",
                    "requirements": [
                        "Seleção de população-alvo e objetivos específicos",
                        "Criação de bateria de avaliações apropriadas",
                        "Desenvolvimento de programa completo e periodizado",
                        "Fundamentação científica das escolhas de métodos e exercícios",
                        "Estratégias de monitoramento e critérios de progressão",
                        "Apresentação profissional do projeto com justificativas"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Preparação Física para Performance",
                "description": "Foco no desenvolvimento de capacidades físicas para alto rendimento em esportes ou atividades específicas",
                "age_range": "14-17 anos",
                "modules": [
                    "Treinamento de Força e Potência Avançado",
                    "Velocidade e Agilidade",
                    "Avaliação de Performance Específica",
                    "Periodização Avançada para Competição"
                ],
                "final_project": {
                    "title": "Programa de Preparação para Performance",
                    "description": "Criar um programa completo de preparação física para uma modalidade específica"
                }
            },
            {
                "name": "Fitness e Condicionamento para Saúde",
                "description": "Desenvolvimento de programas voltados para saúde, qualidade de vida e bem-estar",
                "age_range": "13-17 anos",
                "modules": [
                    "Exercício para Prevenção de Doenças Crônicas",
                    "Treinamento Funcional para Vida Diária",
                    "Estratégias para Adesão e Motivação",
                    "Monitoramento de Saúde e Wellness"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Personal Trainer",
                "Preparador Físico",
                "Técnico de Condicionamento",
                "Fisiologista do Exercício",
                "Treinador de Performance",
                "Especialista em Reabilitação",
                "Instrutor de Fitness",
                "Pesquisador em Ciências do Esporte"
            ],
            "day_in_life": [
                "Um personal trainer avalia clientes, planeja programas individualizados e supervisiona treinos",
                "Um preparador físico trabalha com atletas, monitorando capacidades físicas e desenvolvendo programas específicos para performance",
                "Um fisiologista do exercício realiza testes, analisa dados e desenvolve intervenções baseadas em evidências científicas",
                "Um instrutor de fitness planeja e conduz aulas em grupo, motivando os participantes e garantindo a execução correta dos exercícios"
            ],
            "educational_paths": [
                "Graduação em Educação Física, Ciências do Esporte ou Fisiologia do Exercício",
                "Certificações específicas em treinamento (ACSM, NSCA, ACE, etc.)",
                "Especializações em áreas como treinamento funcional, reabilitação, nutrição esportiva",
                "Pós-graduação em áreas específicas das ciências do exercício",
                "Curso técnico em fitness e condicionamento físico"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica", "Biologia básica"],
            "cross_curricular": ["Biologia (fisiologia)", "Física (biomecânica)", "Matemática (cálculos de treinamento)", "Química (metabolismo)"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Treinamento Físico e Condicionamento"] = treinamento_fisico_subarea
    area_ref.set(area_data)

    return area_data

def setup_esportes_aquaticos_subarea(db):
    """
    Configura a subárea de Esportes Aquáticos dentro da área de Esportes e Atividades Físicas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Esportes e Atividades Físicas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Esportes e Atividades Físicas",
            "description": "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    esportes_aquaticos_subarea = {
        "name": "Esportes Aquáticos",
        "description": "Explore o meio aquático através de diferentes modalidades esportivas, desenvolvendo técnicas de natação, habilidades específicas e confiança na água, além de compreender a importância da segurança em ambientes aquáticos.",
        "estimated_time": "3-24 meses (dependendo da dedicação e modalidade escolhida)",
        "icon": "swimming-pool",
        "references": [
            {"title": "Academia de Esportes Aquáticos", "url": "https://www.esportesaquaticos.com.br/"},
            {"title": "Aquatic Sports Association", "url": "https://www.aquaticsports.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução ao meio aquático e desenvolvimento de habilidades básicas de natação",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Desenvolver confiança e adaptação ao meio aquático",
                    "Aprender técnicas básicas de flutuação, respiração e propulsão na água",
                    "Dominar os fundamentos dos principais nados",
                    "Conhecer os princípios de segurança aquática e prevenção de acidentes"
                ],
                "modules": [
                    {
                        "module_title": "Adaptação ao Meio Aquático",
                        "module_description": "Desenvolva confiança e habilidades fundamentais para se sentir seguro na água",
                        "estimated_time": "4 semanas",
                        "difficulty": "moderado",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Ambientação e Primeiros Contatos",
                                "objectives": "Desenvolver familiaridade e conforto no ambiente aquático",
                                "estimated_time": "60 minutos",
                                "content_summary": "Atividades introdutórias para perder o medo e desenvolver confiança na água",
                                "steps": [
                                    "Entrada na água e deslocamentos em pé (caminhada, corrida, saltos)",
                                    "Controle respiratório: imersão gradual, expiração subaquática",
                                    "Abrir os olhos debaixo d'água e recuperar objetos",
                                    "Flutuação assistida em posição ventral e dorsal"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que a respiração adequada é considerada uma das habilidades mais importantes na adaptação ao meio aquático?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "A respiração adequada é fundamental pois permite o controle e conforto necessários para todas as outras habilidades aquáticas. Dominar a expiração subaquática evita engasgos e pânico, permite maior tempo de imersão, facilita a flutuação e posicionamento correto do corpo, e estabelece o ritmo para os nados. É a base da segurança e confiança na água, além de ser essencial para o desenvolvimento técnico posterior."
                                    },
                                    {
                                        "question": "Qual a sequência mais adequada para ensinar a flutuação a um iniciante?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Começar com flutuação livre em água profunda",
                                            "Iniciar com flutuação dorsal assistida, progredindo para ventral assistida e depois versões livres",
                                            "Apenas flutuação ventral com uso de equipamentos",
                                            "Não é necessário aprender flutuação para nadar"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "jogo",
                                        "title": "Caça ao Tesouro Subaquático",
                                        "description": "Recuperar objetos coloridos no fundo da piscina, progredindo em profundidade"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Primeiros Passos na Água",
                                     "url": "https://exemplo.com/video_adaptacao"},
                                    {"type": "infográfico", "title": "Progressão da Adaptação Aquática",
                                     "url": "https://exemplo.com/infografico_adaptacao"}
                                ]
                            },
                            {
                                "lesson_title": "Flutuação e Equilíbrio",
                                "objectives": "Dominar diferentes posições de flutuação e desenvolver equilíbrio aquático",
                                "estimated_time": "60 minutos",
                                "steps": [
                                    "Flutuação em posição de estrela (ventral e dorsal)",
                                    "Flutuação vertical (posição de 'boia')",
                                    "Transições entre diferentes posições de flutuação",
                                    "Rolamentos e rotações no eixo longitudinal"
                                ],
                                "exercises": [
                                    {
                                        "question": "Quais fatores físicos afetam a flutuabilidade de uma pessoa na água?",
                                        "type": "open",
                                        "answer": "Os principais fatores que afetam a flutuabilidade são: composição corporal (proporção de gordura/músculo/osso), capacidade pulmonar e quantidade de ar nos pulmões, densidade corporal geral, estrutura corporal, e nível de relaxamento muscular. Pessoas com maior percentual de gordura corporal tendem a flutuar mais facilmente, assim como indivíduos com pulmões cheios de ar."
                                    }
                                ],
                                "project": {
                                    "title": "Rotina de Flutuação",
                                    "description": "Criar e apresentar uma sequência de diferentes posições de flutuação com transições suaves",
                                    "expected_outcome": "Domínio do equilíbrio aquático e confiança em diferentes posições",
                                    "estimated_time": "30 minutos para preparação + 5 minutos para demonstração"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Avaliação de Adaptação Aquática",
                            "format": "Circuito de estações com diferentes habilidades aquáticas básicas",
                            "passing_score": "Demonstração de conforto e competência básica em todas as estações",
                            "time_limit": "45 minutos",
                            "certificate": "Adaptação Aquática - Nível 1"
                        }
                    },
                    {
                        "module_title": "Fundamentos da Natação",
                        "module_description": "Aprenda as técnicas básicas dos quatro nados competitivos",
                        "estimated_time": "10 semanas",
                        "prerequisites": ["Adaptação ao Meio Aquático"],
                        "lessons": [
                            {
                                "lesson_title": "Propulsão Básica",
                                "objectives": "Aprender técnicas fundamentais de deslocamento na água",
                                "steps": [
                                    "Batimento de pernas em posição ventral e dorsal",
                                    "Movimentos de braços básicos para propulsão",
                                    "Deslizes após impulso na parede",
                                    "Coordenação entre pernas e braços"
                                ],
                                "exercises": [
                                    {
                                        "question": "Qual a importância do deslize na eficiência da natação?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Não tem importância, o importante é bater pernas e braços rapidamente",
                                            "Aproveita o impulso e reduz o arrasto, tornando a natação mais eficiente e econômica",
                                            "Serve apenas para descansar durante o nado",
                                            "É importante apenas para iniciantes, nadadores avançados não precisam deslizar"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Desafio de Propulsão",
                                    "description": "Experimentar diferentes combinações de movimentos propulsivos e comparar eficiência",
                                    "steps": [
                                        "Testar diferentes posições de mãos e braços",
                                        "Comparar batimentos de pernas com diferentes amplitudes",
                                        "Medir distância percorrida com diferentes técnicas",
                                        "Registrar observações sobre eficiência"
                                    ],
                                    "estimated_time": "45 minutos"
                                }
                            },
                            {
                                "lesson_title": "Nado Crawl (Livre)",
                                "objectives": "Aprender a técnica básica do nado crawl",
                                "steps": [
                                    "Posição do corpo e rolamento",
                                    "Batimento de pernas alternado",
                                    "Braçada e recuperação",
                                    "Respiração lateral e coordenação"
                                ],
                                "project": {
                                    "title": "Aperfeiçoamento do Crawl",
                                    "description": "Praticar o nado crawl completo com foco em um aspecto técnico específico"
                                }
                            },
                            {
                                "lesson_title": "Nado Costas",
                                "objectives": "Aprender a técnica básica do nado costas",
                                "steps": [
                                    "Posição do corpo em decúbito dorsal",
                                    "Batimento de pernas alternado",
                                    "Braçada e recuperação por cima da água",
                                    "Coordenação completa e respiração"
                                ],
                                "project": {
                                    "title": "Desafio do Costas",
                                    "description": "Completar um percurso de nado costas mantendo trajetória reta"
                                }
                            },
                            {
                                "lesson_title": "Introdução ao Peito e Borboleta",
                                "objectives": "Conhecer os elementos básicos dos nados peito e borboleta",
                                "steps": [
                                    "Batimento de pernas específico de cada nado",
                                    "Movimentos de braços básicos",
                                    "Coordenação inicial entre braços e pernas",
                                    "Respiração sincronizada com os movimentos"
                                ],
                                "project": {
                                    "title": "Mini-Circuito de Nados",
                                    "description": "Realizar um circuito com elementos dos quatro estilos de nado"
                                }
                            },
                            {
                                "lesson_title": "Segurança Aquática",
                                "objectives": "Aprender princípios fundamentais de segurança em ambientes aquáticos",
                                "steps": [
                                    "Reconhecimento de ambientes aquáticos seguros e perigosos",
                                    "Técnicas de sobrevivência na água (flutuação de sobrevivência, nado de sobrevivência)",
                                    "Procedimentos básicos de prevenção de afogamento",
                                    "Comportamento responsável em ambientes aquáticos"
                                ],
                                "project": {
                                    "title": "Plano de Segurança",
                                    "description": "Desenvolver um plano de segurança para diferentes ambientes aquáticos (piscina, praia, rio)"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Festival Aquático",
                            "description": "Participar de um evento com atividades variadas que demonstrem as habilidades adquiridas",
                            "deliverables": ["Participação em provas de diferentes nados", "Demonstração de habilidades de segurança aquática", "Participação em jogos aquáticos recreativos"],
                            "estimated_time": "Evento de 2-3 horas"
                        }
                    }
                ],
                "final_project": {
                    "title": "Desafio Aquático Multihabilidades",
                    "description": "Completar um circuito que combine diferentes habilidades aquáticas e técnicas de natação",
                    "requirements": [
                        "Demonstração dos quatro nados em distâncias curtas",
                        "Execução de habilidades aquáticas como flutuação, mergulho e recuperação de objetos",
                        "Demonstração de pelo menos uma técnica de segurança aquática",
                        "Participação em uma atividade aquática recreativa em grupo",
                        "Reflexão sobre o processo de aprendizagem e conquistas"
                    ],
                    "rubric": "Avaliação baseada em técnica, confiança na água, segurança e progresso individual",
                    "showcase": "Evento aquático com demonstrações para colegas e familiares"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Fundamentos dos Esportes Aquáticos",
                    "format": "Avaliação prática de habilidades + teste escrito sobre segurança + autoavaliação",
                    "passing_criteria": "Demonstração de técnicas básicas de natação e compreensão de segurança aquática",
                    "certification": "Fundamentos Aquáticos - Nível Iniciante"
                },
                "suggested_path_forward": ["Especialização em Natação", "Polo Aquático Iniciante", "Nado Sincronizado Básico"]
            },
            "intermediario": {
                "description": "Aperfeiçoamento técnico na natação e introdução a diferentes modalidades aquáticas",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Técnica Avançada de Natação",
                        "module_description": "Aperfeiçoe a técnica dos quatro nados competitivos",
                        "estimated_time": "12 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Refinamento Técnico do Crawl e Costas",
                                "objectives": "Corrigir e aprimorar aspectos técnicos específicos dos nados alternados",
                                "steps": [
                                    "Posicionamento da cabeça e alinhamento corporal",
                                    "Rolamento do corpo e rotação do quadril",
                                    "Entrada da mão e fase propulsiva da braçada",
                                    "Coordenação entre braçada, pernada e respiração"
                                ]
                            },
                            {
                                "lesson_title": "Desenvolvimento do Peito e Borboleta",
                                "objectives": "Aprimorar a técnica dos nados simultâneos",
                                "steps": [
                                    "Movimentos ondulatórios e sincronização no borboleta",
                                    "Técnica da pernada e braçada no nado peito",
                                    "Timming e coordenação específica de cada nado",
                                    "Correção de erros comuns e ajustes individuais"
                                ],
                                "project": {
                                    "title": "Análise de Vídeo",
                                    "description": "Gravação e análise da própria técnica comparada com modelos de referência"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Introdução às Modalidades Aquáticas",
                        "module_description": "Conheça e experimente diferentes esportes aquáticos",
                        "estimated_time": "10 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Polo Aquático Básico",
                                "objectives": "Conhecer os fundamentos do polo aquático",
                                "steps": [
                                    "Técnicas específicas de nado e sustentação vertical",
                                    "Controle da bola e passes básicos",
                                    "Regras fundamentais e posições",
                                    "Mini-jogos adaptados"
                                ]
                            },
                            {
                                "lesson_title": "Elementos de Nado Artístico",
                                "objectives": "Explorar movimentos básicos do nado artístico (sincronizado)",
                                "steps": [
                                    "Flutuação em diferentes posições (vertical, barracuda, flamingo)",
                                    "Deslocamentos específicos (retropedalagem, sculling)",
                                    "Figuras básicas e transições",
                                    "Elementos de sincronização em duplas"
                                ],
                                "project": {
                                    "title": "Rotina Básica",
                                    "description": "Criar e apresentar uma pequena rotina com elementos básicos de nado artístico"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Festival Multiaquático",
                            "description": "Participar de um evento que inclua demonstrações das diferentes modalidades aquáticas",
                            "deliverables": ["Participação em pelo menos duas modalidades diferentes", "Colaboração em uma apresentação coletiva", "Reflexão sobre a experiência nas diferentes modalidades"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Aquático Específico",
                    "description": "Desenvolver um projeto focado em uma modalidade aquática escolhida",
                    "requirements": [
                        "Escolha de uma modalidade aquática para aprofundamento",
                        "Pesquisa sobre aspectos técnicos, históricos e competitivos da modalidade",
                        "Desenvolvimento de habilidades específicas através de treinamento direcionado",
                        "Participação em competição interna ou demonstração",
                        "Documentação do processo e reflexão sobre a experiência"
                    ]
                }
            },
            "avancado": {
                "description": "Treinamento especializado em modalidade aquática específica e conceitos avançados",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Especialização Aquática",
                        "module_description": "Desenvolva habilidades avançadas na modalidade aquática escolhida",
                        "lessons": [
                            {
                                "lesson_title": "Treinamento Específico",
                                "objectives": "Aprofundar conhecimentos e técnicas específicas da modalidade escolhida",
                                "steps": [
                                    "Análise biomecânica específica da modalidade",
                                    "Desenvolvimento de qualidades físicas determinantes",
                                    "Técnicas avançadas específicas",
                                    "Aspectos táticos e estratégicos (quando aplicável)"
                                ]
                            },
                            {
                                "lesson_title": "Preparação para Competição",
                                "objectives": "Desenvolver prontidão física e mental para eventos competitivos",
                                "steps": [
                                    "Periodização do treinamento para competições",
                                    "Simulações e treinamento sob pressão",
                                    "Estratégias de preparação mental",
                                    "Rotinas pré-competitivas e planejamento de prova"
                                ],
                                "project": {
                                    "title": "Plano Competitivo",
                                    "description": "Desenvolver um plano detalhado de preparação para uma competição específica"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Ciência Aplicada aos Esportes Aquáticos",
                        "module_description": "Compreenda os princípios científicos que fundamentam a performance aquática",
                        "lessons": [
                            {
                                "lesson_title": "Hidrodinâmica Aplicada",
                                "objectives": "Entender como as forças aquáticas afetam o desempenho",
                                "steps": [
                                    "Princípios básicos de hidrodinâmica: arrasto, propulsão, flutuação",
                                    "Perfis corporais e posicionamentos eficientes",
                                    "Técnicas para redução de arrasto",
                                    "Aplicações práticas na modalidade específica"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Análise de Performance",
                            "description": "Realizar uma análise detalhada da própria performance usando princípios científicos",
                            "deliverables": ["Análise técnica baseada em vídeo", "Identificação de pontos fortes e áreas para melhoria", "Plano de ação para otimização da performance"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Excelência Aquática",
                    "description": "Desenvolver um projeto abrangente visando excelência na modalidade aquática escolhida",
                    "requirements": [
                        "Diagnóstico avançado de performance atual",
                        "Plano de desenvolvimento técnico, físico e mental",
                        "Implementação e ajustes ao longo de um ciclo de treinamento",
                        "Participação em competição de nível avançado",
                        "Análise de resultados e planejamento futuro",
                        "Possível elemento de mentoria para praticantes iniciantes"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Natação Competitiva",
                "description": "Desenvolvimento avançado nas técnicas e preparação para competições de natação",
                "age_range": "12-17 anos",
                "modules": [
                    "Técnica Avançada dos Quatro Estilos",
                    "Treinamento Específico para Provas",
                    "Saídas, Viradas e Chegadas",
                    "Preparação para Competições"
                ],
                "final_project": {
                    "title": "Ciclo Competitivo",
                    "description": "Planejar e executar um ciclo completo de preparação para competição"
                }
            },
            {
                "name": "Polo Aquático",
                "description": "Desenvolvimento de habilidades técnicas e táticas para o polo aquático",
                "age_range": "13-17 anos",
                "modules": [
                    "Técnicas Específicas de Deslocamento",
                    "Fundamentos com Bola (passe, recepção, arremesso)",
                    "Sistemas Táticos Ofensivos e Defensivos",
                    "Preparação Específica para o Jogo"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Atleta Profissional de Esportes Aquáticos",
                "Professor/Instrutor de Natação",
                "Treinador de Modalidades Aquáticas",
                "Guarda-vidas",
                "Preparador Físico para Esportes Aquáticos",
                "Fisioterapeuta Aquático",
                "Árbitro/Oficial de Competições",
                "Gestor de Instalações Aquáticas"
            ],
            "day_in_life": [
                "Um atleta de natação segue rotina rigorosa de treinamentos na água e em terra, além de cuidados com alimentação e recuperação",
                "Um professor de natação planeja aulas para diferentes níveis, ensina técnicas específicas e garante a segurança dos alunos",
                "Um guarda-vidas monitora constantemente os banhistas, previne situações de risco e está preparado para resgates",
                "Um treinador de polo aquático desenvolve estratégias de jogo, conduz treinamentos técnicos e táticos, e orienta a equipe durante competições"
            ],
            "educational_paths": [
                "Graduação em Educação Física com especialização em esportes aquáticos",
                "Certificações específicas de federações de modalidades aquáticas",
                "Cursos de formação em segurança aquática e salvamento",
                "Especializações em treinamento esportivo ou fisiologia aplicada aos esportes aquáticos",
                "Formação em arbitragem de modalidades aquáticas"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica"],
            "cross_curricular": ["Física (hidrodinâmica)", "Biologia", "Educação Ambiental (em ambientes naturais)", "Segurança"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Esportes Aquáticos"] = esportes_aquaticos_subarea
    area_ref.set(area_data)

    return area_data


def setup_atividades_ar_livre_aventura_subarea(db):
    """
    Configura a subárea de Atividades ao Ar Livre e Aventura dentro da área de Esportes e Atividades Físicas,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    area_ref = db.collection("learning_paths").document("Esportes e Atividades Físicas")
    area_doc = area_ref.get()

    if not area_doc.exists:
        area_data = {
            "name": "Esportes e Atividades Físicas",
            "description": "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",
            "subareas": {}
        }
        area_ref.set(area_data)
    else:
        area_data = area_doc.to_dict()

    atividades_ar_livre_aventura_subarea = {
        "name": "Atividades ao Ar Livre e Aventura",
        "description": "Explore o mundo natural através de atividades físicas ao ar livre, desenvolvendo habilidades de aventura, conexão com a natureza, técnicas de sobrevivência e consciência ambiental.",
        "estimated_time": "3-24 meses (dependendo da dedicação e modalidades escolhidas)",
        "icon": "hiking",
        "references": [
            {"title": "Associação de Esportes de Aventura", "url": "https://www.aventuranatureza.com.br/"},
            {"title": "Outdoor Adventure Education", "url": "https://www.outdooradventureeducation.org/"}
        ],
        "levels": {
            "iniciante": {
                "description": "Introdução às atividades ao ar livre e primeiras experiências em ambientes naturais",
                "age_range": "10-14 anos",
                "learning_outcomes": [
                    "Desenvolver habilidades básicas para atividades ao ar livre em segurança",
                    "Compreender princípios de mínimo impacto ambiental e conservação da natureza",
                    "Adquirir conhecimentos iniciais de orientação, acampamento e caminhada",
                    "Cultivar apreciação pela natureza e confiança em ambientes ao ar livre"
                ],
                "modules": [
                    {
                        "module_title": "Introdução às Atividades Outdoor",
                        "module_description": "Conheça os fundamentos e princípios básicos das atividades ao ar livre",
                        "estimated_time": "4 semanas",
                        "difficulty": "fácil",
                        "fun_factor": "alto",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos das Atividades ao Ar Livre",
                                "objectives": "Compreender os princípios básicos, benefícios e modalidades de atividades na natureza",
                                "estimated_time": "60 minutos",
                                "content_summary": "Introdução ao mundo das atividades ao ar livre, seus princípios e diversidade de experiências",
                                "steps": [
                                    "Tipos de atividades outdoor: trekking, acampamento, escalada, canoagem, etc.",
                                    "Benefícios físicos, mentais e sociais das atividades na natureza",
                                    "Princípios do 'Não Deixe Rastros' (Leave No Trace)",
                                    "Conceitos de desafio, risco calculado e zona de conforto"
                                ],
                                "exercises": [
                                    {
                                        "question": "Por que os princípios de 'Não Deixe Rastros' são fundamentais para as atividades ao ar livre?",
                                        "type": "open",
                                        "suggested_time": "10 minutos",
                                        "answer": "Os princípios de 'Não Deixe Rastros' são fundamentais porque preservam os ambientes naturais para futuras visitas e outros visitantes, minimizam o impacto humano nos ecossistemas frágeis, protegem a flora e fauna locais, mantêm a qualidade da experiência na natureza, educam sobre responsabilidade ambiental, e promovem uma ética de respeito e conservação. Esses princípios garantem a sustentabilidade das atividades outdoor a longo prazo e ajudam a formar uma consciência de cuidado com o meio ambiente."
                                    },
                                    {
                                        "question": "Qual dos seguintes NÃO é considerado um benefício direto das atividades ao ar livre?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Melhoria da condição física e cardiovascular",
                                            "Redução do estresse e conexão com a natureza",
                                            "Ganho automático de seguidores nas redes sociais",
                                            "Desenvolvimento de habilidades de resolução de problemas"
                                        ],
                                        "correct_answer": 2
                                    }
                                ],
                                "interactive_elements": [
                                    {
                                        "type": "atividade",
                                        "title": "Mapa das Possibilidades",
                                        "description": "Em grupos, criar um mapa visual das diferentes atividades ao ar livre e seus ambientes"
                                    }
                                ],
                                "resources": [
                                    {"type": "vídeo", "title": "Descobrindo o Mundo Outdoor",
                                     "url": "https://exemplo.com/video_outdoor"},
                                    {"type": "infográfico", "title": "Princípios de Não Deixe Rastros",
                                     "url": "https://exemplo.com/infografico_lnt"}
                                ]
                            },
                            {
                                "lesson_title": "Segurança e Preparação Básica",
                                "objectives": "Aprender fundamentos de segurança e preparação para atividades na natureza",
                                "estimated_time": "75 minutos",
                                "steps": [
                                    "Equipamentos essenciais e roupas adequadas",
                                    "Planejamento de saídas e avaliação de condições",
                                    "Noções básicas de primeiros socorros outdoor",
                                    "Comunicação e protocolos de emergência"
                                ],
                                "exercises": [
                                    {
                                        "question": "Monte uma lista dos 10 itens essenciais que você levaria para uma caminhada de um dia. Justifique brevemente a importância de cada item.",
                                        "type": "open",
                                        "answer": "Resposta pessoal. Podem incluir: mapa e bússola/GPS (navegação), protetor solar (proteção contra raios UV), roupas extras (mudanças climáticas), lanterna/farol (emergência/atraso), kit de primeiros socorros (lesões), fósforos/isqueiro (emergência), canivete (ferramenta multiuso), alimentos extras (energia/atraso), água (hidratação), abrigo de emergência (proteção contra intempéries)."
                                    }
                                ],
                                "project": {
                                    "title": "Kit de Essenciais",
                                    "description": "Montar um kit básico de itens essenciais para atividades ao ar livre",
                                    "expected_outcome": "Compreensão da importância da preparação adequada",
                                    "estimated_time": "Projeto para casa - 1 semana"
                                }
                            }
                        ],
                        "module_assessment": {
                            "title": "Avaliação de Fundamentos Outdoor",
                            "format": "Teste teórico + apresentação de kit preparado + planejamento simples",
                            "passing_score": "Demonstração adequada de conhecimentos básicos de segurança e preparação",
                            "time_limit": "45 minutos",
                            "certificate": "Fundamentos Outdoor - Nível 1"
                        }
                    },
                    {
                        "module_title": "Primeiras Aventuras",
                        "module_description": "Experimente atividades introdutórias em ambiente natural com supervisão",
                        "estimated_time": "8 semanas",
                        "prerequisites": ["Introdução às Atividades Outdoor"],
                        "lessons": [
                            {
                                "lesson_title": "Caminhada em Trilhas",
                                "objectives": "Aprender técnicas básicas para caminhadas em trilhas",
                                "steps": [
                                    "Técnica de caminhada e postura",
                                    "Navegação básica e leitura de sinalizações",
                                    "Gerenciamento de energia e hidratação",
                                    "Observação da natureza durante a trilha"
                                ],
                                "exercises": [
                                    {
                                        "question": "Ao caminhar em uma descida íngreme, qual técnica você deve utilizar para reduzir o impacto nas articulações?",
                                        "type": "multiple_choice",
                                        "options": [
                                            "Correr rapidamente para descer logo",
                                            "Caminhar lateralmente em zigue-zague, controlando a velocidade e mantendo o centro de gravidade baixo",
                                            "Pular de pedra em pedra para evitar o contato com o solo",
                                            "Sempre descer de costas como em uma escada"
                                        ],
                                        "correct_answer": 1
                                    }
                                ],
                                "project": {
                                    "title": "Mini-Trilha Guiada",
                                    "description": "Participar de uma caminhada curta em trilha fácil com supervisão",
                                    "steps": [
                                        "Preparação e verificação de equipamentos",
                                        "Revisão do mapa e características da trilha",
                                        "Caminhada com atenção às instruções do líder",
                                        "Prática de técnicas básicas durante o percurso"
                                    ],
                                    "estimated_time": "2-3 horas incluindo preparação"
                                }
                            },
                            {
                                "lesson_title": "Acampamento Básico",
                                "objectives": "Aprender fundamentos de acampamento com mínimo impacto",
                                "steps": [
                                    "Escolha de local adequado e montagem de barracas",
                                    "Organização do acampamento e cuidados com alimentos",
                                    "Técnicas básicas de fogo (quando permitido) e cozinha outdoor",
                                    "Princípios de 'Não Deixe Rastros' aplicados ao acampamento"
                                ],
                                "project": {
                                    "title": "Simulação de Acampamento",
                                    "description": "Participar de uma atividade de montagem de acampamento em ambiente controlado"
                                }
                            },
                            {
                                "lesson_title": "Orientação Básica",
                                "objectives": "Desenvolver habilidades iniciais de orientação e navegação",
                                "steps": [
                                    "Uso de bússola e pontos cardeais",
                                    "Leitura básica de mapas topográficos",
                                    "Identificação de pontos de referência naturais",
                                    "Navegação simples em ambiente controlado"
                                ],
                                "project": {
                                    "title": "Caça ao Tesouro",
                                    "description": "Participar de atividade de navegação em pequeno percurso utilizando mapa e bússola"
                                }
                            },
                            {
                                "lesson_title": "Observação e Conexão com a Natureza",
                                "objectives": "Desenvolver habilidades de observação e apreciação do ambiente natural",
                                "steps": [
                                    "Técnicas de observação da fauna e flora",
                                    "Identificação básica de espécies comuns",
                                    "Documentação através de fotografia ou diário de campo",
                                    "Práticas contemplativas e consciência sensorial"
                                ],
                                "project": {
                                    "title": "Diário Naturalista",
                                    "description": "Criar um registro de observações durante uma atividade ao ar livre"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Mini-Expedição",
                            "description": "Participar de uma expedição supervisionada de um dia integrando diferentes habilidades aprendidas",
                            "deliverables": ["Participação ativa na expedição", "Registro da experiência (fotos, diário, desenhos)", "Reflexão sobre aprendizados e desafios"],
                            "estimated_time": "1 dia completo + preparação prévia"
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Aventura Responsável",
                    "description": "Planejar e participar de uma atividade ao ar livre que demonstre as habilidades e conhecimentos adquiridos",
                    "requirements": [
                        "Planejamento detalhado da atividade incluindo equipamentos, rotas e considerações de segurança",
                        "Aplicação de princípios de mínimo impacto ambiental",
                        "Participação ativa com demonstração de habilidades básicas",
                        "Documentação da experiência (fotos, vídeos, diário)",
                        "Apresentação sobre a atividade e aprendizados para a turma"
                    ],
                    "rubric": "Avaliação baseada em planejamento adequado, práticas responsáveis, habilidades demonstradas e reflexão sobre a experiência",
                    "showcase": "Feira de Atividades Outdoor com apresentações dos projetos"
                },
                "final_assessment": {
                    "title": "Avaliação Final: Atividades ao Ar Livre Básicas",
                    "format": "Avaliação teórica + demonstração prática de habilidades + projeto final",
                    "passing_criteria": "Demonstração de conhecimentos básicos de segurança, habilidades técnicas fundamentais e princípios de mínimo impacto",
                    "certification": "Aventureiro Responsável - Nível Iniciante"
                },
                "suggested_path_forward": ["Especialização em Modalidades Específicas", "Certificações em Primeiros Socorros", "Liderança Outdoor"]
            },
            "intermediario": {
                "description": "Desenvolvimento de habilidades específicas e experiências mais desafiadoras em ambiente natural",
                "age_range": "12-16 anos",
                "modules": [
                    {
                        "module_title": "Habilidades Técnicas Específicas",
                        "module_description": "Desenvolva competência em atividades outdoor específicas",
                        "estimated_time": "12 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Trekking e Trilhas",
                                "objectives": "Aprofundar habilidades de caminhada em trilhas mais desafiadoras",
                                "steps": [
                                    "Técnicas avançadas de caminhada em diferentes terrenos",
                                    "Travessia de obstáculos naturais (riachos, campos pedregosos)",
                                    "Planejamento de rotas e gestão de itinerários",
                                    "Caminhadas com mochila carregada (técnicas de peso e distribuição)"
                                ]
                            },
                            {
                                "lesson_title": "Técnicas Verticais Básicas",
                                "objectives": "Aprender fundamentos de atividades verticais como escalada e rapel",
                                "steps": [
                                    "Equipamentos de segurança e sua utilização",
                                    "Nós fundamentais e sua aplicação",
                                    "Técnicas básicas de escalada em rocha (boulder e top rope)",
                                    "Técnicas de rapel supervisionado"
                                ],
                                "project": {
                                    "title": "Dia de Escalada",
                                    "description": "Participar de uma sessão de escalada em ambiente controlado (parede artificial ou via fácil natural)"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Planejamento e Segurança Avançados",
                        "module_description": "Aprenda a planejar expedições mais complexas com foco em segurança",
                        "estimated_time": "8 semanas",
                        "lessons": [
                            {
                                "lesson_title": "Navegação Avançada",
                                "objectives": "Desenvolver habilidades de navegação em ambientes variados",
                                "steps": [
                                    "Leitura avançada de mapas topográficos",
                                    "Navegação em condições de baixa visibilidade",
                                    "Uso de GPS e tecnologias de navegação",
                                    "Triangulação e técnicas de localização"
                                ]
                            },
                            {
                                "lesson_title": "Primeiros Socorros em Ambientes Remotos",
                                "objectives": "Aprender a lidar com emergências longe de recursos médicos",
                                "steps": [
                                    "Avaliação de pacientes e gerenciamento de cenários",
                                    "Tratamento de lesões comuns em atividades outdoor",
                                    "Imobilizações improvisadas e transporte de vítimas",
                                    "Protocolos de evacuação e comunicação de emergência"
                                ],
                                "project": {
                                    "title": "Simulações de Emergência",
                                    "description": "Participar de cenários simulados de emergência em ambiente outdoor"
                                }
                            }
                        ],
                        "module_project": {
                            "title": "Expedição Planejada",
                            "description": "Planejar e executar uma expedição de dois dias com pernoite em ambiente natural",
                            "deliverables": ["Plano detalhado da expedição", "Análise de riscos e plano de contingência", "Execução com sucesso da atividade", "Relatório pós-atividade com análise da experiência"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto de Aventura Intermediária",
                    "description": "Planejar e liderar uma atividade outdoor para um pequeno grupo",
                    "requirements": [
                        "Seleção de uma modalidade outdoor para aprofundamento",
                        "Planejamento detalhado com análise de riscos",
                        "Liderança parcial da atividade com supervisão",
                        "Aplicação de habilidades técnicas específicas",
                        "Facilitação da experiência para outros participantes",
                        "Documentação completa e análise crítica da atividade"
                    ]
                }
            },
            "avancado": {
                "description": "Desenvolvimento de liderança, habilidades avançadas e planejamento de expedições",
                "age_range": "14-17 anos",
                "modules": [
                    {
                        "module_title": "Liderança em Ambientes Naturais",
                        "module_description": "Desenvolva habilidades para liderar grupos em atividades ao ar livre",
                        "lessons": [
                            {
                                "lesson_title": "Fundamentos da Liderança Outdoor",
                                "objectives": "Compreender os princípios de liderança em ambientes naturais",
                                "steps": [
                                    "Estilos de liderança e sua aplicação em diferentes contextos",
                                    "Gerenciamento de riscos e tomada de decisão",
                                    "Comunicação efetiva em grupos e em emergências",
                                    "Facilitação de experiências significativas na natureza"
                                ]
                            },
                            {
                                "lesson_title": "Instrução e Facilitação",
                                "objectives": "Desenvolver habilidades para ensinar técnicas outdoor e facilitar experiências",
                                "steps": [
                                    "Métodos de ensino de habilidades técnicas",
                                    "Feedback construtivo e progressão de aprendizado",
                                    "Adaptação para diferentes perfis de aprendizado",
                                    "Criação de experiências educativas na natureza"
                                ],
                                "project": {
                                    "title": "Micro-Ensino",
                                    "description": "Planejar e executar uma pequena aula sobre uma habilidade outdoor específica"
                                }
                            }
                        ]
                    },
                    {
                        "module_title": "Expedições e Projetos Avançados",
                        "module_description": "Planeje e execute projetos outdoor complexos e expedições desafiadoras",
                        "lessons": [
                            {
                                "lesson_title": "Planejamento de Expedições",
                                "objectives": "Aprender a planejar e organizar expedições de múltiplos dias",
                                "steps": [
                                    "Pesquisa e seleção de destinos",
                                    "Logística, suprimentos e equipamentos",
                                    "Itinerários, rotas alternativas e pontos de saída",
                                    "Considerações ambientais e permisos necessários"
                                ]
                            }
                        ],
                        "module_project": {
                            "title": "Expedição Autoguiada",
                            "description": "Planejar e liderar uma expedição de múltiplos dias para um grupo pequeno",
                            "deliverables": ["Projeto completo da expedição", "Execução com supervisão mínima", "Documentação e análise crítica", "Apresentação da experiência e aprendizados"]
                        }
                    }
                ],
                "final_project": {
                    "title": "Projeto Outdoor de Impacto",
                    "description": "Desenvolver um projeto significativo que combine aventura, liderança e impacto positivo",
                    "requirements": [
                        "Planejamento de atividade outdoor avançada com componente educativo ou de serviço",
                        "Liderança completa da atividade com supervisão apenas de segurança",
                        "Integração de princípios de sustentabilidade e educação ambiental",
                        "Desenvolvimento de material educativo relacionado à atividade",
                        "Documentação profissional e avaliação de impacto do projeto",
                        "Apresentação pública dos resultados e aprendizados"
                    ]
                }
            }
        },
        "specializations": [
            {
                "name": "Montanhismo e Escalada",
                "description": "Desenvolvimento de habilidades específicas para atividades em ambiente de montanha",
                "age_range": "14-17 anos",
                "modules": [
                    "Técnicas Verticais Avançadas",
                    "Escalada em Rocha Natural",
                    "Montanhismo e Alta Montanha",
                    "Planejamento de Expedições Verticais"
                ],
                "final_project": {
                    "title": "Projeto de Escalada",
                    "description": "Planejar e executar um projeto pessoal de escalada ou montanhismo"
                }
            },
            {
                "name": "Educação e Interpretação Ambiental",
                "description": "Foco em conhecimentos ambientais e capacidade de facilitar experiências educativas na natureza",
                "age_range": "13-17 anos",
                "modules": [
                    "Fundamentos de Ecologia e Conservação",
                    "Técnicas de Interpretação Ambiental",
                    "Condução de Grupos em Trilhas Educativas",
                    "Desenvolvimento de Programas de Educação ao Ar Livre"
                ]
            }
        ],
        "career_exploration": {
            "related_careers": [
                "Guia de Ecoturismo/Aventura",
                "Instrutor de Atividades Outdoor",
                "Educador Ambiental",
                "Gestor de Parques e Áreas Protegidas",
                "Coordenador de Programas de Aventura",
                "Técnico em Segurança de Atividades de Aventura",
                "Pesquisador em Recreação ao Ar Livre",
                "Empreendedor em Turismo de Aventura"
            ],
            "day_in_life": [
                "Um guia de aventura planeja rotas, lidera grupos, gerencia riscos e compartilha conhecimentos sobre o ambiente natural",
                "Um educador ambiental desenvolve e facilita programas educativos em ambientes naturais, conectando as pessoas com a natureza",
                "Um gestor de programas outdoor organiza logística, treinamento de equipe e desenvolvimento de atividades adequadas ao público-alvo",
                "Um instrutor de escalada ensina técnicas, supervisiona práticas, avalia riscos e garante a segurança dos participantes"
            ],
            "educational_paths": [
                "Graduação em Educação Física, Turismo, Biologia ou Gestão Ambiental",
                "Certificações técnicas em diferentes modalidades de aventura",
                "Cursos de Wilderness First Responder (WFR) e segurança outdoor",
                "Formação em liderança e facilitação de grupos",
                "Especialização em temas como interpretação ambiental ou gestão de áreas naturais"
            ]
        },
        "meta": {
            "age_appropriate": True,
            "school_aligned": True,
            "prerequisite_subjects": ["Educação Física básica"],
            "cross_curricular": ["Biologia", "Geografia", "Educação Ambiental", "Primeiros Socorros", "Liderança"]
        }
    }

    # Atualizar a área com a nova subárea
    area_data["subareas"]["Atividades ao Ar Livre e Aventura"] = atividades_ar_livre_aventura_subarea
    area_ref.set(area_data)

    return area_data


def setup_learning_paths(db):
    """
    Função principal para configurar todas as áreas e subáreas de aprendizado,
    com conteúdo adequado para estudantes do ensino básico e médio.
    """
    print("Iniciando configuração das trilhas de aprendizado...")

    # Lista de áreas conforme LEARNING_TRACKS
    areas = [
        "Ciências Exatas e Aplicadas",
        "Artes e Expressão",
        "Música e Performance",
        "Esportes e Atividades Físicas",
        "Jogos e Cultura Geek",
        "Ciências Biológicas",
        "Ciências Humanas",
        "Ciências Sociais",
        "Direito e Carreiras Jurídicas",
        "Negócios e Empreendedorismo",
        "Meio Ambiente e Sustentabilidade",
        "Comunicação e Mídias",
        "Literatura e Linguagens",
        "Tecnologia e Sociedade",
        "Inovação e Criatividade",
        "Bem-estar e Desenvolvimento Pessoal"
    ]

    # Criar estrutura básica para todas as áreas
    for area_name in areas:
        area_ref = db.collection("learning_paths").document(area_name)
        area_doc = area_ref.get()

        if not area_doc.exists:
            # Criar estrutura inicial da área
            area_data = {
                "name": area_name,
                "description": get_area_description(area_name),
                "subareas": {},
                "meta": {
                    "created_date": time.strftime("%Y-%m-%d"),
                    "last_updated": time.strftime("%Y-%m-%d"),
                    "version": "1.0"
                }
            }
            area_ref.set(area_data)
            print(f"Área '{area_name}' criada com sucesso!")
        else:
            print(f"Área '{area_name}' já existe.")

    # Configurar subáreas detalhadas

    # 1. Ciências Exatas e Aplicadas
    setup_exatas_matematica_subarea(db)
    setup_exatas_programacao_subarea(db)
    setup_exatas_estatistica_subarea(db)
    setup_exatas_astronomia_subarea(db)
    setup_exatas_fisica_subarea(db)
    setup_exatas_quimica_subarea(db)
    setup_exatas_robotica_subarea(db)
    # 2. Artes
    setup_artes_danca_subarea(db)
    setup_artes_teatro_subarea(db)
    setup_artes_design_subarea(db)
    setup_artes_desenho_subarea(db)
    setup_artes_pintura_subarea(db)
    setup_artes_escrita_criativa_subarea(db)
    setup_artes_fotografia_subarea(db)
    setup_artes_cinema_audiovisual_subarea(db)
    # 3. Musica
    setup_musica_canto_vocal_subarea(db)
    setup_musica_producao_musical_subarea(db)
    setup_musica_canto_vocal_subarea(db)
    # 4. Esportes
    setup_artes_marciais_subarea(db)
    setup_esportes_aquaticos_subarea(db)
    setup_esportes_coletivos_subarea(db)
    setup_esportes_individuais_subarea(db)
    setup_treinamento_fisico_condicionamento_subarea(db)
    setup_atividades_ar_livre_aventura_subarea(db)
    print("Configuração das trilhas de aprendizado concluída!")
    return True


def get_area_description(area_name):
    """
    Retorna uma descrição apropriada para cada área, usando linguagem
    adequada para estudantes do ensino básico e médio.
    """
    descriptions = {
        "Ciências Exatas e Aplicadas":
            "Explore o mundo dos números, padrões e tecnologia! Nesta área você vai aprender matemática, "
            "física, química, programação e como aplicar esses conhecimentos para resolver problemas e criar coisas incríveis.",

        "Artes e Expressão":
            "Desperte sua criatividade e aprenda diferentes formas de expressão artística! Aqui você vai explorar "
            "desenho, pintura, fotografia, teatro, design e muitas outras maneiras de criar e se expressar.",

        "Música e Performance":
            "Descubra o universo dos sons, ritmos e melodias! Aprenda a tocar instrumentos, cantar, "
            "compor músicas, mixar, produzir e se apresentar no palco.",

        "Esportes e Atividades Físicas":
            "Movimente-se e descubra como seu corpo funciona! Experimente diferentes esportes e atividades físicas, "
            "aprenda sobre saúde, treinamento, trabalho em equipe e superação de desafios.",

        "Jogos e Cultura Geek":
            "Mergulhe no mundo dos jogos, animes, quadrinhos e cultura pop! Conheça diferentes tipos de jogos, "
            "aprenda a criar seus próprios jogos, participe de comunidades e explore o universo geek.",

        "Ciências Biológicas":
            "Explore os mistérios da vida! Descubra como funcionam os seres vivos, desde as células microscópicas "
            "até ecossistemas inteiros, e entenda como nosso corpo funciona.",

        "Ciências Humanas":
            "Viaje pelo tempo e entenda como pensamos! Explore história, filosofia, psicologia e antropologia "
            "para compreender melhor quem somos e como as sociedades se desenvolveram ao longo do tempo.",

        "Ciências Sociais":
            "Compreenda como vivemos em sociedade! Investigue temas como política, economia, direitos, "
            "desigualdades e movimentos sociais para entender melhor o mundo em que vivemos.",

        "Direito e Carreiras Jurídicas":
            "Descubra como as leis funcionam e como elas afetam nossa vida! Aprenda sobre seus direitos, "
            "como funciona a justiça e explore carreiras relacionadas ao mundo jurídico.",

        "Negócios e Empreendedorismo":
            "Transforme ideias em realidade! Aprenda como criar e gerenciar projetos, negócios e empresas, "
            "desenvolvendo habilidades de liderança, planejamento financeiro e marketing.",

        "Meio Ambiente e Sustentabilidade":
            "Ajude a proteger nosso planeta! Descubra como funciona a natureza e aprenda maneiras de conservar "
            "recursos naturais, combater as mudanças climáticas e criar um futuro mais sustentável.",

        "Comunicação e Mídias":
            "Aprenda a se expressar e compartilhar ideias! Explore o mundo do jornalismo, publicidade, redes sociais, "
            "podcasts, vídeos e outras formas de comunicar e influenciar pessoas.",

        "Literatura e Linguagens":
            "Viaje por mundos criados com palavras! Mergulhe no universo dos livros, histórias, poesias e diferentes "
            "idiomas, desenvolvendo sua capacidade de ler, escrever e se expressar melhor.",

        "Tecnologia e Sociedade":
            "Entenda como a tecnologia está transformando nossa vida! Explore o impacto das novas tecnologias "
            "na sociedade, questões éticas, inclusão digital e como usar a tecnologia de forma consciente.",

        "Inovação e Criatividade":
            "Desenvolva novas formas de pensar e resolver problemas! Aprenda técnicas para ter ideias "
            "originais, desenvolver projetos inovadores e pensar fora da caixa.",

        "Bem-estar e Desenvolvimento Pessoal":
            "Cuide de você e desenvolva habilidades para a vida! Aprenda sobre inteligência emocional, "
            "hábitos saudáveis, organização pessoal, foco e como se relacionar melhor com os outros."
    }

    return descriptions.get(area_name, f"Área de estudo sobre {area_name}.")


def adapt_for_age_group(content, age_group):
    """
    Adapta o conteúdo para diferentes faixas etárias.

    Args:
        content: O conteúdo a ser adaptado
        age_group: "ensino_fundamental_1" (6-10), "ensino_fundamental_2" (11-14), "ensino_medio" (15-17)

    Returns:
        Conteúdo adaptado
    """
    # Esta função seria usada para adaptar automaticamente conteúdos
    # específicos para diferentes faixas etárias

    # Exemplo simples:
    if age_group == "ensino_fundamental_1":
        # Simplificar bastante, usar linguagem muito acessível
        # Adicionar elementos lúdicos, personagens, etc.
        pass
    elif age_group == "ensino_fundamental_2":
        # Linguagem acessível, exemplos concretos
        # Menos infantilizado, mais desafios
        pass
    elif age_group == "ensino_medio":
        # Linguagem mais formal, conceitos mais abstratos
        # Conexões com vestibular, ENEM, mercado de trabalho
        pass

    return content

if __name__ == "__main__":
    db = get_firestore_client()
    setup_learning_paths(db)