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

    # 2. Adicionar outras subáreas detalhadas aqui
    # setup_artes_desenho_subarea(db)
    # setup_musica_instrumental_subarea(db)
    # Etc.

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