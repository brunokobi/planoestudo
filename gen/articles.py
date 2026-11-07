# (semana, prioridade, data, título, url, por que é provável)
B = "https://news.mit.edu/2026/"
A = [
 # Semana 3 (16–22/11)
 (3,"Máxima","09/06","The consequences of relying on AI for accurate news",B+"consequences-of-relying-on-ai-for-accurate-news-0609","Estudo do Media Lab sobre o efeito da IA na cognição, no mesmo molde do texto do ChatGPT na prova 2025-2"),
 (3,"Máxima","04/08","The benefits of medical AI assistance vary based on user expertise",B+"medical-ai-assistance-benefits-vary-based-on-user-expertise-0804","LLM em diagnóstico médico, como o texto da prova 2025-2R"),
 (3,"Alta","03/06","Teaching AI agents to ask better questions by playing \"Battleship\"",B+"teaching-ai-agents-ask-better-questions-playing-battleship-0603","Estudo com método e achado claros (modelo pequeno vence modelos grandes)"),
 # Semana 4
 (4,"Máxima","30/06","Q&A: What is agentic AI today, and what do we want it to be?",B+"agentic-ai-and-what-do-we-want-it-be-0630","Formato pergunta e resposta, como o texto da prova 2024-2; tema central de 2026"),
 (4,"Alta","26/06","LLMs help robots understand vague instructions and focus on key details",B+"llms-help-robots-understand-vague-instructions-and-focus-key-details-0626","Robôs + LLM, parecido com o texto de treino de robôs da prova 2025-1"),
 (4,"Alta","13/07","AI agents create virtual playgrounds to help robots get crucial training data",B+"ai-agents-create-virtual-playgrounds-to-help-robots-get-crucial-training-data-0713","Treino de robôs em simulação, mesmo tema da prova 2025-1"),
 # Semana 5
 (5,"Alta","07/07","How novice coders can develop AI programs for military applications",B+"how-novice-coders-can-develop-ai-programs-for-military-applications-0707","Estudo com chatbots e programação, tema de computação aplicada"),
 (5,"Alta","18/08","When AI art has no author: Study finds generated images often can't be traced to training data",B+"when-ai-art-has-no-author-generated-images-often-cant-be-traced-to-training-data-0818","Estudo com achado surpreendente; rende perguntas de implicação"),
 (5,"Alta","13/07","New method aims to keep kids safe from illegal AI-generated content",B+"new-method-keeps-kids-safe-from-illegal-ai-generated-content-0713","Segurança de IA generativa; método e motivação claros"),
 # Semana 6
 (6,"Máxima","15/10","Q&A: The \"collision\" between AI, your brain, and society",B+"collision-between-ai-your-brain-and-society-eric-so-book-1015","IA e capacidade de pensar: continuação direta do tema da prova 2025-2"),
 (6,"Alta","02/09","System helps humans predict when self-driving cars will make mistakes",B+"system-helps-humans-predict-when-self-driving-cars-will-make-mistakes-0902","Explicabilidade de IA; estrutura problema → solução → teste"),
 (6,"Alta","29/09","The effects of an \"algorithmic monoculture\" depend on the details",B+"algorithmic-monoculture-effects-depend-on-details-0929","Estudo sobre algoritmos de contratação; bom para perguntas de inferência"),
 # Semana 7
 (7,"Máxima","30/10","Q&A: Hey AI, who should I vote for this year?",B+"qa-hey-ai-who-should-i-vote-for-this-year-1030","Viés de LLMs, como na prova 2025-2R; muito recente"),
 (7,"Alta","13/10","How artificial neural networks build their own learning machinery",B+"how-artificial-neural-networks-build-their-own-learning-machinery-1013","Pesquisa básica de redes neurais com analogia com o cérebro"),
 (7,"Alta","21/05","Technology usually creates jobs for young, skilled workers. Will AI do the same?",B+"technology-creates-jobs-young-skilled-workers-ai-0521","IA e trabalho; perguntas de opinião e implicação, como em 2024-2"),
 # Semana 8 (Natal: leitura leve)
 (8,"Alta","29/09","Who we become when we talk to machines",B+"when-we-talk-to-machines-sherry-turkle-book-0929","Chatbots e relações humanas; vocabulário de opinião e tom"),
 (8,"Média","17/06","Could AI tell you where you left your keys?",B+"could-ai-tell-you-where-you-left-your-keys-0617","Memória espacial de robôs; texto curto e técnico"),
 (8,"Média","24/09","Estimating suicide risk from text",B+"estimating-suicide-risk-from-text-0924","PLN em saúde; estrutura de estudo clássica"),
 # Semana 9
 (9,"Alta","22/04","Teaching AI models to say \"I'm not sure\"",B+"teaching-ai-models-to-say-im-not-sure-0422","Alucinação e confiança de LLMs (é de abril, um pouco antes da janela, mas o tema é central)"),
 (9,"Média","30/09","This game-playing AI is the new champ at Stratego",B+"game-playing-ai-stratego-new-champ-0930","IA em jogos; comparação com humanos e outros modelos"),
 (9,"Média","25/06","Improving the speed and energy-efficiency of AI agents",B+"improving-ai-agent-speed-and-energy-efficiency-0625","Eficiência de agentes de IA; vocabulário de sistemas"),
 # Semana 10
 (10,"Média","14/10","Researchers improve weather forecasts looking two to six weeks out",B+"researchers-improve-weather-forecasts-looking-two-six-weeks-out-1014","Machine learning aplicado, com resultado quantitativo"),
 (10,"Média","19/10","Why teaching AI about symmetry could make prenatal diagnosis more reliable",B+"teaching-ai-about-symmetry-could-make-prenatal-diagnosis-more-reliable-1019","IA em saúde; explicação do método com analogia"),
 (10,"Média","15/07","3 Questions: Neural transparency and the future of AI design",B+"3-questions-neural-transparency-and-future-of-ai-design-0715","Formato '3 perguntas'; transparência de IA"),
 # Semana 11
 (11,"Média","08/10","Using AI to mitigate the growing environmental threat of data centers",B+"mitigating-environmental-threat-of-data-centers-christina-delimitrou-1008","Energia e data centers, tema em alta"),
 (11,"Média","14/09","New method enables AI for safety-critical situations",B+"new-method-enables-ai-safety-critical-situations-0914","IA generativa com restrições (HardFlow)"),
 (11,"Média","23/10","Q&A: How AI came to model the \"messy\" human mind",B+"qa-how-ai-came-to-model-messy-human-mind-1023","Q&A sobre IA e mente humana"),
 # Semana 12
 (12,"Média","16/09","New AI technique could make minimally invasive surgeries safer and more precise",B+"new-ai-technique-could-make-minimally-invasive-surgeries-safer-more-precise-0916","IA em cirurgia; estrutura problema → método → resultado"),
 (12,"Média","13/10","Q&A: Building accountability behind our words — and AI's — in civic conversations",B+"qa-building-accountability-behind-our-words-and-ai-civic-conversations-1013","Ética de textos gerados por IA"),
 (12,"Média","10/08","With a feel for physics, AI models simulate a wider range of real-world scenarios",B+"ai-models-simulate-wider-range-of-real-world-scenarios-0810","IA + física; vocabulário técnico"),
 # Semana 13
 (13,"Média","05/08","Personalized physical therapy: Stroke rehabilitation powered by AI",B+"personalized-physical-therapy-stroke-rehabilitation-powered-by-ai-0805","IA em reabilitação; texto acessível"),
 (13,"Média","08/10","3 Questions: What is the best path forward for AI in academia?",B+"3-questions-best-path-forward-for-ai-academia-1008","IA na educação; perguntas de opinião"),
 (13,"Média","28/10","Making machines that can listen",B+"making-machines-that-can-listen-paris-smaragdis-1028","Perfil de pesquisador em IA de áudio"),
 # Varredura de 07/11/2026 (artigos novos, entram como extras da semana)
 (3,"Alta","05/11","Clearing up a robot’s fuzzy memory",B+"clearing-up-robot-fuzzy-memory-1105","Estudo de robôs com modelo de visão e linguagem; publicado na janela ideal"),
 (4,"Média","06/11","How to predict the behavior of molecules from scant data",B+"how-to-predict-molecule-behavior-with-scant-data-1106","Estudo de IA em química; vocabulário técnico"),
]
