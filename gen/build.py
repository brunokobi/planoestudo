import json, sys, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "gen"); OUT = os.path.join(ROOT, "agenda"); INDEX = os.path.join(ROOT, "agenda-ppcomp-2027.html")
os.makedirs(OUT, exist_ok=True)
d = json.load(open(G + "/data.json"))
W = {1:("Diagnóstico, inscrição e lógica inicial","Anote a nota-base do diagnóstico (N1 e N2): ela mostra onde pôr horas extras."),
 2:("Lógica proposicional + operadores Python","Checkpoint L1 (14/11): 20 questões de lógica com pelo menos 85% de acerto."),
 3:("Python I: teste de mesa","Refazer as Q11–15 das três provas de 2025 sem errar nenhuma."),
 4:("Python II: funções e recursão","Checkpoint 1 (28/11): prova 2025-1 com Específicas ≥ 16/20 e Inglês ≥ 8/10."),
 5:("Estruturas lineares: pilha, fila, lista","Escrever Pilha e FilaCircular de memória; acertar 10/10 questões de identificar a estrutura."),
 6:("Hash, heap e custo das operações","Taxa paga e comprovante enviado até 13/12."),
 7:("Árvores binárias de busca + currículo","Checkpoint 2 (19/12): prova 2025-2 com Específicas ≥ 17/20; dossiê do currículo pronto."),
 8:("Semana leve (Natal): grafos e revisão","Nenhum tema com acerto abaixo de 70% no caderno de erros."),
 9:("Busca: BFS, DFS e binária","Acertar todas as questões de grafos e de busca binária das provas."),
 10:("Ordenação I: bubble, selection, insertion","Escrever os 3 sorts de memória e acertar 8/8 questões de 'lista após k iterações'."),
 11:("Ordenação II e complexidade","Checkpoint 3 (16/01): simulado A com 22/30."),
 12:("Simulados completos","N2 ≥ 24/30 em 2 de 3 simulados."),
 13:("Lapidação pelo caderno de erros","Nenhum erro repetido no simulado final."),
 14:("Reta final e prova","Fazer a prova com calma, seguindo a tática ensaiada.")}
weeks = []
for n in range(1, 15):
    ds = [x for x in d["days"] if x["wk"] == n]
    weeks.append(dict(n=n, range=ds[0]["dm"] + " a " + ds[-1]["dm"], title=W[n][0], cp=W[n][1]))
d["weeks"] = weeks

import re
P = open(os.path.join(ROOT, "plano-ppcomp-2027.html")).read()
def sec(i):
    m = re.search(r'<section id="'+i+r'">(.*?)</section>\n', P, re.S); return m.group(1)
facts = re.search(r'<div class="facts">.*?</div>\n  </div>', P, re.S).group(0)
pasta = re.search(r'<section>\s*<div class="eyebrow">Material na pasta</div>(.*?)</section>', P, re.S).group(1)
AN = dict(resumo='<div class="eyebrow">Resumo</div><h2>O edital em números</h2>'+facts+sec("gemini"),
  metodo=sec("metodo"), ranking=sec("ranking"), prova=sec("prova2027").replace('class="legend"','class="legend circ"'),
  pegadinhas=sec("armadilhas"), diad=sec("diaD"), curriculo=sec("curriculo"), pasta=pasta)
for k in AN: AN[k] = AN[k].replace('href="#diaD"','href="#diad"').replace('href="#cronograma"','href="inicio.html"')
d["analise"] = AN
d["sims"] = json.load(open(G + "/sims.json"))
sys.path.insert(0, G)
import articles, prov_en
d["prov"] = prov_en.build(articles.A)
_pt = {r["url"]: r for r in d["prov"]["rank"]}
for a in d["arts"]:
    r = _pt[a["url"]]; a["pri"] = r["tier"]; a["score"] = r["total"]; a["pos"] = r["pos"]
    if r["note"]: a["why"] = r["note"]
open(OUT + "/data.js", "w").write("window.DATA=" + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + ";")
shutil.copy(G + "/app.js", OUT + "/app.js"); shutil.copy(G + "/style.css", OUT + "/style.css"); shutil.copy(G + "/ifes-logo.svg", OUT + "/ifes-logo.svg")
# Variante sem a marca do Ifes (para o link do Claude): ARTIFACT_OUT=<pasta> python3 gen/build.py
ART = os.environ.get("ARTIFACT_OUT")
if ART:
    os.makedirs(ART, exist_ok=True)
    for f in ("data.js", "app.js", "style.css"): shutil.copy(OUT + "/" + f, ART + "/" + f)
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
BODY = '<header class="top" id="top"></header>\n<main id="app" class="wrap"></main>\n<script src="data.js"></script>\n<script src="app.js"></script>'
NEUTRAL_ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Crect width=%2764%27 height=%2764%27 rx=%2714%27 fill=%27%231f3a8a%27/%3E%3Ctext x=%2732%27 y=%2742%27 font-family=%27sans-serif%27 font-size=%2726%27 font-weight=%27700%27 text-anchor=%27middle%27 fill=%27white%27%3EPP%3C/text%3E%3C/svg%3E">'
def page(fname, title, attrs):
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<link rel="stylesheet" href="style.css">
{{ICON}}
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body {attrs}{{BRAND}}>
{BODY}
</body>
</html>
'''
    open(OUT + "/" + fname, "w").write(html.replace("{ICON}", '<link rel="icon" type="image/svg+xml" href="ifes-logo.svg">').replace("{BRAND}", ' data-brand="ifes"'))
    if ART: open(ART + "/" + fname, "w").write(html.replace("{ICON}", NEUTRAL_ICON).replace("{BRAND}", ""))
for w in weeks:
    page(f"semana-{w['n']:02d}.html", f"Semana {w['n']} · PPComp", f'data-page="semana" data-week="{w["n"]}"')
page("analise.html", "Análise da prova · PPComp", 'data-page="analise"')
page("inicio.html", "Agenda PPComp 2027", 'data-page="home"')
page("index.html", "Agenda PPComp 2027", 'data-page="home"')
page("simulados.html", "Simulados · PPComp", 'data-page="simulados"')
page("ingles.html", "Inglês · PPComp", 'data-page="ingles"')
page("mapa.html", "Mapa mental · PPComp", 'data-page="mapa"')
page("quadro.html", "Quadro · PPComp", 'data-page="kanban"')
page("temas.html", "Temas · PPComp", 'data-page="temas"')
page("tecnicas.html", "Técnicas · PPComp", 'data-page="tecnicas"')
# index = página principal (o publish envolve no esqueleto)
open(INDEX, "w").write(f'''<title>Agenda PPComp 2027</title>
<meta name="claude:viewport-fit-sides" content="cover">
{NEUTRAL_ICON}
{FONTS}
<link rel="stylesheet" href="style.css">
{BODY}
''')
print(sorted(os.listdir(OUT)))
