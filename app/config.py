import os

# Variáveis de ambiente
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# Modelo Zero-Shot e configuração do pipeline
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

# CANDIDATE_LABELS com novos labels adicionados e organizados
CANDIDATE_LABELS = [
    # Ciências Exatas e Aplicadas
    "matemática", "estatística", "física", "química",
    "programação", "robótica", "cibersegurança", "inteligência artificial",
    "big data", "desenvolvimento de software", "desenvolvimento de jogos",
    "engenharia civil", "engenharia mecânica", "engenharia ambiental",
    "circuitos elétricos", "energia solar", "energia eólica", "algoritmos",
    "banco de dados", "computação em nuvem", "internet das coisas", "automação",

    # Artes e Expressão
    "desenho", "pintura", "arte digital", "design gráfico",
    "fotografia", "cinema", "teatro", "dança",
    "escultura", "grafite", "artesanato", "animação 3D",
    "customização de roupas", "design de moda", "quadrinhos", "arquitetura",
    "cerâmica", "história da arte", "curadoria", "performance art",

    # Música e Performance
    "violão", "guitarra", "bateria", "teclado", "canto",
    "produção musical", "música eletrônica", "DJing",
    "composição musical", "arranjo", "hip hop", "k-pop",
    "performance ao vivo", "banda", "microfone", "teoria musical",
    "técnica vocal", "home studio", "mixagem", "masterização",

    # Esportes e Atividades Físicas
    "futebol", "vôlei", "basquete", "natação", "corrida",
    "ciclismo", "ginástica artística", "judô", "boxe",
    "musculação", "crossfit", "yoga", "dança fitness",
    "skate", "artes marciais", "nutrição esportiva",
    "treinamento funcional", "fisioterapia", "suplementação", "tênis",

    # Jogos e Cultura Geek
    "RPG", "FPS", "jogos de luta", "jogos de estratégia",
    "jogos de aventura", "consoles retrô", "League of Legends",
    "Fortnite", "desenvolvimento de jogos 2D", "anime",
    "mangá", "cosplay", "cultura pop", "filmes de ficção científica",
    "comunidades de jogos", "design de jogos", "roteiro para jogos",
    "arte para jogos", "jogos de tabuleiro", "game jam", "emulação",
    "speedrunning", "crítica de jogos", "jogos independentes",
    "história dos videogames", "comunidade gamer", "monetização de jogos",
    "realidade virtual", "realidade aumentada", "e-sports",

    # Ciências Biológicas
    "biologia celular", "anatomia", "fisiologia",
    "genética", "ecologia", "zoologia", "botânica",
    "microbiologia", "imunologia", "neurociência",
    "biotecnologia", "meio ambiente", "evolução",
    "laboratório", "biodiversidade", "biologia molecular",
    "bioquímica", "histologia", "farmacologia", "embriologia",

    # Ciências Humanas
    "filosofia", "história", "psicologia", "antropologia",
    "sociologia", "arte", "literatura", "cinema",
    "linguística", "direitos humanos", "movimentos sociais",
    "feminismo", "racismo", "religião", "política", "ética",
    "epistemologia", "existencialismo", "história antiga",
    "história contemporânea", "arqueologia",

    # Ciências Sociais
    "sociologia", "movimentos sociais", "racismo",
    "identidade de gênero", "economia", "urbanismo",
    "desigualdade social", "criminologia", "justiça criminal",
    "criminalidade urbana", "política", "globalização",
    "direitos civis", "ativismo", "eleições", "geopolítica",
    "relações internacionais", "políticas públicas", "análise de dados sociais",
    "estudos culturais", "ciência política",

    # Direito e Carreiras Jurídicas
    "direito penal", "direito civil", "direito constitucional",
    "direito do trabalho", "criminologia", "justiça criminal",
    "mediação e arbitragem", "direitos humanos", "advocacia",
    "legislação", "tribunal", "juiz", "concursos públicos",
    "promotor", "delegacia", "debater", "crime", "investigação",
    "direito digital", "direito ambiental", "direito tributário",

    # Negócios e Empreendedorismo
    "administração", "finanças", "marketing", "publicidade",
    "empreendedorismo", "startup", "e-commerce",
    "inovação em negócios", "responsabilidade social",
    "networking", "gestão de pessoas", "liderança",
    "planejamento financeiro", "negociação", "pitch",
    "análise de mercado", "gestão de projetos", "economia",
    "empreendedorismo social", "transformação digital",

    # Meio Ambiente e Sustentabilidade
    "ecologia", "mudanças climáticas", "energias renováveis",
    "consumo consciente", "reciclagem", "desenvolvimento sustentável",
    "biodiversidade", "economia circular", "reflorestamento",
    "poluição", "água potável", "agricultura orgânica",
    "lixo zero", "descarbonização", "proteção ambiental",
    "preservação ambiental", "recursos hídricos", "fauna e flora",
    "impacto ambiental", "sustentabilidade empresarial", "economia verde",
    "ecoturismo", "gestão de resíduos", "permacultura", "bioconstrução",
    "conservação marinha", "educação ambiental", "política ambiental",
    "restauração ecológica", "justiça ambiental",

    # Comunicação e Mídias
    "jornalismo", "reportagem", "podcasts", "mídias sociais",
    "marketing digital", "relações públicas", "publicidade",
    "storytelling", "edição de vídeo", "debate",
    "desinformação", "oratória", "comunicação interpessoal",
    "memes", "streaming", "comunicação digital", "análise de mídia",
    "criação de conteúdo", "estratégia de comunicação",
    "gerenciamento de redes sociais", "redação publicitária",
    "documentário", "fotojornalismo", "comunicação corporativa",
    "assessoria de imprensa", "produção editorial", "crítica de mídia",
    "cultura digital", "ética na comunicação", "influenciadores digitais",

    # Literatura e Linguagens
    "literatura", "romance", "conto", "poesia", "gramática",
    "escrita criativa", "tradução", "inglês", "espanhol",
    "fanfiction", "narrativa", "análise de texto",
    "leitura crítica", "interpretação de textos", "publicação de livros",
    "teoria literária", "escrita de roteiros", "copywriting",
    "edição de textos", "mundo editorial", "crítica literária",
    "literatura contemporânea", "literatura clássica", "biografias",
    "ensaios", "literatura técnica", "criação de personagens",

    # Tecnologia e Sociedade
    "ética na tecnologia", "impacto social da IA", "inclusão digital",
    "acessibilidade tecnológica", "privacidade de dados", "divulgação científica",
    "cibercultura", "tecnologias assistivas", "democracia digital",
    "letramento digital", "tecnologia e educação", "história da tecnologia",
    "tecnopolítica", "movimento maker", "futurismo",

    # Inovação e Criatividade
    "design thinking", "resolução criativa de problemas", "inovação social",
    "prototipagem", "pensamento visual", "improvisação", "brainstorming",
    "criação colaborativa", "técnicas de ideação", "processos criativos",
    "estratégias de inovação", "criatividade aplicada", "propriedade intelectual",
    "gestão da inovação", "tendências em inovação",

    # Bem-estar e Desenvolvimento Pessoal
    "mindfulness", "produtividade pessoal", "comunicação não-violenta",
    "inteligência emocional", "gestão de estresse", "aprendizado contínuo",
    "hábitos saudáveis", "resolução de conflitos", "organização pessoal",
    "técnicas de concentração", "foco e produtividade", "meditação",
    "psicologia positiva", "técnicas de estudo", "liderança pessoal",

    # Outros
    "karl marx"  # Mantido como estava no original
]

# Atualização direta do dicionário LEARNING_TRACKS
LEARNING_TRACKS = {
    "Ciências Exatas e Aplicadas": [
        "matemática", "estatística", "física", "química",
        "programação", "robótica", "cibersegurança", "inteligência artificial",
        "big data", "desenvolvimento de software", "desenvolvimento de jogos",
        "engenharia civil", "engenharia mecânica", "engenharia ambiental",
        "circuitos elétricos", "energia solar", "energia eólica",
        # Novos labels
        "algoritmos", "banco de dados", "computação em nuvem",
        "internet das coisas", "automação"
    ],

    "Artes e Expressão": [
        "desenho", "pintura", "arte digital", "design gráfico",
        "fotografia", "cinema", "teatro", "dança",
        "escultura", "grafite", "artesanato", "animação 3D",
        "customização de roupas", "design de moda", "quadrinhos",
        # Novos labels
        "arquitetura", "cerâmica", "história da arte", "curadoria", "performance art"
    ],

    "Música e Performance": [
        "violão", "guitarra", "bateria", "teclado", "canto",
        "produção musical", "música eletrônica", "DJing",
        "composição musical", "arranjo", "hip hop", "k-pop",
        "performance ao vivo", "banda", "microfone",
        # Novos labels
        "teoria musical", "técnica vocal", "home studio", "mixagem", "masterização"
    ],

    "Esportes e Atividades Físicas": [
        "futebol", "vôlei", "basquete", "natação", "corrida",
        "ciclismo", "ginástica artística", "judô", "boxe",
        "musculação", "crossfit", "yoga", "dança fitness",
        "skate", "artes marciais",
        # Novos labels
        "nutrição esportiva", "treinamento funcional", "fisioterapia",
        "suplementação", "tênis"
    ],

    "Jogos e Cultura Geek": [
        "RPG", "FPS", "jogos de luta", "jogos de estratégia",
        "jogos de aventura", "consoles retrô", "League of Legends",
        "Fortnite", "desenvolvimento de jogos 2D", "anime",
        "mangá", "cosplay", "cultura pop", "filmes de ficção científica",
        "comunidades de jogos",
        # Novos labels
        "design de jogos", "roteiro para jogos", "arte para jogos",
        "jogos de tabuleiro", "game jam", "emulação", "speedrunning",
        "crítica de jogos", "jogos independentes", "história dos videogames",
        "comunidade gamer", "monetização de jogos", "realidade virtual",
        "realidade aumentada", "e-sports"
    ],

    "Ciências Biológicas": [
        "biologia celular", "anatomia", "fisiologia",
        "genética", "ecologia", "zoologia", "botânica",
        "microbiologia", "imunologia", "neurociência",
        "biotecnologia", "meio ambiente", "evolução",
        "laboratório", "biodiversidade",
        # Novos labels
        "biologia molecular", "bioquímica", "histologia",
        "farmacologia", "embriologia"
    ],

    "Ciências Humanas": [
        "filosofia", "história", "psicologia", "antropologia",
        "sociologia", "arte", "literatura", "cinema",
        "linguística", "direitos humanos", "movimentos sociais",
        "feminismo", "racismo", "religião", "política",
        # Novos labels
        "ética", "epistemologia", "existencialismo", "história antiga",
        "história contemporânea", "arqueologia"
    ],

    "Ciências Sociais": [
        "sociologia", "movimentos sociais", "racismo",
        "identidade de gênero", "economia", "urbanismo",
        "desigualdade social", "criminologia", "justiça criminal",
        "criminalidade urbana", "política", "globalização",
        "direitos civis", "ativismo", "eleições",
        # Novos labels
        "geopolítica", "relações internacionais", "políticas públicas",
        "análise de dados sociais", "estudos culturais", "ciência política"
    ],

    "Direito e Carreiras Jurídicas": [
        "direito penal", "direito civil", "direito constitucional",
        "direito do trabalho", "criminologia", "justiça criminal",
        "mediação e arbitragem", "direitos humanos", "advocacia",
        "legislação", "tribunal", "juiz", "concursos públicos",
        "promotor", "delegacia", "debater", "crime", "investigação",
        # Novos labels
        "direito digital", "direito ambiental", "direito tributário"
    ],

    "Negócios e Empreendedorismo": [
        "administração", "finanças", "marketing", "publicidade",
        "empreendedorismo", "startup", "e-commerce",
        "inovação em negócios", "responsabilidade social",
        "networking", "gestão de pessoas", "liderança",
        "planejamento financeiro", "negociação", "pitch",
        # Novos labels
        "análise de mercado", "gestão de projetos", "economia",
        "empreendedorismo social", "transformação digital"
    ],

    "Meio Ambiente e Sustentabilidade": [
        "ecologia", "mudanças climáticas", "energias renováveis",
        "consumo consciente", "reciclagem", "desenvolvimento sustentável",
        "biodiversidade", "economia circular", "reflorestamento",
        "poluição", "água potável", "agricultura orgânica",
        "lixo zero", "descarbonização", "proteção ambiental",
        # Novos labels
        "preservação ambiental", "recursos hídricos", "fauna e flora",
        "impacto ambiental", "sustentabilidade empresarial", "economia verde",
        "ecoturismo", "gestão de resíduos", "permacultura", "bioconstrução",
        "conservação marinha", "educação ambiental", "política ambiental",
        "restauração ecológica", "justiça ambiental"
    ],

    "Comunicação e Mídias": [
        "jornalismo", "reportagem", "podcasts", "mídias sociais",
        "marketing digital", "relações públicas", "publicidade",
        "storytelling", "edição de vídeo", "debate",
        "desinformação", "oratória", "comunicação interpessoal",
        "memes", "streaming",
        # Novos labels
        "comunicação digital", "análise de mídia", "criação de conteúdo",
        "estratégia de comunicação", "gerenciamento de redes sociais",
        "redação publicitária", "documentário", "fotojornalismo",
        "comunicação corporativa", "assessoria de imprensa",
        "produção editorial", "crítica de mídia", "cultura digital",
        "ética na comunicação", "influenciadores digitais"
    ],

    "Literatura e Linguagens": [
        "literatura", "romance", "conto", "poesia", "gramática",
        "escrita criativa", "tradução", "inglês", "espanhol",
        "fanfiction", "narrativa", "análise de texto",
        "leitura crítica", "interpretação de textos", "publicação de livros",
        # Novos labels
        "teoria literária", "escrita de roteiros", "copywriting",
        "edição de textos", "mundo editorial", "crítica literária",
        "literatura contemporânea", "literatura clássica", "biografias",
        "ensaios", "literatura técnica", "criação de personagens"
    ],

    # Novas trilhas
    "Tecnologia e Sociedade": [
        "ética na tecnologia", "impacto social da IA", "inclusão digital",
        "acessibilidade tecnológica", "privacidade de dados", "divulgação científica",
        "cibercultura", "tecnologias assistivas", "democracia digital",
        "letramento digital", "tecnologia e educação", "história da tecnologia",
        "tecnopolítica", "movimento maker", "futurismo"
    ],

    "Inovação e Criatividade": [
        "design thinking", "resolução criativa de problemas", "inovação social",
        "prototipagem", "pensamento visual", "improvisação", "brainstorming",
        "criação colaborativa", "técnicas de ideação", "processos criativos",
        "estratégias de inovação", "criatividade aplicada", "propriedade intelectual",
        "gestão da inovação", "tendências em inovação"
    ],

    "Bem-estar e Desenvolvimento Pessoal": [
        "mindfulness", "produtividade pessoal", "comunicação não-violenta",
        "inteligência emocional", "gestão de estresse", "aprendizado contínuo",
        "hábitos saudáveis", "resolução de conflitos", "organização pessoal",
        "técnicas de concentração", "foco e produtividade", "meditação",
        "psicologia positiva", "técnicas de estudo", "liderança pessoal"
    ]
}

# Valor mínimo para considerar a pontuação do Zero-Shot
MIN_SCORE = 0.10