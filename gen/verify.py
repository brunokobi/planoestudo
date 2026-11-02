import json,sys,io,contextlib,itertools,re
S=json.load(open(sys.argv[1]))
bad=0;nc=0;nl=0
def tok(s): return re.findall(r'[pqr]|∼|∧|∨|→|↔|\(|\)',s)
def parse(s):
    t=tok(s);i=[0]
    def peek(): return t[i[0]] if i[0]<len(t) else None
    def nxt(): i[0]+=1; return t[i[0]-1]
    def atom():
        x=nxt()
        if x=='∼': a=atom(); return lambda e:not a(e)
        if x=='(':
            v=expr(); nxt(); return v
        return lambda e,x=x:e[x]
    def expr():
        a=atom()
        while peek() in ('∧','∨','→','↔'):
            op=nxt(); b=atom()
            a={'∧':lambda e,a=a,b=b:a(e) and b(e),'∨':lambda e,a=a,b=b:a(e) or b(e),'→':lambda e,a=a,b=b:(not a(e)) or b(e),'↔':lambda e,a=a,b=b:a(e)==b(e)}[op]
        return a
    return expr()
def tt(f): return tuple(f(dict(zip('pqr',v))) for v in itertools.product([True,False],repeat=3))
for s in S:
  for i,q in enumerate(s['esp']):
    if len(set(q['opts']))!=5: print('dup opts',s['id'],i);bad+=1
    if q['code'] and q['stem'].startswith(('Qual','O que','A função','Quantas')) and 'quicksort' not in q['code'] and '# ...' not in q['code']:
      b=io.StringIO()
      with contextlib.redirect_stdout(b): exec(q['code'],{})
      out=b.getvalue().strip(); nc+=1
      if q['opts'][q['ans']]!=out or q['opts'].count(out)!=1: print('ERRO código',s['id'],i);bad+=1
    st=q['stem']
    m=re.search(r'equivalente a\s+(.+?)\s*\?$',st) or re.search(r'A fórmula (.+) é equivalente a:',st)
    if q['bloco']=='Lógica' and m:
      nl+=1;T=tt(parse(m.group(1)));oks=[k for k,o in enumerate(q['opts']) if tt(parse(o))==T]
      if oks!=[q['ans']]: print('ERRO equiv',s['id'],i);bad+=1
    if 'TAUTOLOGIA' in st:
      nl+=1;oks=[k for k,o in enumerate(q['opts']) if all(tt(parse(o)))]
      if oks!=[q['ans']]: print('ERRO taut',s['id'],i);bad+=1
    m2=re.search(r'proposição (.+) é (verdadeira|falsa), é necessariamente',st)
    if m2:
      nl+=1;P=parse(m2.group(1));want=m2.group(2)=='verdadeira'
      envs=[dict(zip('pqr',v)) for v in itertools.product([True,False],repeat=3) if P(dict(zip('pqr',v)))==want]
      oks=[k for k,o in enumerate(q['opts']) if all(parse(o)(e) for e in envs)]
      if oks!=[q['ans']]: print('ERRO valor',s['id'],i);bad+=1
print('código checado:',nc,'| lógica simbólica checada:',nl,'| problemas:',bad)
