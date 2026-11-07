# Gera o baralho do Anki (agenda/ppcomp-2027.apkg) a partir do mesmo conteúdo do site.
# Uso: <python com genanki> gen/anki.py
import html, json, os, re, subprocess, sys
import genanki

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "gen")
sys.path.insert(0, G)
T = json.load(open(os.path.join(G, "data.json")))["topics"]  # já com as respostas dos exercícios de código

# IDs fixos: reimportar atualiza os cartões em vez de duplicar
MODEL_ID, DECK_BASE = 1607392319, 2059400110

CSS = """.card{font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:20px;text-align:left;color:#18213a;background:#fff;line-height:1.45;padding:8px}
.nightMode.card,.night_mode .card{color:#e6eaf5;background:#161d30}
.tag{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#5a6580}
.word{font-size:30px;font-weight:700}
.ex{font-style:italic;color:#5a6580;font-size:17px}
.why{font-size:16px;color:#5a6580}
pre{font-family:Consolas,Menlo,monospace;font-size:16px;background:rgba(127,127,127,.12);padding:10px;border-radius:8px;white-space:pre-wrap}
hr{border:0;border-top:1px solid rgba(127,127,127,.3)}"""

MODEL = genanki.Model(
    MODEL_ID, "PPComp 2027 · Básico",
    fields=[{"name": "Frente"}, {"name": "Verso"}, {"name": "Extra"}, {"name": "Origem"}],
    templates=[{"name": "Cartão",
                "qfmt": '<div class="tag">{{Origem}}</div>{{Frente}}',
                "afmt": '{{FrontSide}}<hr id="answer">{{Verso}}{{#Extra}}<p class="why">{{Extra}}</p>{{/Extra}}'}],
    css=CSS)


def esc(s):
    return html.escape(str(s))


def code_or_text(s):
    s = str(s)
    return "<pre>" + esc(s) + "</pre>" if "\n" in s else esc(s)


def note(deck, front, back, extra, origin, tags, guid_key):
    deck.add_note(genanki.Note(model=MODEL, fields=[front, back, extra, esc(origin)],
                               tags=[re.sub(r"\s+", "_", t) for t in tags], guid=genanki.guid_for(guid_key)))


# --- vocabulário da página de Inglês (lido do app.js, a mesma fonte do site)
EN = json.loads(subprocess.check_output(["node", "-e", r"""
const s=require('fs').readFileSync(process.argv[1],'utf8'); const i=s.indexOf('var EN = {'); let d=0,j=i+9;
for(;j<s.length;j++){ if(s[j]=='{')d++; else if(s[j]=='}'){ d--; if(d==0) break; } }
process.stdout.write(JSON.stringify(eval('('+s.slice(i+9,j+1)+')').vocab));""", os.path.join(G, "app.js")]))

# --- palavras difíceis dos artigos com questões prováveis (frase do próprio texto)
ART_WORDS = [
    ("Medical AI assistance", [
        ("deference", "submissão, acatar sem questionar", "...it was largely due to deference to the AI system."),
        ("explainability", "explicabilidade (dizer por que o modelo decidiu)", "AI explainability methods had different impacts depending on the users' knowledge level."),
        ("automation bias", "viés de automação (confiar demais na máquina)", "both AI and explainability methods can engage automation bias in humans"),
        ("to be led astray", "ser desviado, induzido ao erro", "those with the least medical knowledge are most likely to be led astray"),
        ("overreliance", "dependência excessiva", "explainability methods that encourage critical thinking rather than overreliance on the model"),
        ("liability", "risco, passivo, ponto fraco", "an asset for one user and a liability for another"),
        ("to underscore", "ressaltar, enfatizar", "These results underscore the importance of building AI systems with users in mind"),
    ]),
    ("AI for accurate news", [
        ("to give (someone) pause", "fazer alguém hesitar, refletir", "A new open-access study from the MIT Media Lab should give some of those users pause"),
        ("misinformation", "informação falsa ou enganosa", "got worse at detecting misinformation on their own"),
        ("deskilling", "perda de habilidade por desuso", "broader tech trends around so-called \"deskilling\""),
        ("cognitive offloading", "transferir o esforço mental para uma ferramenta", "\"deskilling\" (or \"cognitive offloading\")"),
        ("wrinkle", "complicação, detalhe novo", "a new wrinkle emerged when the AI was no longer present"),
        ("crutch", "muleta", "whether its impact will be \"as a coach, versus as a crutch.\""),
        ("probing", "sondagem, investigação com perguntas", "so-called \"deep probing\""),
        ("to discern", "discernir, distinguir", "engaging someone to actually learn how to discern the truth on their own"),
    ]),
    ("Algorithmic monoculture", [
        ("resume screening", "triagem de currículos", "resume screening algorithms are often used in hiring"),
        ("pitfalls", "armadilhas, riscos", "to systematically assess the promises and pitfalls of algorithmic monoculture"),
        ("bargaining power", "poder de negociação", "algorithmic monoculture could improve bargaining power of job candidates"),
        ("to game the system", "burlar o sistema", "monoculture could enable individuals to game the system"),
        ("ensemble", "conjunto, combinação de vários modelos", "bundling various hiring algorithms into a single \"ensemble\""),
        ("to mitigate", "atenuar, reduzir", "This problem could be mitigated by building randomness into a monocultural platform"),
        ("feasible", "viável", "it remains to be explored how feasible this kind of algorithmic \"ensembling\" would be"),
    ]),
    ("AI art has no author", [
        ("attribution", "atribuição (de autoria, de crédito)", "a phenomenon they call attribution decay"),
        ("counterintuitive", "contraintuitivo", "It feels counterintuitive, but at sufficiently large scales..."),
        ("prohibitive", "proibitivo (caro ou difícil demais)", "the math quickly becomes prohibitive"),
        ("counterfactual", "contrafactual (o que teria acontecido se...)", "What's left is a true counterfactual model, not an estimate of one."),
        ("loophole", "brecha (na lei ou regra)", "an obligation for the industry, rather than a loophole"),
        ("derivative work", "obra derivada", "whether model outputs are derivative works"),
        ("fair use", "uso legítimo (exceção de direitos autorais)", "that raises questions about fair use"),
    ]),
    ("Self-driving cars mistakes", [
        ("black-box model", "modelo caixa-preta (funcionamento interno opaco)", "The planners are usually black-box models"),
        ("phantom braking", "frenagem fantasma (sem motivo aparente)", "an unexpected decision, like phantom braking"),
        ("faithful", "fiel (que reflete a causa real)", "concepts that faithfully describe the autonomous vehicle's decisions"),
        ("to troubleshoot", "diagnosticar e corrigir problemas", "feedback for engineers as they troubleshoot in-vehicle artificial intelligence systems"),
        ("situational awareness", "consciência da situação", "improve their situational awareness"),
        ("high-stakes", "de alto risco, em que muito está em jogo", "Especially in high-stakes settings like self-driving cars"),
    ]),
    ("The collision (Eric So)", [
        ("atrophy", "atrofia", "heavy use of AI can lead to a kind of cognitive atrophy"),
        ("sycophantic", "bajulador", "these models are simultaneously sycophantic"),
        ("allure", "atração, encanto", "how the allure of AI takes hold"),
        ("to outsource", "terceirizar", "students are outsourcing their thinking to AI"),
        ("self-fulfilling prophecy", "profecia autorrealizável", "it becomes a self-fulfilling prophecy"),
        ("friction", "atrito, esforço", "AI removes a lot of the friction necessary to build foundational mastery"),
        ("to wrestle with", "lutar com, se esforçar para entender", "our ability to learn gets dramatically better when we wrestle with material"),
    ]),
    ("Robot fuzzy memory", [
        ("mislabeled", "rotulado errado", "corrects the descriptions of mislabeled objects"),
        ("uncertainty quantification", "medição da incerteza", "UQ-DAAAM integrates uncertainty quantification into the DAAAM framework"),
        ("threshold", "limiar, limite", "If that number exceeds a certain threshold, the uncertainty is too high"),
        ("heuristic", "heurística, regra prática simples", "It does this using a heuristic, or simple rule"),
        ("vantage point", "ponto de observação, ângulo", "captions of images that describe the same object from different vantage points"),
        ("to fuse", "fundir, combinar", "the system uses an LLM to fuse them into a single object description"),
        ("downstream", "nas etapas seguintes", "which could impact downstream applications"),
    ]),
]

decks = {}
def deck(name):
    if name not in decks:
        decks[name] = genanki.Deck(DECK_BASE + len(decks), name)
    return decks[name]

n_vocab = n_art = n_ex = n_memo = 0
for group, words in EN:
    d = deck("PPComp 2027::1 Inglês::1 Vocabulário")
    for w in words:
        note(d, '<div class="word">' + esc(w[0]) + "</div>", esc(w[1]), "", "Inglês · " + group,
             ["ingles", "vocab", group], "vocab:" + w[0])
        n_vocab += 1
for art, words in ART_WORDS:
    d = deck("PPComp 2027::1 Inglês::2 Artigos prováveis")
    for w, pt, ex in words:
        note(d, '<div class="word">' + esc(w) + '</div><p class="ex">' + esc(ex) + "</p>", esc(pt), "", "Artigo · " + art,
             ["ingles", "artigo", art], "art:" + w)
        n_art += 1

ORDER = ["Python", "Estruturas de Dados", "Busca", "Ordenação", "Lógica"]
for tid, tp in T.items():
    b = tp["bloco"]; num = ORDER.index(b) + 1 if b in ORDER else 9
    d = deck("PPComp 2027::2 Específicas::%d %s" % (num, b))
    for j, e in enumerate(tp["ex"]):
        front = esc(e["q"]) + ("<pre>" + esc(e["code"]) + "</pre>" if e.get("code") else "")
        note(d, front, code_or_text(e["a"]), esc(e.get("why", "")), tid + " · " + tp["titulo"],
             ["especificas", b, tid], "ex:%s:%d" % (tid, j))
        n_ex += 1
    if tp.get("memo"):
        note(d, "Qual é o gancho de memória de <b>" + esc(tp["titulo"]) + "</b>?",
             "<ul>" + "".join("<li>" + esc(m) + "</li>" for m in tp["memo"]) + "</ul>",
             "Leitura: " + esc(tp.get("leitura", "")), tid + " · memorização", ["especificas", b, tid, "memo"], "memo:" + tid)
        n_memo += 1

out = os.path.join(ROOT, "agenda", "ppcomp-2027.apkg")
genanki.Package(list(decks.values())).write_to_file(out)
print(out, "| vocab", n_vocab, "| artigos", n_art, "| exercícios", n_ex, "| ganchos", n_memo, "| total", n_vocab + n_art + n_ex + n_memo)
