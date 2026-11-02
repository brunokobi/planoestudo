# Gera os simulados A–E. Respostas de código: execução real. Lógica: tabela-verdade.
import io, contextlib, random, itertools, json, sys, math
from collections import deque
sys.path.insert(0, sys.argv[1])
from sim_en import TEXTS

def run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {"__name__": "__sim__"})
    return buf.getvalue().strip()

def safe_run(code):
    try: return run(code)
    except Exception: return None

class Q(dict): pass
def mk(bloco, stem, correct, wrongs, why="", code=None):
    correct = str(correct)
    ws = []
    for w in wrongs:
        w = str(w)
        if w and w != correct and w not in ws: ws.append(w)
    return Q(bloco=bloco, stem=stem, code=code, correct=correct, wrongs=ws, why=why)

def numfill(correct, ws, rng, need=4):
    """completa distratores numéricos com perturbações plausíveis"""
    try: c = int(correct)
    except ValueError: return ws
    cand = [c+1, c-1, c+2, c-2, c*2, c+3, c-3, c+5, -c if c else 7, c+10]
    rng.shuffle(cand)
    for x in cand:
        if len(ws) >= need: break
        if c >= 0 and x < 0: continue
        if str(x) != str(correct) and str(x) not in ws: ws.append(str(x))
    return ws

import ast
def genfill(correct, ws, rng, need=4):
    ws = numfill(correct, ws, rng, need)
    if len(ws) >= need: return ws
    cands = []
    try:
        v = ast.literal_eval(correct)
        if isinstance(v, (list, tuple)) and len(v) > 1:
            L = list(v)
            cands += [L[::-1], sorted(L), L[1:] + L[:1], L[:-1], [x + 1 if isinstance(x, int) else x for x in L]]
            m = L[:]; m[0], m[-1] = m[-1], m[0]; cands.append(m)
            cands = [str(type(v)(c)) for c in cands]
    except Exception:
        pass
    for sep in (", ", " → "):
        if sep in correct and not correct.startswith("["):
            parts = correct.split(sep)
            for i in range(1, len(parts) - 1):
                m = parts[:]; m[i], m[i + 1] = m[i + 1], m[i]; cands.append(sep.join(m))
            cands.append(sep.join(parts[:1] + parts[1:][::-1]))
            rng.shuffle(cands)
            break
    toks = correct.split()
    if len(toks) > 1 and not cands:
        cands += [" ".join(toks[::-1]), " ".join(toks[1:] + toks[:1]), " ".join(toks[:-1]), " ".join(sorted(toks))]
    if not cands:
        cands += [correct.upper(), correct.lower(), correct.capitalize(), correct[::-1], correct.swapcase()]
    for c in cands:
        if len(ws) >= need: break
        if c and c != correct and c not in ws: ws.append(c)
    return ws

def code_q(bloco, stem, code, mutations, rng, why=""):
    correct = run(code)
    ws = []
    for a, b in mutations:
        out = safe_run(code.replace(a, b))
        if out is not None and out != correct and out not in ws and out != "": ws.append(out)
    ws = genfill(correct, ws, rng)
    return mk(bloco, stem, correct, ws, why or "Saída obtida executando o código. Faça o teste de mesa e confira linha a linha.", code)

# ---------------- PYTHON ----------------
def py_templates(rng):
    T = []
    n = rng.randint(6, 9)
    T.append(lambda: code_q("Python","Qual o valor impresso?",
        f"def calcular(n):\n    total = 0\n    for i in range(1, n + 1):\n        if i % 3 == 0:\n            total -= i\n        else:\n            total += i\n    return total\nprint(calcular({n}))",
        [("range(1, n + 1)","range(1, n)"),("total -= i","total += i"),("i % 3 == 0","i % 3 != 0"),("range(1, n + 1)","range(n + 1)")], rng,
        "Some os que não são múltiplos de 3 e subtraia os múltiplos de 3."))
    x = rng.choice([18, 25, 30, 40, 50])
    T.append(lambda: code_q("Python","Qual o valor impresso?",
        f"def f(x):\n    m = 0\n    soma = 0\n    while soma < x:\n        m += 1\n        soma += m * 2\n    return m, soma\nprint(f({x}))",
        [("soma < x","soma <= x"),("soma += m * 2","soma += m"),("m += 1\n        soma += m * 2","soma += m * 2\n        m += 1")], rng,
        "Acompanhe m e soma a cada volta; o laço para quando soma ≥ x."))
    a, b = rng.choice([(17,5),(23,4),(29,6),(38,7),(19,4)])
    T.append(lambda: code_q("Python","Qual o valor impresso?",
        f"x = {a}\ny = {b}\nz = x // y * 2 + x % y ** 2\nprint(z)",
        [("x // y * 2 + x % y ** 2","x / y * 2 + x % y ** 2"),("x // y * 2 + x % y ** 2","x // y * 2 + (x % y) ** 2"),("x // y * 2 + x % y ** 2","x // (y * 2) + x % y ** 2"),("x // y * 2 + x % y ** 2","x % y * 2 + x // y ** 2")], rng,
        "Precedência: ** antes de * / // %, e estes antes de +. Então x % y ** 2 é x % (y²)."))
    k = rng.randint(2, 5)
    T.append(lambda: code_q("Python","O que será impresso?",
        f"def f(x):\n    y = x - {k}\n    return y * 3\nprint(f(f({k+3})))",
        [("return y * 3","return x * 3"),(f"print(f(f({k+3})))",f"print(f({k+3}))"),(f"y = x - {k}",f"y = x + {k}")], rng,
        "Resolva de dentro para fora: primeiro f(interno), depois f do resultado."))
    m = rng.randint(3, 4)
    T.append(lambda: code_q("Python","O que será impresso?",
        f"def rec(n):\n    if n == 0:\n        return\n    print(n, end=' ')\n    rec(n - 1)\n    print(n * 10, end=' ')\nrec({m})",
        [("print(n, end=' ')\n    rec(n - 1)","rec(n - 1)\n    print(n, end=' ')"),("rec(n - 1)\n    print(n * 10, end=' ')","print(n * 10, end=' ')\n    rec(n - 1)"),("if n == 0","if n == 1")], rng,
        "O que vem antes da chamada recursiva sai na ida; o que vem depois sai na volta, em ordem inversa."))
    L = rng.sample(range(1, 15), 6)
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"def s(lista):\n    if not lista:\n        return 0\n    return lista[0] + s(lista[2:])\nprint(s({L}))",
        [("lista[2:]","lista[1:]"),("lista[0] + s","lista[-1] + s"),("lista[2:]","lista[3:]")], rng,
        "lista[2:] pula de 2 em 2: soma os elementos dos índices 0, 2, 4…"))
    V = rng.sample(range(2, 20), 5)
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"v = {V}\nfor i in range(len(v)):\n    if v[i] % 2 == 0:\n        v[i] //= 2\n    else:\n        v[i] = v[i] * 3 + 1\nprint(v)",
        [("v[i] //= 2","v[i] /= 2"),("v[i] % 2 == 0","v[i] % 2 != 0"),("range(len(v))","range(len(v) - 1)")], rng,
        "Percorra cada posição: par → metade inteira; ímpar → 3x + 1."))
    word = rng.choice(["computacao","algoritmo","estrutura","programador","pesquisa"])
    T.append(lambda: code_q("Python","Qual é a saída?",
        f"def alterar(s):\n    r = ''\n    for i in range(len(s)):\n        if s[i] in 'aeiou' and i % 2 == 0:\n            r += s[i].upper()\n        else:\n            r += s[i]\n    return r\nprint(alterar('{word}'))",
        [("i % 2 == 0","i % 2 != 0"),("and i % 2 == 0","or i % 2 == 0"),("s[i] in 'aeiou' and ","")], rng,
        "Só vira maiúscula a vogal que está em índice par (0, 2, 4…)."))
    a, b, c = rng.sample(range(1, 9), 3)
    T.append(lambda: code_q("Python","O que será impresso?",
        f"a, b, c = {a}, {b}, {c}\nr = a > b and b > c or a < c\nprint(r, a < b or c)",
        [(" and "," or "),("a < b or c","a < b and c"),("or a < c","and a < c")], rng,
        "and tem precedência sobre or. O or devolve o 1º valor verdadeiro; se nenhum for, devolve o último."))
    num = rng.choice([4096, 1203, 2750, 9081, 3540])
    T.append(lambda: code_q("Python","Qual o retorno de f?",
        f"def f(num):\n    r = 0\n    while num > 0:\n        r = r * 10 + num % 10\n        num //= 10\n    return r\nprint(f({num}))",
        [("r * 10 + num % 10","r + num % 10"),("num //= 10","num //= 100"),("num % 10","num // 10")], rng,
        "Cada volta tira o último dígito (num % 10) e o põe à direita de r: inverte o número. Zeros à esquerda somem."))
    n2 = rng.randint(4, 6)
    T.append(lambda: code_q("Python","Qual o valor impresso?",
        f"c = 0\nfor i in range({n2}):\n    for j in range(i, {n2}):\n        if (i + j) % 2 == 0:\n            c += 1\nprint(c)",
        [("range(i, ","range(i + 1, "),("% 2 == 0","% 2 != 0"),(f"for j in range(i, {n2})",f"for j in range({n2})")], rng,
        "Conte os pares (i, j) com j ≥ i e i + j par."))
    lst = rng.sample(range(1, 30), 5); alvo = rng.choice([lst[2] + 1, lst[3]])
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"def busca(lista, x):\n    for i, e in enumerate(lista):\n        if e == x:\n            print('achou', i)\n            break\n    else:\n        print('nao achou')\nbusca({lst}, {alvo})",
        [("break","pass"),("enumerate(lista)","enumerate(lista, 1)"),("if e == x","if e != x")], rng,
        "O else do for só executa se o laço terminar sem break."))
    a2, b2, m2 = rng.randint(1, 4), rng.randint(10, 16), rng.choice([2, 3])
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"print([x * {m2} for x in range({a2}, {b2}) if x % {m2+1} == 0])",
        [(f"range({a2}, {b2})",f"range({a2}, {b2+1})"),(f"x * {m2}","x"),(f"x % {m2+1} == 0",f"x % {m2} == 0")], rng,
        "Gere os x do range (o fim não entra), filtre pelo if e só então aplique a expressão."))
    v = list(range(rng.randint(1, 3), rng.randint(9, 12)))
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"v = {v}\nprint(v[2:7:2], v[::-3][:2], v[-2])",
        [("v[2:7:2]","v[2:8:2]"),("v[::-3][:2]","v[::3][:2]"),("v[-2]","v[-1]")], rng,
        "Fatiamento [início:fim:passo]: o fim não entra; passo negativo percorre de trás para frente."))
    x1, y1 = rng.randint(1, 5), rng.randint(6, 9)
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"a = [{x1}, {y1}]\nb = a\nc = a[:]\nb.append(0)\nc.append(1)\nc.append(2)\nprint(len(a), len(b), len(c))",
        [("b = a","b = a[:]"),("c = a[:]","c = a")], rng,
        "b = a é a MESMA lista (alias); a[:] cria uma cópia."))
    d = rng.randint(3, 4)
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"m = [[i * {d} + j for j in range({d})] for i in range({d})]\nprint(sum(m[i][i] for i in range({d})), m[{d-1}][0])",
        [("m[i][i]",f"m[i][{d-1} - i]"),(f"m[{d-1}][0]",f"m[0][{d-1}]"),(f"i * {d} + j","i + j")], rng,
        "Monte a matriz linha a linha; a diagonal principal tem i == j."))
    w2 = rng.choice(["banana","abacaxi","paralelepipedo","engenharia"])
    T.append(lambda: code_q("Python","Qual será a saída?",
        f"d = {{}}\nfor c in '{w2}':\n    d[c] = d.get(c, 0) + 1\nprint(d['a'], len(d))",
        [("d.get(c, 0) + 1","1"),("len(d)",f"len('{w2}')")], rng,
        "O dicionário conta as ocorrências de cada letra; len(d) é o número de letras distintas."))
    b3, e3 = rng.randint(2, 3), rng.randint(4, 6)
    T.append(lambda: code_q("Python","Qual o valor impresso?",
        f"def pot(b, e):\n    if e == 0:\n        return 1\n    return b * pot(b, e - 1)\nprint(pot({b3}, {e3}) - {e3})",
        [("if e == 0:\n        return 1","if e == 1:\n        return 1"),("b * pot(b, e - 1)","b + pot(b, e - 1)")], rng,
        "pot(b, e) = bᵉ."))
    return T

# ---------------- ESTRUTURAS DE DADOS ----------------
def ed_templates(rng):
    T = []
    def pilha():
        ops, p, popped = [], [], []
        vals = iter(rng.sample(range(1, 40), 12))
        for _ in range(8):
            if p and rng.random() < 0.4: ops.append("pop()"); popped.append(p.pop())
            else: v = next(vals); ops.append(f"push({v})"); p.append(v)
        correct = f"topo = {p[-1]}, tamanho = {len(p)}" if p else "pilha vazia"
        q = [list(x) for x in [p]]
        ws = [f"topo = {p[0]}, tamanho = {len(p)}" if p else "topo = 1", f"topo = {p[-1]}, tamanho = {len(p)+1}" if p else "x",
              f"topo = {popped[-1] if popped else 0}, tamanho = {len(p)}", f"topo = {p[-2] if len(p)>1 else 99}, tamanho = {len(p)-1}"]
        return mk("Estruturas de Dados", "Numa pilha inicialmente vazia são executadas, em ordem: " + ", ".join(ops) + ". Ao final, qual o topo e o tamanho da pilha?", correct, ws, "LIFO: cada pop remove o último elemento inserido que ainda está na pilha.")
    T.append(pilha)
    def posfixa():
        e = rng.choice(["4 2 3 * + 5 -","8 3 - 2 *","9 3 / 4 2 * +","5 1 2 + 4 * + 3 -","7 2 3 * - 4 +","6 2 + 3 * 4 -"])
        code = "def ev(e):\n    s = []\n    for t in e.split():\n        if t.isdigit():\n            s.append(int(t))\n        else:\n            b = s.pop()\n            a = s.pop()\n            if t == '+': s.append(a + b)\n            elif t == '-': s.append(a - b)\n            elif t == '*': s.append(a * b)\n            else: s.append(a // b)\n    return s.pop()\nprint(ev('" + e + "'))"
        return code_q("Estruturas de Dados","A função avalia uma expressão pós-fixa com uma pilha. Qual a saída?", code,
            [("b = s.pop()\n            a = s.pop()","a = s.pop()\n            b = s.pop()")], rng, "Número entra na pilha; operador desempilha b (topo) e depois a, e empilha a op b.")
    T.append(posfixa)
    def balanc():
        good = rng.choice(["{ [ ( ) ( ) ] }","( [ { } ] ) ( )","[ ( ) { [ ] } ]"])
        bads = ["( [ ) ]","{ [ ( ] ) }","( ( ) ] )","[ { ( ) } ] )","{ ( [ ] }"]
        rng.shuffle(bads)
        return mk("Estruturas de Dados","Usando uma pilha para verificar o balanceamento de símbolos, qual das sequências está BALANCEADA?", good, bads[:4],
                  "Empilha ao abrir; ao fechar, o topo precisa ser o par correspondente; no fim, a pilha precisa estar vazia.")
    T.append(balanc)
    def fila():
        a = rng.sample(range(1, 30), 5)
        code = f"from collections import deque\nd = deque({a[:3]})\nd.append({a[3]})\nd.appendleft({a[4]})\nd.popleft()\nd.pop()\nd.append(d.popleft())\nprint(list(d))"
        return code_q("Estruturas de Dados","Qual será a saída?", code,
            [("d.popleft()\nd.pop()","d.pop()\nd.popleft()"),("d.append(d.popleft())","d.appendleft(d.pop())"),("d.appendleft(","d.append(")], rng,
            "deque: append/pop atuam no fim; appendleft/popleft atuam no início.")
    T.append(fila)
    def heap():
        letters = rng.sample("ABCDEFGH", 5); pr = [rng.randint(1, 3) for _ in range(5)]
        items = list(zip(pr, letters))
        code = f"import heapq\nh = []\nfor it in {items}:\n    heapq.heappush(h, it)\nprint([heapq.heappop(h)[1] for _ in range(3)])"
        corr = run(code)
        ws = [str([x[1] for x in items[:3]]), str([x[1] for x in sorted(items, reverse=True)[:3]]),
              str([x[1] for x in sorted(items, key=lambda t: t[0])[:3]]), str(sorted(letters)[:3])]
        return mk("Estruturas de Dados","As tuplas (prioridade, rótulo) são inseridas num heap com heapq. Qual a saída?", corr, ws,
                  "heapq é min-heap e compara tuplas elemento a elemento: menor prioridade primeiro e, em empate, o menor rótulo.", code)
    T.append(heap)
    def hashq():
        m = rng.choice([7, 11]); keys = rng.sample(range(10, 80), 6)
        idx = [k % m for k in keys]; col = len(keys) - len(set(idx))
        return mk("Estruturas de Dados", f"Uma tabela hash de tamanho {m} usa h(k) = k mod {m} e encadeamento. Inserindo as chaves {', '.join(map(str, keys))}, quantas colisões ocorrem (inserções em posição já ocupada)?",
                  col, numfill(col, [], rng), f"Índices: {', '.join(str(i) for i in idx)}. Conte as repetições.")
    T.append(hashq)
    def bst_trav():
        seq = rng.sample(range(1, 40), 7)
        code = ("class N:\n    def __init__(s, v): s.v, s.l, s.r = v, None, None\n"
                "def ins(r, v):\n    if r is None: return N(v)\n    if v < r.v: r.l = ins(r.l, v)\n    else: r.r = ins(r.r, v)\n    return r\n"
                "def pre(r): return [] if r is None else [r.v] + pre(r.l) + pre(r.r)\n"
                "def pos(r): return [] if r is None else pos(r.l) + pos(r.r) + [r.v]\n"
                "def emo(r): return [] if r is None else emo(r.l) + [r.v] + emo(r.r)\n"
                f"raiz = None\nfor v in {seq}: raiz = ins(raiz, v)\n")
        kind = rng.choice(["pré-ordem", "pós-ordem"])
        f = "pre" if kind == "pré-ordem" else "pos"
        corr = run(code + f"print({f}(raiz))")
        ws = [run(code + f"print({g}(raiz))") for g in ("pre", "pos", "emo") if g != f] + [str(seq), str(seq[::-1])]
        return mk("Estruturas de Dados", f"Os valores {', '.join(map(str, seq))} são inseridos, nessa ordem, numa árvore binária de busca inicialmente vazia. Qual o percurso em {kind}?",
                  corr, ws, "Desenhe a árvore. Pré: raiz-esq-dir; em: esq-raiz-dir (ordenado); pós: esq-dir-raiz.")
    T.append(bst_trav)
    def bst_fl():
        seq = rng.sample(range(1, 50), 8)
        code = ("class N:\n    def __init__(s, v): s.v, s.l, s.r = v, None, None\n"
                "def ins(r, v):\n    if r is None: return N(v)\n    if v < r.v: r.l = ins(r.l, v)\n    else: r.r = ins(r.r, v)\n    return r\n"
                "def folhas(r):\n    if r is None: return 0\n    if r.l is None and r.r is None: return 1\n    return folhas(r.l) + folhas(r.r)\n"
                "def alt(r): return 0 if r is None else 1 + max(alt(r.l), alt(r.r))\n"
                f"raiz = None\nfor v in {seq}: raiz = ins(raiz, v)\nprint(folhas(raiz), alt(raiz))")
        corr = run(code); f_, a_ = map(int, corr.split())
        ws = [f"{f_+1} {a_}", f"{f_} {a_-1}", f"{f_-1} {a_+1}", f"{f_} {a_+1}", f"{a_} {f_}"]
        return mk("Estruturas de Dados", f"Inserindo {', '.join(map(str, seq))} (nessa ordem) numa BST vazia, o código abaixo imprime o número de folhas e a altura (em nós). Qual a saída?",
                  corr, ws, "Desenhe a árvore, conte os nós sem filhos e o maior caminho raiz → folha.", code.split("raiz = None")[0] + "# ... inserções ...\nprint(folhas(raiz), alt(raiz))")
    T.append(bst_fl)
    def circ():
        tam = rng.choice([4, 5]); e1 = rng.randint(tam - 1, tam); d1 = rng.randint(2, 3); e2 = rng.randint(1, 2)
        ini, fim, cnt = 0, 0, 0
        for _ in range(e1): fim = (fim + 1) % tam; cnt += 1
        for _ in range(d1): ini = (ini + 1) % tam; cnt -= 1
        for _ in range(e2): fim = (fim + 1) % tam; cnt += 1
        corr = f"inicio = {ini}, fim = {fim}, contador = {cnt}"
        ws = [f"inicio = {ini}, fim = {e1+e2}, contador = {cnt}", f"inicio = {d1-1}, fim = {fim}, contador = {cnt}", f"inicio = {ini}, fim = {fim}, contador = {e1+e2}", f"inicio = {fim}, fim = {ini}, contador = {cnt}"]
        return mk("Estruturas de Dados", f"Uma fila circular de tamanho {tam} começa com inicio = fim = contador = 0. Enfileirar faz fim = (fim + 1) % {tam}; desenfileirar faz inicio = (inicio + 1) % {tam}. Após {e1} enfileiramentos, {d1} desenfileiramentos e mais {e2} enfileiramentos, qual o estado?",
                  corr, ws, "Some os passos módulo o tamanho; o contador é enfileirados − desenfileirados.")
    T.append(circ)
    def encad():
        vals = rng.sample(range(1, 10), 5)
        code = ("class No:\n    def __init__(s, v, p=None): s.v, s.p = v, p\n"
                f"cab = None\nfor v in {vals[::-1]}:\n    cab = No(v, cab)\n"
                "def f(n):\n    if n is None:\n        return\n    print(n.v, end='')\n    if n.p:\n        f(n.p.p)\n    print(n.v, end='')\nf(cab)")
        return code_q("Estruturas de Dados", f"A lista encadeada contém {' -> '.join(map(str, vals))}. Qual a saída?", code,
                      [("f(n.p.p)","f(n.p)"),("    print(n.v, end='')\n    if n.p","    if n.p"),("print(n.v, end='')\nf(cab)","pass\nf(cab)")], rng,
                      "A função imprime ao descer e ao voltar, pulando de 2 em 2 nós.")
    T.append(encad)
    CONC = [
      ("Qual estrutura é a mais adequada para implementar a função 'desfazer' (Ctrl+Z) de um editor?","Pilha",["Fila","Tabela hash","Heap","Árvore binária de busca"],"A última ação feita é a primeira desfeita: LIFO."),
      ("Num pronto-socorro, os pacientes são atendidos pelo nível de urgência. Qual estrutura é a mais adequada?","Heap (fila de prioridade)",["Pilha","Fila simples","Lista encadeada","Matriz"],"Fila de prioridade remove sempre o mais prioritário em O(log n)."),
      ("Para verificar rapidamente se um CPF já está cadastrado, sem importar a ordem, qual estrutura é a mais adequada?","Tabela hash",["Lista","Pilha","Fila","Lista encadeada"],"Busca em O(1) no caso médio."),
      ("Documentos enviados a uma impressora são impressos na ordem de chegada. Que estrutura modela isso?","Fila",["Pilha","Heap","Árvore binária de busca","Tabela hash"],"FIFO."),
      ("Qual a complexidade de remover o menor elemento de um heap binário com n elementos?","O(log n)",["O(1)","O(n)","O(n log n)","O(n²)"],"Remove a raiz e desce o último elemento pela altura do heap."),
      ("Qual a complexidade da busca numa BST construída inserindo 1, 2, 3, …, n nessa ordem?","O(n)",["O(1)","O(log n)","O(n log n)","O(n²)"],"A árvore degenera numa lista."),
      ("O percurso em-ordem de uma árvore binária de busca produz as chaves:","em ordem crescente",["na ordem de inserção","em ordem decrescente","com a raiz primeiro","com as folhas primeiro"],"Esquerda (menores), raiz, direita (maiores)."),
      ("Num heap armazenado em vetor com índice inicial 0, os filhos do elemento de índice i ficam nos índices:","2i + 1 e 2i + 2",["2i e 2i + 1","i + 1 e i + 2","2i − 1 e 2i","i/2 e i/2 + 1"],"Com índice 0, o pai de i fica em (i − 1)//2."),
      ("Qual a complexidade de inserir um elemento no início de uma lista simplesmente encadeada?","O(1)",["O(n)","O(log n)","O(n log n)","O(n²)"],"Basta criar o nó e apontá-lo para a cabeça antiga."),
      ("Quantas árvores binárias de busca distintas podem ser formadas com 3 chaves diferentes?","5",["3","4","6","8"],"Número de Catalan C₃ = 5."),
      ("Qual estrutura permite inserir e remover elementos nas duas extremidades em O(1)?","Deque",["Pilha","Heap","Tabela hash","Árvore binária de busca"],"Deque = fila de duas pontas."),
      ("Qual a complexidade, no caso médio, de buscar uma chave numa tabela hash?","O(1)",["O(n)","O(log n)","O(n log n)","O(n²)"],"A função hash leva direto ao índice; colisões são poucas no caso médio."),
      ("Numa fila, após enfileirar A, B e C (nessa ordem) e desenfileirar uma vez, qual elemento fica na frente?","B",["A","C","Nenhum, a fila fica vazia","D"],"FIFO: sai o A; o B passa a ser o primeiro."),
      ("Qual a principal vantagem de uma lista encadeada sobre um vetor?","Inserir e remover sem deslocar os demais elementos",["Acesso por índice em O(1)","Ocupar menos memória por elemento","Manter os elementos sempre ordenados","Permitir busca binária"],"Basta ajustar as referências; em compensação, o acesso por índice é O(n)."),
      ("Qual a altura mínima (em nós) de uma árvore binária com 15 nós?","4",["3","5","7","15"],"Árvore cheia: 1 + 2 + 4 + 8 = 15 nós em 4 níveis."),
      ("Em Python, qual a complexidade de 'x in lista' no pior caso e de 'x in conjunto' no caso médio?","O(n) e O(1)",["O(1) e O(n)","O(log n) e O(1)","O(n) e O(log n)","O(1) e O(1)"],"Lista percorre; set é tabela hash."),
    ]
    for c in CONC: T.append(lambda c=c: mk("Estruturas de Dados", c[0], c[1], c[2], c[3]))
    return T

# ---------------- BUSCA ----------------
def rand_graph(rng, n):
    nodes = list(range(1, n + 1)); g = {v: [] for v in nodes}
    for v in nodes[1:]:
        u = rng.choice(nodes[:v - 1]); g[u].append(v)
    for _ in range(rng.randint(1, 3)):
        u, v = sorted(rng.sample(nodes, 2))
        if v not in g[u]: g[u].append(v)
    for v in g: rng.shuffle(g[v])
    return g
def bfs(g, s):
    vis, f, o = set(), deque([s]), []
    while f:
        v = f.popleft()
        if v not in vis: vis.add(v); o.append(v); f.extend(g[v])
    return o
def dfs(g, s):
    o = []
    def go(v):
        o.append(v)
        for w in g[v]:
            if w not in o: go(w)
    go(s); return o
def busca_templates(rng):
    T = []
    def bfsq():
        for _ in range(50):
            g = rand_graph(rng, 7)
            if bfs(g, 1) != dfs(g, 1): break
        ws = [dfs(g, 1), bfs({k: v[::-1] for k, v in g.items()}, 1), sorted(bfs(g, 1)), dfs({k: v[::-1] for k, v in g.items()}, 1)]
        code = "from collections import deque\ndef run(grafo, inicio):\n    visitados, fila, ordem = set(), deque([inicio]), []\n    while fila:\n        v = fila.popleft()\n        if v not in visitados:\n            visitados.add(v)\n            ordem.append(v)\n            fila.extend(grafo[v])\n    return ordem\ngrafo = " + str(g) + "\nprint(run(grafo, 1))"
        return mk("Busca", "Qual a saída do código abaixo?", str(bfs(g, 1)), [str(w) for w in ws], "Busca em largura: a fila visita por níveis, na ordem das listas de adjacência.", code)
    T.append(bfsq)
    def dfsq():
        for _ in range(50):
            g = rand_graph(rng, 7)
            if bfs(g, 1) != dfs(g, 1): break
        ws = [bfs(g, 1), dfs({k: v[::-1] for k, v in g.items()}, 1), sorted(dfs(g, 1)), bfs({k: v[::-1] for k, v in g.items()}, 1)]
        return mk("Busca", f"Dado o grafo direcionado representado pelo dicionário de adjacência {g}, qual a ordem de visita da busca em profundidade (DFS recursiva, visitando os vizinhos na ordem da lista) a partir do nó 1?",
                  ", ".join(map(str, dfs(g, 1))), [", ".join(map(str, w)) for w in ws], "DFS vai até o fim do primeiro vizinho antes de passar para o próximo.")
    T.append(dfsq)
    def binq():
        n = rng.choice([7, 9, 11, 15]); v = sorted(rng.sample(range(2, 99), n))
        for alvo in rng.sample(v, n):
            l, r, comp = 0, n - 1, []
            while l <= r:
                m = (l + r) // 2; comp.append(v[m])
                if v[m] == alvo: break
                if v[m] < alvo: l = m + 1
                else: r = m - 1
            if len(comp) >= 3: break
        seq = v[:v.index(alvo) + 1]
        l, r, alt = 0, n - 1, []
        while l <= r:
            m = (l + r + 1) // 2; alt.append(v[m])
            if v[m] == alvo: break
            if v[m] < alvo: l = m + 1
            else: r = m - 1
        ws = [" → ".join(map(str, seq[-4:])), " → ".join(map(str, alt)), " → ".join(map(str, comp[::-1])), " → ".join(map(str, [v[n // 2], alvo])), " → ".join(map(str, comp[:-1] + [v[min(n - 1, v.index(alvo) + 1)], alvo]))]
        return mk("Busca", f"Dado o vetor ordenado {v}, qual a sequência de elementos comparados pela busca binária (meio = (esq + dir) // 2) para encontrar {alvo}?",
                  " → ".join(map(str, comp)), ws, "Compare com o meio; se for menor, vá para a direita (esq = meio + 1); se for maior, para a esquerda.")
    T.append(binq)
    def maxcomp():
        n = rng.choice([1000, 2000, 500, 100000, 1000000]); c = int(math.floor(math.log2(n))) + 1
        return mk("Busca", f"No pior caso, quantas comparações a busca binária faz, aproximadamente, num vetor ordenado de {n:,} elementos?".replace(",", "."),
                  c, [n // 2, n, c * 2, int(math.sqrt(n))], "⌊log₂ n⌋ + 1. Lembre: 2¹⁰ ≈ 1.000.")
    T.append(maxcomp)
    CONC = [
      ("Qual estrutura de dados auxiliar a busca em largura (BFS) utiliza?","Fila",["Pilha","Heap","Tabela hash","Árvore binária"],"BFS: Largura = fiLa."),
      ("Qual estrutura de dados a versão iterativa da busca em profundidade (DFS) utiliza?","Pilha",["Fila","Heap","Tabela hash","Matriz"],"DFS: Profundidade = Pilha."),
      ("Qual a complexidade de BFS ou DFS num grafo representado por listas de adjacência?","O(V + E)",["O(V²)","O(V · E)","O(log V)","O(E²)"],"Cada vértice e cada aresta são processados uma vez."),
      ("Qual é a pré-condição para aplicar a busca binária?","O vetor precisa estar ordenado",["O vetor não pode ter repetidos","O tamanho do vetor precisa ser par","Os elementos precisam ser inteiros","Os dados precisam estar numa lista encadeada"],"Sem ordenação, descartar metade não é válido."),
      ("Quantas comparações a busca sequencial faz no pior caso num vetor de n elementos?","n",["log₂ n","1","n²","n log n"],"Pode precisar olhar todos os elementos."),
      ("A matriz de adjacência de um grafo com n vértices é:","uma matriz n × n",["um vetor de tamanho n","uma matriz n × m, com m = número de arestas","um conjunto de listas de vizinhos","uma árvore de pares de vértices"],"Cada entrada [i][j] indica se há aresta entre i e j."),
      ("Para achar o caminho com menos arestas entre dois vértices de um grafo não ponderado, usa-se:","busca em largura (BFS)",["busca em profundidade (DFS)","busca binária","busca sequencial","ordenação por inserção"],"BFS visita por níveis de distância."),
      ("Num grafo não direcionado com 12 arestas, qual a soma dos graus de todos os vértices?","24",["12","6","144","36"],"Cada aresta contribui com 2 para a soma."),
      ("Na busca binária num vetor ordenado de 16 elementos, após a primeira comparação sem sucesso, quantos elementos restam, no máximo, para examinar?","8",["15","4","16","7"],"O meio é o índice 7: sobram 7 à esquerda ou 8 à direita."),
      ("Sobre a busca sequencial, é correto afirmar que:","funciona em listas não ordenadas",["exige que a lista esteja ordenada","tem complexidade O(log n)","só funciona com números","sempre encontra o elemento procurado"],"Ela compara elemento por elemento, do início ao fim."),
    ]
    for c in CONC: T.append(lambda c=c: mk("Busca", c[0], c[1], c[2], c[3]))
    return T

# ---------------- ORDENAÇÃO ----------------
def bubble_k(v, k):
    v = v[:]; n = len(v)
    for i in range(k):
        for j in range(n - i - 1):
            if v[j] > v[j + 1]: v[j], v[j + 1] = v[j + 1], v[j]
    return v
def sel_k(v, k):
    v = v[:]
    for i in range(k):
        m = i
        for j in range(i + 1, len(v)):
            if v[j] < v[m]: m = j
        v[i], v[m] = v[m], v[i]
    return v
def ins_k(v, k):
    v = v[:]
    for i in range(1, k + 1):
        key = v[i]; j = i - 1
        while j >= 0 and v[j] > key: v[j + 1] = v[j]; j -= 1
        v[j + 1] = key
    return v
def ord_templates(rng):
    T = []
    def passes(name, f, others):
        def q():
            for _ in range(100):
                v = rng.sample(range(1, 30), 6); k = rng.randint(1, 2) if name != "insertion" else rng.randint(2, 3)
                c = f(v, k); ws = [str(o(v, k)) for o in others] + [str(f(v, k + 1)), str(f(v, k - 1) if k > 1 else v), str(sorted(v))]
                ws = [w for w in dict.fromkeys(ws) if w != str(c)]
                if len(ws) >= 4: break
            lab = {"bubble": "passada", "selection": "iteração", "insertion": "inserção"}[name]
            extra = "" if name != "insertion" else " (a 1ª inserção trata o elemento de índice 1)"
            return mk("Ordenação", f"Dada a lista {v}, como ela fica após a {k}ª {lab} do {name.capitalize()} Sort em ordem crescente{extra}?", str(c), ws,
                      {"bubble": "Cada passada leva o maior elemento restante para o fim.", "selection": "Cada iteração i troca a posição i com o menor elemento do restante.", "insertion": "Cada inserção encaixa o próximo elemento na parte já ordenada à esquerda."}[name])
        return q
    T.append(passes("bubble", bubble_k, [sel_k, ins_k]))
    T.append(passes("selection", sel_k, [bubble_k, ins_k]))
    T.append(passes("insertion", ins_k, [bubble_k, sel_k]))
    def quickp():
        v = rng.sample(range(1, 30), 7); p = v[0]
        a = [x for x in v[1:] if x < p]; b = [x for x in v[1:] if x >= p]
        c = f"{a}, {p}, {b}"
        ws = [f"{sorted(a)}, {p}, {sorted(b)}", f"{b}, {p}, {a}", f"{[x for x in v if x < p]}, {v[-1]}, {[x for x in v if x > v[-1]]}", f"{a + [p]}, {b[0] if b else p}, {b[1:]}"]
        return mk("Ordenação", f"No quicksort abaixo, com a lista {v}, quais são subset1, pivo e subset2 na PRIMEIRA chamada?", c, ws,
                  "O pivô é o 1º elemento; as compreensões mantêm a ordem original dos elementos.",
                  "def quicksort(lista):\n    if len(lista) <= 1:\n        return lista\n    pivo = lista[0]\n    subset1 = [x for x in lista[1:] if x < pivo]\n    subset2 = [x for x in lista[1:] if x >= pivo]\n    return quicksort(subset1) + [pivo] + quicksort(subset2)")
    T.append(quickp)
    def mergeq():
        a = sorted(rng.sample(range(1, 40), 4)); b = sorted(rng.sample(range(1, 40), 4))
        code = f"def merge(a, b):\n    r, i, j, comp = [], 0, 0, 0\n    while i < len(a) and j < len(b):\n        comp += 1\n        if a[i] <= b[j]:\n            r.append(a[i]); i += 1\n        else:\n            r.append(b[j]); j += 1\n    return r + a[i:] + b[j:], comp\nprint(merge({a}, {b})[1])"
        return code_q("Ordenação", "Quantas comparações a intercalação (merge) abaixo faz?", code, [("comp += 1\n","")], rng,
                      "Conte uma comparação por volta do while; ele para quando uma das listas acaba.")
    T.append(mergeq)
    CONC = [
      ("Qual algoritmo tem complexidade O(n log n) no melhor, no médio e no pior caso?","Merge Sort",["Quick Sort","Insertion Sort","Bubble Sort","Selection Sort"],"Merge divide sempre ao meio: T(n) = 2T(n/2) + n."),
      ("Qual a complexidade do Quick Sort no pior caso?","O(n²)",["O(n log n)","O(n)","O(log n)","O(2ⁿ)"],"Ocorre quando o pivô é sempre o menor ou o maior elemento."),
      ("Qual a complexidade do Insertion Sort quando a lista já está ordenada?","O(n)",["O(n²)","O(n log n)","O(log n)","O(1)"],"O while interno não executa nenhuma vez."),
      ("Quais algoritmos são estáveis?","Bubble, Insertion e Merge",["Quick, Selection e Heap","Selection e Merge","Quick e Insertion","Heap e Bubble"],"Mnemônico: BIM é estável, QSH não."),
      ("Qual destes NÃO é um algoritmo de ordenação por comparação?","Counting Sort",["Merge Sort","Quick Sort","Heap Sort","Insertion Sort"],"Counting conta as ocorrências: O(n + k)."),
      ("Quais algoritmos usam a estratégia de dividir para conquistar?","Merge Sort e Quick Sort",["Bubble Sort e Selection Sort","Insertion Sort e Bubble Sort","Selection Sort e Heap Sort","Counting Sort e Bubble Sort"],""),
      ("Qual o limite inferior de qualquer algoritmo de ordenação baseado em comparações?","Ω(n log n)",["Ω(n)","Ω(n²)","Ω(log n)","Ω(1)"],"Argumento da árvore de decisão (Cormen 8.1)."),
      ("Sobre o Merge Sort, é correto afirmar que:","usa memória auxiliar proporcional a n",["é in-place","tem pior caso O(n²)","não é estável","tem melhor caso O(n)"],""),
      ("No máximo, quantas trocas o Selection Sort faz para ordenar n elementos?","n − 1",["n²","n log n","n(n − 1)/2","1"],"Uma troca por iteração do laço externo."),
      ("Qual a complexidade do trecho? for i in range(n): j = 1; while j < n: j *= 2","O(n log n)",["O(n²)","O(n)","O(log n)","O(2ⁿ)"],"O while roda log n vezes para cada um dos n valores de i."),
      ("Qual a complexidade do trecho? i = n; while i > 1: i //= 2","O(log n)",["O(n)","O(n log n)","O(1)","O(n²)"],"i cai pela metade a cada volta."),
      ("Qual a complexidade de: def f(n): return 1 if n <= 1 else f(n − 1) + f(n − 1)?","O(2ⁿ)",["O(n)","O(n²)","O(log n)","O(n log n)"],"Duas chamadas com n − 1 dobram o trabalho a cada nível."),
      ("Qual linha completa o Insertion Sort? for i in range(1, len(arr)): key = arr[i]; j = i − 1; ______: arr[j + 1] = arr[j]; j −= 1 (e no fim arr[j + 1] = key)","while j >= 0 and arr[j] > key",["while j > 0 and arr[j] > key","while j >= 0 and arr[j] < key","while j >= i and arr[j] > key","if j >= 0 and arr[j] > key"],"j >= 0 inclui o índice 0; '>' mantém a estabilidade."),
      ("No Bubble Sort, dentro de 'if lista[j] > lista[j + 1]:', qual linha completa o algoritmo?","lista[j], lista[j + 1] = lista[j + 1], lista[j]",["lista[j] = lista[j + 1]","lista[j + 1] = lista[j]","lista[j] == lista[j + 1]","lista[j + 1] -= lista[j]"],"É preciso trocar os dois valores."),
      ("Ordene as funções da que cresce MENOS para a que cresce MAIS:","log n, n, n log n, n², 2ⁿ",["n, log n, n log n, 2ⁿ, n²","log n, n log n, n, n², 2ⁿ","n², n log n, n, log n, 2ⁿ","log n, n, n², n log n, 2ⁿ"],"A escada: 1 < log n < n < n log n < n² < 2ⁿ < n!"),
    ]
    for c in CONC: T.append(lambda c=c: mk("Ordenação", c[0], c[1], c[2], c[3]))
    return T

# ---------------- LÓGICA ----------------
def ev(f, a):
    t = f[0]
    if t == 'v': return a[f[1]]
    if t == 'not': return not ev(f[1], a)
    x, y = ev(f[1], a), ev(f[2], a)
    return {'and': x and y, 'or': x or y, 'imp': (not x) or y, 'iff': x == y}[t]
SYM = {'and': '∧', 'or': '∨', 'imp': '→', 'iff': '↔'}
def show(f, top=True):
    t = f[0]
    if t == 'v': return f[1]
    if t == 'not':
        return '∼' + (show(f[1], False) if f[1][0] in ('v', 'not') else '(' + show(f[1], True) + ')')
    s = show(f[1], False) + ' ' + SYM[t] + ' ' + show(f[2], False)
    return s if top else '(' + s + ')'
def atoms(f, acc=None):
    acc = set() if acc is None else acc
    if f[0] == 'v': acc.add(f[1])
    else:
        for g in f[1:]: atoms(g, acc)
    return acc
def table(f, names):
    return tuple(ev(f, dict(zip(names, vals))) for vals in itertools.product([True, False], repeat=len(names)))
V = lambda x: ('v', x); N = lambda x: ('not', x); A_ = lambda x, y: ('and', x, y); O_ = lambda x, y: ('or', x, y); I_ = lambda x, y: ('imp', x, y); B_ = lambda x, y: ('iff', x, y)
p, q, r = V('p'), V('q'), V('r')
def pool2():
    lits = [p, q, N(p), N(q)]; out = []
    for x in lits:
        for y in lits:
            if atoms(x) == atoms(y): continue
            for op in (A_, O_, I_, B_): out.append(op(x, y)); out.append(N(op(x, y)))
    return out
POOL2 = pool2()
def equiv_sym(rng):
    target = rng.choice([N(A_(p, q)), N(O_(p, q)), I_(p, q), N(I_(p, q)), B_(p, q), I_(N(p), q), A_(O_(p, q), N(p)), N(B_(p, q)), O_(N(p), q)])
    names = ['p', 'q']; tt = table(target, names); ts = show(target)
    eqs = [f for f in POOL2 if table(f, names) == tt and show(f) != ts and f[0] != 'not']
    eqs = eqs or [f for f in POOL2 if table(f, names) == tt and show(f) != ts]
    neq = [f for f in POOL2 if table(f, names) != tt]
    c = rng.choice(eqs); ws = rng.sample(neq, 4)
    return mk("Lógica", f"Qual das proposições é logicamente equivalente a  {ts} ?", show(c), [show(w) for w in ws], "Conferido por tabela-verdade: só a alternativa correta tem os mesmos valores em todas as linhas.")
def export_q(rng):
    target = I_(A_(p, q), r); names = ['p', 'q', 'r']; tt = table(target, names)
    cands = [I_(p, I_(q, r)), O_(O_(N(p), N(q)), r), I_(p, A_(q, r)), I_(I_(p, q), r), A_(p, I_(q, r)), I_(O_(p, q), r), O_(N(p), A_(N(q), r)), I_(N(r), A_(p, q))]
    eq = [f for f in cands if table(f, names) == tt]; ne = [f for f in cands if table(f, names) != tt]
    return mk("Lógica", "A fórmula (p ∧ q) → r é equivalente a:", show(rng.choice(eq)), [show(w) for w in rng.sample(ne, 4)], "Exportação: (p ∧ q) → r ≡ p → (q → r) ≡ ∼p ∨ ∼q ∨ r.")
def pool3():
    L = [p, q, r, N(p), N(q), N(r)]; out = []
    for x in L:
        for y in L:
            if atoms(x) == atoms(y): continue
            for op in (A_, O_, I_, B_): out.append(op(x, y))
    for x in L:
        for y in L:
            for z in L:
                if len(atoms(x) | atoms(y) | atoms(z)) == 3: out.append(I_(A_(x, y), z)); out.append(O_(A_(x, y), z))
    return out
POOL3 = pool3()
def valor_q(rng):
    a = {k: rng.random() < 0.5 for k in 'pqr'}
    lit = lambda k: V(k) if a[k] else N(V(k))
    if rng.random() < 0.5:
        prem = A_(A_(lit('p'), lit('q')), lit('r')); txt = f"Sabendo que a proposição {show(prem)} é verdadeira, é necessariamente VERDADEIRA a proposição:"
    else:
        ant = A_(lit('p'), lit('q')); cons = N(lit('r')) if True else None
        prem = I_(ant, ('not', lit('r')) if False else (V('r') if not a['r'] else N(V('r'))))
        txt = f"Sabendo que a proposição {show(prem)} é falsa, é necessariamente VERDADEIRA a proposição:"
        assert ev(prem, a) is False
    tr = [f for f in POOL3 if ev(f, a)]; fa = [f for f in POOL3 if not ev(f, a)]
    return mk("Lógica", txt, show(rng.choice(tr)), [show(f) for f in rng.sample(fa, 4)], f"As premissas fixam p = {'V' if a['p'] else 'F'}, q = {'V' if a['q'] else 'F'}, r = {'V' if a['r'] else 'F'}; só a alternativa correta é V nessa valoração.")
def tauto_q(rng):
    T_ = [O_(p, N(p)), I_(A_(p, q), p), I_(p, O_(p, q)), O_(I_(p, q), I_(q, p)), I_(A_(I_(p, q), p), q), N(A_(p, N(p))), I_(A_(I_(p, q), N(q)), N(p))]
    F_ = [I_(p, A_(p, q)), I_(O_(p, q), p), A_(p, N(p)), I_(I_(p, q), p), B_(p, q), A_(O_(p, q), N(q)), I_(I_(p, q), I_(q, p)), O_(p, q)]
    for f in T_: assert all(table(f, ['p', 'q']))
    for f in F_: assert not all(table(f, ['p', 'q']))
    return mk("Lógica", "Qual das proposições é uma TAUTOLOGIA?", show(rng.choice(T_)), [show(f) for f in rng.sample(F_, 4)], "Tautologia é V em todas as linhas da tabela-verdade.")
PAIRS = [("o servidor cai", "o servidor não cai", "o sistema para", "o sistema não para"),
         ("chove", "não chove", "o jogo é adiado", "o jogo não é adiado"),
         ("Ana estuda", "Ana não estuda", "Ana passa na prova", "Ana não passa na prova"),
         ("o código compila", "o código não compila", "os testes passam", "os testes não passam"),
         ("o modelo é treinado", "o modelo não é treinado", "a acurácia melhora", "a acurácia não melhora"),
         ("o backup é feito", "o backup não é feito", "os dados são recuperados", "os dados não são recuperados"),
         ("Rui é bolsista", "Rui não é bolsista", "Rui faz pesquisa", "Rui não faz pesquisa")]
cap = lambda s: s[0].upper() + s[1:]
def neg_cond(rng):
    P, nP, Qx, nQ = rng.choice(PAIRS)
    return mk("Lógica", f"Qual é a negação da proposição: “Se {P}, então {Qx}”?", f"{cap(P)} e {nQ}.",
              [f"Se {nP}, então {nQ}.", f"{cap(nP)} e {Qx}.", f"{cap(nP)} ou {Qx}.", f"Se {Qx}, então {P}.", f"{cap(P)} ou {nQ}."],
              "MANÉ: mantém a primeira, nega a segunda e troca por E. ¬(p → q) ≡ p ∧ ¬q.")
def equiv_cond(rng):
    P, nP, Qx, nQ = rng.choice(PAIRS)
    c = rng.choice([f"Se {nQ}, então {nP}.", f"{cap(nP)} ou {Qx}."])
    return mk("Lógica", f"A proposição “Se {P}, então {Qx}” é logicamente equivalente a:", c,
              [f"Se {Qx}, então {P}.", f"Se {nP}, então {nQ}.", f"{cap(P)} e {Qx}.", f"{cap(P)} ou {nQ}.", f"{cap(P)} e {nQ}."],
              "p → q ≡ ¬q → ¬p (contrapositiva) ≡ ¬p ∨ q. A recíproca (q → p) e a inversa (¬p → ¬q) não são equivalentes.")
def demorgan_nl(rng):
    P, nP, Qx, nQ = rng.choice(PAIRS)
    if rng.random() < 0.5:
        return mk("Lógica", f"Qual é a negação de “{cap(P)} e {Qx}”?", f"{cap(nP)} ou {nQ}.",
                  [f"{cap(nP)} e {nQ}.", f"{cap(nP)} e {Qx}.", f"{cap(P)} ou {Qx}.", f"Se {nP}, então {Qx}."], "De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q.")
    return mk("Lógica", f"Qual é a negação de “{cap(P)} ou {Qx}”?", f"{cap(nP)} e {nQ}.",
              [f"{cap(nP)} ou {nQ}.", f"{cap(P)} e {nQ}.", f"{cap(nP)} ou {Qx}.", f"Se {nP}, então {Qx}."], "De Morgan: ¬(p ∨ q) ≡ ¬p ∧ ¬q.")
QUANT = [("estudante", "recebe bolsa", "não recebe bolsa"), ("servidor", "está online", "não está online"), ("teste", "passa", "não passa"),
         ("candidato", "fez a inscrição", "não fez a inscrição"), ("algoritmo de ordenação", "é estável", "não é estável"), ("programador", "usa Python", "não usa Python")]
def quant_q(rng):
    X, Y, nY = rng.choice(QUANT)
    if rng.random() < 0.6:
        return mk("Lógica", f"A negação de “Todo {X} {Y}” é logicamente equivalente a:", f"Algum {X} {nY}.",
                  [f"Nenhum {X} {Y}.", f"Algum {X} {Y}.", f"Não existe {X} que {Y}.", f"Todo {X} {Y}, exceto um."], "¬∀x P(x) ≡ ∃x ¬P(x): 'nem todo' = 'algum não'.")
    return mk("Lógica", f"A negação de “Algum {X} {Y}” é logicamente equivalente a:", f"Nenhum {X} {Y}.",
              [f"Algum {X} {nY}.", f"Todo {X} {Y}.", f"Pelo menos um {X} {Y}.", f"Nem todo {X} {Y}."], "¬∃x P(x) ≡ ∀x ¬P(x): 'não existe' = 'nenhum'.")
TRIPLES = [("Rui estuda", "Rui não estuda", "Rui passa na prova", "Rui não passa na prova", "Rui recebe bolsa", "Rui não recebe bolsa"),
           ("o servidor cai", "o servidor não cai", "o sistema para", "o sistema não para", "os clientes reclamam", "os clientes não reclamam"),
           ("chove", "não chove", "o jogo é adiado", "o jogo não é adiado", "o estádio fica vazio", "o estádio não fica vazio"),
           ("o código compila", "o código não compila", "os testes rodam", "os testes não rodam", "o deploy é feito", "o deploy não é feito"),
           ("o modelo é treinado", "o modelo não é treinado", "a acurácia melhora", "a acurácia não melhora", "o artigo é publicado", "o artigo não é publicado")]
def arg_q(rng):
    t = rng.choice(TRIPLES); nm = {'a': (t[0], t[1]), 'b': (t[2], t[3]), 'c': (t[4], t[5])}
    a_, b_, c_ = V('a'), V('b'), V('c')
    def txt(f):
        def lit(x): return nm[x[1]][0] if x[0] == 'v' else nm[x[1][1]][1]
        if f[0] == 'imp': return f"Se {lit(f[1])}, então {lit(f[2])}"
        if f[0] == 'or': return f"{cap(lit(f[1]))} ou {lit(f[2])}"
        if f[0] == 'and': return f"{cap(lit(f[1]))} e {lit(f[2])}"
        return cap(lit(f))
    kind = rng.randint(0, 3)
    if kind == 0: prem = [I_(a_, b_), I_(b_, c_)]
    elif kind == 1: prem = [I_(N(a_), b_), I_(b_, c_)]
    elif kind == 2: prem = [O_(a_, b_), I_(b_, c_), N(c_)]
    else: prem = [I_(a_, b_), I_(c_, N(b_))]
    L = [a_, b_, c_, N(a_), N(b_), N(c_)]
    cands = [I_(x, y) for x in L for y in L if atoms(x) != atoms(y)] + [O_(x, y) for x in L for y in L if atoms(x) < atoms(y) or (atoms(x) != atoms(y) and show(x) < show(y))]
    names = ['a', 'b', 'c']
    def valid(cn):
        for vals in itertools.product([True, False], repeat=3):
            asg = dict(zip(names, vals))
            if all(ev(pp, asg) for pp in prem) and not ev(cn, asg): return False
        return True
    good = [cn for cn in cands if valid(cn) and len(atoms(cn)) == 2 and not any(show(cn) == show(pp) for pp in prem)]
    good = [g for g in good if not (atoms(g) == {'a', 'b'} and kind in (0, 1))] or good
    bad = [cn for cn in cands if not valid(cn)]
    c = rng.choice(good)
    ws = rng.sample(bad, 4)
    premtxt = " ".join(f"{['I', 'II', 'III'][i]}. {txt(pp)}." for i, pp in enumerate(prem))
    return mk("Lógica", f"Considere verdadeiras as premissas: {premtxt} Qual conclusão torna o argumento VÁLIDO?", txt(c) + ".", [txt(w) + "." for w in ws],
              "Conferido por tabela-verdade: em toda linha em que as premissas são verdadeiras, a conclusão correta também é. Use silogismo hipotético e contrapositiva.")
LOG = [neg_cond, equiv_cond, demorgan_nl, quant_q, equiv_sym, arg_q]

# ---------------- MONTAGEM ----------------
def letters_balanced(rng, n):
    base = [i % 5 for i in range(n)]; rng.shuffle(base); return base
def finalize(qs, rng):
    pos = letters_balanced(rng, len(qs)); out = []
    for q, k in zip(qs, pos):
        ws = q["wrongs"][:]
        rng.shuffle(ws)
        if len(ws) < 4: ws = genfill(q["correct"], ws, rng)
        if len(ws) < 4: raise RuntimeError("distratores insuficientes: " + q["stem"] + " | " + str(q["correct"]) + " | " + str(ws))
        opts = ws[:4]; opts.insert(k, q["correct"])
        assert len(set(opts)) == 5, opts
        out.append(dict(bloco=q["bloco"], stem=q["stem"], code=q["code"], opts=opts, ans=k, why=q["why"]))
    return out
SIMS = []
master = random.Random(20270204)
SEEN = set()
U = {k: set() for k in ['py','edc','edk','bu','orc','ork']}
for si, name in enumerate("ABCDE"):
    rng = random.Random(1000 + si * 77)
    def fresh(gen):
        for _ in range(25):
            q = gen(); key = (q["stem"], q["code"])
            if key not in SEEN: SEEN.add(key); return q
        return None
    def pick(templates, k, used):
        idx = [i for i in range(len(templates)) if i not in used]
        if len(idx) < k: used.clear(); idx = list(range(len(templates)))
        rng.shuffle(idx); out = []
        for i in idx + [j for j in range(len(templates)) if j not in idx]:
            if len(out) == k: break
            q = fresh(templates[i])
            if q: out.append(q); used.add(i)
        assert len(out) == k, "sem questões novas suficientes"
        return out
    pyT, edT, buT, orT = py_templates(rng), ed_templates(rng), busca_templates(rng), ord_templates(rng)
    qs = pick(pyT, 8, U['py'])
    qs += pick(edT[:10], 3, U['edc']) + pick(edT[10:], 3, U['edk'])
    qs += [fresh(buT[0]), fresh(buT[1])] if si % 2 == 0 else [fresh(buT[2]), fresh(buT[rng.choice([0, 1])])]
    qs += pick(buT[3:], 2, U['bu'])
    qs += pick(orT[:5], 3, U['orc']) + pick(orT[5:], 2, U['ork'])
    extra = [valor_q, tauto_q, export_q][si % 3]
    lq = [fresh(lambda f=f: f(rng)) for f in LOG] + [fresh(lambda: extra(rng)) or fresh(lambda: valor_q(rng))]
    rng.shuffle(lq); qs += lq[:7]
    esp = finalize(qs, rng)
    sim = dict(id=name, esp=esp)
    if name != "A":
        tx = TEXTS[si - 1]; pos = letters_balanced(rng, 10); en = []
        for (stem, corr, wr, why), k in zip(tx["qs"], pos):
            w = wr[:]; rng.shuffle(w); w.insert(k, corr); en.append(dict(stem=stem, opts=w, ans=k, why=why))
        sim["en"] = dict(title=tx["title"], paras=tx["paras"], qs=en)
    SIMS.append(sim)
json.dump(SIMS, open(sys.argv[2], "w"), ensure_ascii=False)
for s in SIMS:
    from collections import Counter
    c = Counter(q["bloco"] for q in s["esp"]); L = Counter("ABCDE"[q["ans"]] for q in s["esp"] + s.get("en", {}).get("qs", []))
    print(s["id"], len(s["esp"]), dict(c), "letras:", dict(sorted(L.items())))
