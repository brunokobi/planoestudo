import sys, io, json, contextlib, datetime as dt
sys.path.insert(0, sys.argv[1])
from topics import T
from articles import A

# 1) calcular respostas dos exercícios de código
for tp in T.values():
    for e in tp["ex"]:
        if "code" in e:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(e["code"], {"__name__": "__ex__"})
            e["a"] = buf.getvalue().strip()
            e.setdefault("why", "")

D = dt.date
def d(s):  # 'dd/mm'
    dd, mm = map(int, s.split("/"))
    return D(2027 if mm <= 2 else 2026, mm, dd)

# kind: estudo | pratica | simulado | revisao | leve | livre | prova | admin
# topic: id (ex 1-4 do tema) ; extra tasks ; reserve: list of topics whose ex5 is used
S = []
def add(date, kind, title, topic=None, tasks=(), provas=None, reserve=(), edital=None, ing=None):
    S.append(dict(date=d(date), kind=kind, title=title, topic=topic, tasks=list(tasks), provas=provas, reserve=list(reserve), edital=edital, ing=ing))

ING = "Inglês (20 min): ler 1 artigo do MIT News · AI, responder as 4 perguntas-guia (objetivo, achado, limitação, próximo passo) e pôr 5 palavras novas no Anki"
# Semana 1
add("03/11","admin","Inscrição + simulado diagnóstico",tasks=["Fazer a inscrição no formulário (abre hoje) e salvar o comprovante","Às 20h: prova 2025-2R completa (provas/edital-119-2025-prova-PPComp.pdf), 30 questões em 90 min, sem consulta e sem computador","Anotar as notas N1 e N2 (não corrigir ainda)"],edital="Inscrições de 03/11 a 13/12")
add("04/11","admin","Correção do diagnóstico e montagem do sistema",tasks=["Corrigir com o gabarito (edital-119-2025-gabarito-prova.pdf)","Classificar cada erro pelo tema (Python, ED, Busca, Ordenação, Lógica) e pelo tipo (conceito, leitura, cálculo, pegadinha)","Criar o caderno de erros (caderno ou planilha)","Instalar o Anki e criar os baralhos: Lógica, Python, ED, Busca/Ordenação, Inglês"])
add("05/11","estudo","Lógica: conectivos e tabela-verdade",topic="L1")
add("06/11","estudo","Lógica: equivalências da condicional",topic="L2",tasks=["Pedir ao RH a declaração com cargo, período e descrição das atividades de computação"])
add("07/11","estudo","Lógica: negações",topic="L3",tasks=["Bloco extra (1h): copiar de memória a tabela 'conectivo → negação' e conferir"])
add("08/11","revisao","Revisão da semana + Inglês",tasks=["Escrever de memória tudo o que lembrar de L1–L3 numa folha (blurting) e conferir com a página dos temas",],reserve=["L1"],ing="Inglês (1h): prova 2022, texto 1 (Q1–10), com cronômetro de 25 min e o gabarito gabarito-prova-2022.pdf")
# Semana 2
add("09/11","estudo","Lógica: De Morgan, bicondicional e exportação",topic="L4")
add("10/11","estudo","Lógica: valor lógico a partir de premissas",topic="L5")
add("11/11","estudo","Python: operadores, precedência e and/or",topic="P1")
add("12/11","estudo","Python: strings e fatiamento",topic="P2")
add("13/11","pratica","Bateria de lógica (questões reais)",provas="2022 Q21–26 · 2025-1 Q26–30 · 2025-2 Q26–30 · 2025-2R Q27–30 (ignore as que você já fez no diagnóstico)",reserve=["L2","L3"])
add("14/11","pratica","Checkpoint L1: 20 questões de lógica",tasks=["Refazer as 20 questões de lógica das provas misturadas, cronometrando 2 min por questão","Meta: 85% de acerto. Abaixo disso, repetir L3 e L4 amanhã"],reserve=["L4","L5"],ing="Inglês (30 min): prova 2022, texto 2 (Q11–20)")
add("15/11","revisao","Revisão espaçada + Inglês",tasks=[],reserve=["P1"])
# Semana 3
add("16/11","estudo","Python: listas, range e compreensões",topic="P3")
add("17/11","estudo","Python: loops aninhados e teste de mesa",topic="P4")
add("18/11","estudo","Python: for-else, while True, break e continue",topic="P5")
add("19/11","estudo","Lógica: quantificadores (todo/algum)",topic="L6")
add("20/11","estudo","Feriado: funções, escopo e composição",topic="P6",tasks=["Bloco extra (30 min): 10 testes de mesa da Puga, cap. 3"])
add("21/11","pratica","Bateria de Python (questões reais)",provas="2025-1 Q11–15 · 2025-2 Q11, Q12, Q15, Q23 · 2025-2R Q11, Q12, Q14 · 2022 Q29–31 · 2024-2 Q19–21",reserve=["P2","P3","P4"],ing="Inglês (30 min): prova 2024-2, Q1–10")
add("22/11","estudo","Lógica: argumentos e silogismos + revisão",topic="L7",tasks=[])
# Semana 4
add("23/11","estudo","Python: mutabilidade e aliasing",topic="P7")
add("24/11","estudo","Python: recursão I (pilha de chamadas)",topic="P8")
add("25/11","estudo","Python: recursão II (listas e strings)",topic="P9")
add("26/11","estudo","Python: matrizes",topic="P10")
add("27/11","pratica","Bloco misto + preparação do checkpoint",tasks=["Recitar de memória as 6 equivalências e as 5 negações","Revisar o caderno de erros (só Python e Lógica)"],reserve=["P5","P6","L6"])
add("28/11","simulado","Checkpoint 1: prova 2025-1 completa",tasks=["Às 19h: prova 2025-1 (edital-03-2025-prova-PPComp-2025-1.pdf), 30 questões em 90 min","Corrigir com edital-03-2025-gabarito.jpg","Meta: Específicas ≥ 16/20 e Inglês ≥ 8/10","Lançar os erros no caderno"])
add("29/11","revisao","Revisão espaçada + Inglês",tasks=[],reserve=["P7","L7"])
# Semana 5
add("30/11","estudo","ED: pilha I (operações e trace)",topic="E1")
add("01/12","estudo","ED: pilha II (balanceamento e pós-fixa)",topic="E2")
add("02/12","estudo","ED: fila, fila circular e deque",topic="E3",edital="Isenção da taxa: último dia é amanhã, 03/12")
add("03/12","estudo","ED: listas encadeadas",topic="E4")
add("04/12","pratica","Recuperação ativa de estruturas lineares",tasks=["Escrever de memória as classes Pilha, Fila (com deque) e FilaCircular, e testar no Python","Escrever a função de parênteses balanceados sem consultar"],reserve=["P8","P9"])
add("05/12","pratica","Bateria de estruturas lineares (questões reais)",provas="2025-1 Q17–18 · 2025-2 Q17–18 · 2025-2R Q22 · 2024-2 Q25 · 2022 Q37, Q39, Q42, Q43",reserve=["E1","E2","P10"],ing="Inglês (30 min): 1 artigo do MIT News + 10 perguntas que você mesmo escrever")
add("06/12","revisao","Revisão espaçada + Inglês",tasks=[],reserve=["E3"])
# Semana 6
add("07/12","estudo","ED: tabela hash, dict e set",topic="E5")
add("08/12","estudo","ED: heap e fila de prioridade",topic="E6")
add("09/12","estudo","Custo das operações em Python",topic="C2")
add("10/12","pratica","'Qual estrutura é a mais adequada' (questões reais)",provas="2025-2 Q14, Q18, Q20 · 2025-2R Q18 · 2025-1 Q20, Q23",reserve=["E4","E5"])
add("11/12","pratica","Revisão intercalada: lógica + Python",tasks=["Escolher 10 questões erradas do caderno de erros e refazer sem olhar a resposta"],reserve=["L1","P4","L5"])
add("12/12","pratica","Bloco misto de 20 questões",tasks=["PAGAR A TAXA (R$ 100) E ENVIAR O COMPROVANTE, se ainda não fez: o prazo é amanhã","Montar o bloco: as 2 questões mais difíceis de cada tema estudado até aqui (pelo caderno de erros)"],reserve=["E6","C2","P1"],edital="Prazo final da taxa e da GRU: 13/12",ing="Inglês (30 min): 1 artigo do MIT News")
add("13/12","revisao","Revisão espaçada + conferir a inscrição",tasks=["Conferir se o comprovante foi enviado para ppcomp.serra@ifes.edu.br"],edital="Hoje é o último dia da inscrição e da taxa")
# Semana 7
add("14/12","estudo","Árvore binária de busca: inserção e busca",topic="E7")
add("15/12","estudo","Árvores: percursos, folhas e altura",topic="E8")
add("16/12","pratica","Árvores: código recursivo",tasks=["Implementar de memória: inserir, buscar, em_ordem, contar_folhas e altura","Desenhar 3 BSTs a partir de sequências inventadas e escrever os 3 percursos de cada"],provas="2025-1 Q19 · 2025-2 Q25 · 2025-2R Q24 · 2024-2 Q24 · 2022 Q38, Q40, Q41, Q45",reserve=["E7"])
add("17/12","admin","Dossiê do currículo (Anexo III)",tasks=["Juntar CTPS, declaração do RH, certificados de pós/IC/projetos","Montar o PDF único da documentação com páginas numeradas","Preencher a tabela do Anexo III indicando as páginas","30 min: flashcards do Anki"])
add("18/12","pratica","Revisão de árvores e de estruturas de dados",tasks=["Recitar de memória os percursos e a tabela de complexidades de estruturas"],reserve=["E8","E3"],edital="Homologação das inscrições: hoje")
add("19/12","simulado","Checkpoint 2: prova 2025-2 completa",tasks=["Às 19h: prova 2025-2 (edital-80-2025-prova.pdf), 30 questões em 90 min","Corrigir com edital-80-2025-gabarito.pdf","Meta: Específicas ≥ 17/20","Lançar os erros no caderno"])
add("20/12","admin","Fechar o currículo + revisão",tasks=["Conferir as regras: linha sem quantidade, total ou página vale zero; só ano e semestre completos","Salvar os 2 PDFs finais"])
# Semana 8 (Natal)
add("21/12","estudo","Grafos: representação",topic="G1")
add("22/12","revisao","Revisão pelo caderno de erros",tasks=["Refazer todas as questões marcadas como 'conceito' no caderno de erros"],reserve=["P8","E2"])
add("23/12","pratica","Bloco misto intercalado",tasks=["Recitar a escada de complexidades e os pares de negação"],reserve=["L3","P7","E6","G1"])
add("24/12","livre","Véspera de Natal",tasks=["Opcional: 15 min de flashcards"])
add("25/12","livre","Natal",tasks=["Descanso. Dormir bem também consolida a memória"])
add("26/12","pratica","Bloco misto + Inglês",tasks=["Escolher 20 questões das provas de 2022 e 2024 ainda não feitas"],reserve=["P9","E1","L6"],ing="Inglês (30 min): 1 artigo do MIT News")
add("27/12","leve","Revisão leve",tasks=["30 min de Anki","Ler a lista de pegadinhas da página do plano"])
# Semana 9
add("28/12","estudo","Busca em largura (BFS)",topic="G2")
add("29/12","estudo","Busca em profundidade (DFS)",topic="G3")
add("30/12","estudo","Busca sequencial e busca binária",topic="B1")
add("31/12","livre","Véspera de Ano Novo",tasks=["Opcional: 15 min de flashcards"])
add("01/01","livre","Ano Novo",tasks=["Descanso"])
add("02/01","pratica","Bateria de buscas (questões reais)",provas="2025-1 Q16, Q21–23 · 2025-2 Q21–22 · 2025-2R Q17, Q21, Q23 · 2024-2 Q23 · 2022 Q32",reserve=["G2","G3","B1"],ing="Inglês (30 min): 1 artigo do MIT News")
add("03/01","revisao","Revisão espaçada + Inglês",tasks=[])
# Semana 10
add("04/01","estudo","Ordenação: bubble sort",topic="O1")
add("05/01","estudo","Ordenação: selection sort",topic="O2")
add("06/01","estudo","Ordenação: insertion sort",topic="O3")
add("07/01","pratica","Identificar o algoritmo e a estabilidade",tasks=["Escrever os 3 sorts de memória e testar no Python","Para cada sort, simular 2 listas inventadas, passada a passada"],reserve=["O1","O2"])
add("08/01","pratica","Recuperação ativa e caderno de erros",tasks=["Refazer as questões erradas de Python e ED"],reserve=["O3","G1"])
add("09/01","pratica","Bateria de ordenação (questões reais)",provas="2025-1 Q24–25 · 2025-2 Q16, Q19 · 2025-2R Q16, Q19, Q20 · 2024-2 Q22 · 2022 Q33–36",ing="Inglês (30 min): 1 artigo do MIT News")
add("10/01","revisao","Revisão espaçada + Inglês",tasks=[])
# Semana 11
add("11/01","estudo","Ordenação: merge sort",topic="O4")
add("12/01","estudo","Ordenação: quicksort",topic="O5")
add("13/01","estudo","Heapsort, counting sort e estabilidade",topic="O6")
add("14/01","estudo","Notação assintótica e complexidade de código",topic="C1")
add("15/01","pratica","Tabela-mãe de complexidades",tasks=["Escrever de memória a tabela algoritmo | melhor | médio | pior | estável | in-place","Conferir e repetir até sair perfeita 2 vezes seguidas"],reserve=["O4","O5","O6","C1"])
add("16/01","simulado","Checkpoint 3: Simulado A (30 questões de Específicas)",tasks=["19h: Simulado A na aba Simulados, 30 questões em 1h30, no papel","Corrigir na própria aba (1h): ler a explicação de cada erro","Lançar os erros no caderno com o tipo (conceito, leitura, cálculo ou pegadinha)","Meta: 22/30"],ing="Inglês (1h): prova 2025-2R, questões 1 a 10, refeita com cronômetro de 25 min, e correção")
add("17/01","simulado","Simulado B (40 questões)",tasks=["Simulado B na aba Simulados: 10 de Inglês + 30 de Específicas em 2h30 (o Inglês do dia está dentro do simulado)","Ensaiar a ordem: Inglês → Lógica → conceituais → teste de mesa","Corrigir (1h30) e lançar os erros"],ing="Inglês: incluído no Simulado B (texto + 10 questões)")
# Semana 12
add("18/01","pratica","Correção profunda dos simulados A e B",tasks=["Refazer no papel todas as questões erradas dos simulados A e B, sem olhar a explicação","Listar os 3 subtemas mais fracos"])
add("19/01","pratica","Reforço do subtema mais fraco (1)",tasks=["Abrir o tema na aba Temas e refazer os 5 exercícios","Refazer as questões das provas antigas desse tema"])
add("20/01","pratica","Reforço do subtema mais fraco (2)",tasks=["Mesmo roteiro para o 2º subtema mais fraco"])
add("21/01","pratica","Ensaio no horário da prova (quinta, 19h)",tasks=["Às 19h: 20 questões de reserva da aba Temas (exercício 5 de cada tema), misturadas, em 1h","Corrigir e lançar os erros"])
add("22/01","pratica","Reforço do subtema mais fraco (3)",tasks=["Mesmo roteiro para o 3º subtema mais fraco","Recitar a tabela-mãe de complexidades"])
add("23/01","simulado","Simulado C (40 questões)",tasks=["Simulado C na aba Simulados: 40 questões em 2h30","Corrigir (1h30) e lançar os erros","Meta da semana: Específicas ≥ 24/30 em 2 de 3 simulados"],ing="Inglês: incluído no Simulado C (texto + 10 questões)")
add("24/01","simulado","Simulado D (40 questões)",tasks=["Simulado D na aba Simulados: 40 questões em 2h30","Corrigir (1h30) e lançar os erros"],ing="Inglês: incluído no Simulado D (texto + 10 questões)")
# Semana 13
add("25/01","revisao","Caderno de erros: lógica",tasks=["Refazer só as questões de lógica que você já errou","Recitar o palácio da memória das equivalências"])
add("26/01","revisao","Caderno de erros: Python",tasks=["Refazer só as questões de Python que você já errou","Ler a lista de pegadinhas (aba Análise da prova)"])
add("27/01","revisao","Caderno de erros: ED, busca e ordenação",tasks=["Refazer só as questões dessas áreas que você já errou","Recitar a tabela-mãe de complexidades"])
add("28/01","pratica","Ensaio final no horário da prova (quinta, 19h)",tasks=["Às 19h: refazer as 20 questões mais difíceis dos simulados A a D, em 1h","Corrigir; se algum erro repetiu, criar um flashcard novo dele"])
add("29/01","pratica","Refazer as questões de 2025 que você já errou",tasks=["Só as questões das 3 provas de 2025 que você errou alguma vez","Conferir os 2 PDFs do currículo"])
add("30/01","simulado","Simulado final E (40 questões)",tasks=["Simulado E na aba Simulados: 40 questões em 2h30, nas condições reais (papel, caneta, sem celular)","Corrigir (1h30) e lançar os erros"],ing="Inglês: incluído no Simulado E (texto + 10 questões)")
add("31/01","leve","Revisão leve",tasks=["30 min de Anki","Ler o caderno de erros","Nada de conteúdo novo"])
# Reta final
add("01/02","leve","Tabelas finais",tasks=["Ler as tabelas: equivalências, negações, complexidades, pegadinhas Python","Dormir cedo"])
add("02/02","admin","Conferir local e horário da prova",tasks=["Ver em ifes.edu.br/processosseletivos/alunos o local e o horário","Planejar o trajeto até a Av. dos Sabiás, 330, saindo com folga para chegar 1h antes","20 min de Anki"],edital="Divulgação do local e do horário: hoje")
add("03/02","leve","Véspera: descanso ativo",tasks=["No máximo 30 min: só os flashcards marcados como difíceis","Separar documento com foto e 2 canetas pretas ou azul-escuras","Dormir cedo"])
add("04/02","prova","DIA DA PROVA (à noite)",tasks=["Chegar 1h antes, com documento e caneta","Celular desligado antes de entrar na sala","Ordem: Inglês → Lógica → conceituais → teste de mesa; 20 min finais para o cartão-resposta"])
add("05/02","admin","Enviar o currículo",tasks=["Enviar os 2 PDFs pelo formulário https://forms.gle/2pNvxiJKLLTH4SHW8 e salvar o comprovante"],edital="Entrega da análise curricular: hoje")

# 2) revisões espaçadas
dates = [s["date"] for s in S]
byd = {s["date"]: s for s in S}
blocked = {"livre", "prova", "simulado"}
rev = {s["date"]: [] for s in S}
for s in S:
    if s["kind"] == "estudo" and s["topic"]:
        for k in (1, 3, 7, 14, 30):
            x = s["date"] + dt.timedelta(k)
            while x in byd and (byd[x]["kind"] in blocked or len(rev[x]) >= 3):
                x += dt.timedelta(1)
            if x in byd and x <= D(2027, 2, 3):
                rev[x].append(dict(topic=s["topic"], k=k))
WD = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
DUR = {"livre": "livre", "prova": "prova", "leve": "30–45 min"}
out = []
for s in S:
    w = s["date"].weekday()
    dur = DUR.get(s["kind"]) or ("4h · 3h de Específicas + 1h de Inglês" if w >= 5 else "2h · 1h40 de Específicas + 20 min de Inglês")
    ing = s["ing"]
    if ing and ing.startswith("Inglês: incluído"): dur = "4h · simulado com Inglês (2h30) + correção (1h30)"
    if s["kind"] not in ("livre", "prova", "leve"):
        wk = (s["date"] - D(2026, 11, 2)).days // 7 + 1
        if ing and not ing.startswith("Inglês:"):
            ing = ing.split(":", 1)[1].strip() if ing.startswith("Inglês (") else ing
            ing = ("Inglês (1h): " if w >= 5 else "Inglês (20 min): ") + ing
        elif not ing:
            if w >= 5:
                ing = ("Inglês (1h): reler os 3 artigos da semana pelo seu resumo, escrever 3 questões no estilo da banca e passar o Anki de vocabulário" if wk >= 3
                       else "Inglês (1h): estudar as abas Tipos de pergunta e Método da página de Inglês e passar 2 grupos da aba Vocabulário para o Anki")
            else:
                if wk >= 3 and wk <= 13:
                    ing = ["Inglês (20 min): Anki de vocabulário + 1 grupo da aba Vocabulário",
                           "Inglês (20 min): ler o artigo 1 da semana respondendo goal / finding / limitation / next step",
                           "Inglês (20 min): terminar o artigo 1 e passar 5 palavras dele para o Anki",
                           "Inglês (20 min): ler o artigo 2 da semana com as mesmas 4 perguntas",
                           "Inglês (20 min): ler o artigo 3 da semana com as mesmas 4 perguntas"][w]
                else:
                    ing = ["Inglês (20 min): Anki de vocabulário + 1 grupo da aba Vocabulário",
                           "Inglês (20 min): aba Tipos de pergunta: ler e decorar como atacar cada tipo",
                           "Inglês (20 min): aba Método: ensaiar o passo a passo de 25 min",
                           "Inglês (20 min): aba Vocabulário: conectores e falsos cognatos",
                           "Inglês (20 min): ler 1 artigo da lista de artigos prováveis"][w]
    out.append(dict(id=s["date"].isoformat(), wd=WD[w], dm=s["date"].strftime("%d/%m"), kind=s["kind"], title=s["title"], topic=s["topic"],
                    tasks=s["tasks"], provas=s["provas"], reserve=s["reserve"], edital=s["edital"], ing=ing, rev=rev[s["date"]], dur=dur, wk=(s["date"]-D(2026,11,2)).days//7+1))
arts=[dict(wk=a[0],pri=a[1],dt=a[2],title=a[3],url=a[4],why=a[5],id='art:'+a[4].rstrip('/').split('/')[-1]) for a in A]
json.dump(dict(topics=T, days=out, arts=arts), open(sys.argv[2], "w"), ensure_ascii=False)
print(len(out), "dias;", sum(len(t["ex"]) for t in T.values()), "exercícios")
missing = [s["date"] for s in S]
allx = [D(2026, 11, 3) + dt.timedelta(i) for i in range((D(2027, 2, 5) - D(2026, 11, 3)).days + 1)]
print("faltando:", [x for x in allx if x not in byd], "duplicados:", len(dates) - len(set(dates)))
used = {s["topic"] for s in S if s["topic"]}
print("temas não agendados:", set(T) - used)
