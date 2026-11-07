(function(){
"use strict";
var DATA = window.DATA, DAYS = DATA.days, T = DATA.topics, ARTS = DATA.arts, WEEKS = DATA.weeks;
var PAGE = document.body.getAttribute("data-page") || "home";
var app = document.getElementById("app");
var KEY = "ppcomp2027-agenda", st = {};
try { st = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch(e) { st = {}; }
function save(){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch(e) {} }
function esc(s){ return String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function pad(n){ return String(n).padStart(2,"0"); }
var KIND = {estudo:"Conteúdo novo", pratica:"Prática", simulado:"Simulado", revisao:"Revisão", leve:"Leve", livre:"Livre", admin:"Tarefas do edital", prova:"Prova"};
var firstDay = {}; DAYS.forEach(function(d){ if(d.topic && !firstDay[d.topic]) firstDay[d.topic] = d; });
var byWeek = {}; DAYS.forEach(function(d){ (byWeek[d.wk] = byWeek[d.wk] || []).push(d); });
function weekFile(w){ return "semana-"+pad(w)+".html"; }
function dayHref(d){ return weekFile(d.wk)+"#dia-"+d.id; }
var HOME = "inicio.html";
function todayISO(){ var n = new Date(); return n.getFullYear()+"-"+pad(n.getMonth()+1)+"-"+pad(n.getDate()); }
function todayDay(){ var t = todayISO(); for (var i=0;i<DAYS.length;i++) if (DAYS[i].id >= t) return DAYS[i]; return DAYS[DAYS.length-1]; }
function chk(id, label){ return '<label class="check"><input type="checkbox" data-k="'+esc(id)+'"'+(st[id]?" checked":"")+'><span>'+label+'</span></label>'; }
function pbar(done, tot, unit){ var p = tot ? Math.round(100*done/tot) : 0;
  return '<div class="progress"><span>'+p+'%</span><div class="track"><div class="fill" style="width:'+p+'%"></div></div><span>'+done+'/'+tot+' '+unit+'</span></div>'; }

/* ---------- navegação comum (abas principais) ---------- */
function nav(){
  var td = todayDay();
  function t(href, label, page){ return '<a class="'+(PAGE===page?"here":"")+'" href="'+href+'"'+(PAGE===page?' aria-current="page"':'')+'>'+label+'</a>'; }
  document.getElementById("top").innerHTML = '<div class="in"><a class="brand" href="'+HOME+'">Agenda PPComp 2027<small>Preparação pessoal · seleção Ifes Serra</small></a>'+
    '<nav class="maintabs" aria-label="Principal">'+
    t("analise.html","Análise da prova","analise")+t(HOME,"Plano de estudo","home")+t("mapa.html","Mapa mental","mapa")+t(weekFile(td.wk),"Semanas","semana")+
    t("simulados.html","Simulados","simulados")+t("ingles.html","Inglês","ingles")+t("temas.html","Temas","temas")+t("tecnicas.html","Técnicas","tecnicas")+
    '<a class="today" href="'+dayHref(td)+'">Hoje · '+td.dm+'</a></nav></div>';
}
/* ---------- abas genéricas ---------- */
var TABGROUPS = {};
function tabs(group, items, def){
  TABGROUPS[group] = items.map(function(i){return i.key;});
  var h = location.hash.replace("#",""), act = null;
  if (TABGROUPS[group].indexOf(h) >= 0) act = h;
  else if (def && TABGROUPS[group].indexOf(def) >= 0) act = def;
  else if (st["tab:"+group] && TABGROUPS[group].indexOf(st["tab:"+group]) >= 0) act = st["tab:"+group];
  else act = items[0].key;
  var bar = '<div class="tabbar" role="tablist" aria-label="'+esc(group)+'">'+items.map(function(i){
    return '<button type="button" class="tab'+(i.cls?" "+i.cls:"")+'" role="tab" id="tb-'+i.key+'" aria-controls="'+i.key+'" aria-selected="'+(i.key===act)+'" data-tg="'+esc(group)+'" data-tk="'+i.key+'">'+i.label+'</button>'; }).join("")+'</div>';
  var panels = items.map(function(i){ return '<div class="tabpanel" role="tabpanel" id="'+i.key+'" aria-labelledby="tb-'+i.key+'" data-tg="'+esc(group)+'"'+(i.key===act?'':' hidden')+'>'+i.html+'</div>'; }).join("");
  return '<section>'+bar+'</section>'+panels;
}
function activate(group, key, push){
  document.querySelectorAll('[data-tg="'+group+'"]').forEach(function(el){
    if (el.getAttribute("role")==="tab") el.setAttribute("aria-selected", String(el.getAttribute("data-tk")===key));
    else el.hidden = el.id !== key;
  });
  st["tab:"+group] = key; save();
  if (push) { try { history.replaceState(null, "", "#"+key); } catch(e) {} }
}

/* ---------- blocos reutilizáveis ---------- */
function exHTML(e, key, label){
  return '<div class="ex">'+chk(key, '<b>'+esc(label)+'.</b> '+esc(e.q))+(e.code?'<pre>'+esc(e.code)+'</pre>':'')+
    '<details><summary>Ver resposta</summary><div class="ans">'+(e.code?'<pre>'+esc(e.a)+'</pre>':'<p><b>'+esc(e.a)+'</b></p>')+(e.why?'<p class="small muted">'+esc(e.why)+'</p>':'')+'</div></details></div>';
}
function isWeekend(d){ return d && (d.wd === "Sáb" || d.wd === "Dom"); }
function timeline(d){
  var we = isWeekend(d), conteudo = !d || d.kind === "estudo";
  if (conteudo && !we) return '<div class="timeline">'+
    '<div><b>0–10 min</b>Aquecimento: Anki e revisões espaçadas de hoje</div>'+
    '<div><b>10–15</b>Pré-teste: tente o exercício 1 antes de estudar</div>'+
    '<div><b>15–50</b>Conteúdo: tópicos e leitura indicada no livro</div>'+
    '<div><b>50–85</b>Exercícios 1 a 4 no papel; depois confira as respostas</div>'+
    '<div><b>85–95</b>Memorização: crie 3 a 5 flashcards e repita os mnemônicos</div>'+
    '<div><b>95–100</b>Blurting e Feynman: escreva e explique o que lembra</div>'+
    '<div><b>100–120</b>Inglês (20 min): a tarefa da seção Inglês do dia</div></div>';
  if (conteudo && we) return '<div class="timeline">'+
    '<div><b>0–10 min</b>Aquecimento: Anki e revisões espaçadas de hoje</div>'+
    '<div><b>10–15</b>Pré-teste: tente o exercício 1 antes de estudar</div>'+
    '<div><b>15–65</b>Conteúdo: tópicos e leitura indicada no livro</div>'+
    '<div><b>65–115</b>Exercícios do dia e de revisão, no papel</div>'+
    '<div><b>115–125</b>Pausa</div>'+
    '<div><b>125–170</b>Questões reais das provas sobre o tema e tarefas do dia</div>'+
    '<div><b>170–180</b>Flashcards, blurting e Feynman</div>'+
    '<div><b>180–240</b>Inglês (1h): a tarefa da seção Inglês do dia</div></div>';
  if (d.kind === "simulado" && d.ing && d.ing.indexOf("incluído") >= 0) return '<div class="timeline"><div><b>0–150 min</b>Simulado completo, com o Inglês incluído</div><div><b>150–160</b>Pausa</div><div><b>160–240</b>Correção e caderno de erros</div></div>';
  if (d.kind === "livre" || d.kind === "leve" || d.kind === "prova") return "";
  return we ? '<div class="timeline"><div><b>0–180 min</b>Específicas: tarefas, questões e exercícios abaixo (pausa de 10 min a cada hora)</div><div><b>180–240</b>Inglês (1h): a tarefa da seção Inglês do dia</div></div>'
            : '<div class="timeline"><div><b>0–100 min</b>Específicas: tarefas, questões e exercícios abaixo</div><div><b>100–120</b>Inglês (20 min): a tarefa da seção Inglês do dia</div></div>';
}
var PQ = {}; (DATA.prov ? DATA.prov.quizzes : []).forEach(function(q){ PQ[q.url] = q.id; });
function artItem(a){
  var cls = a.pri==="Máxima"?"simulado":a.pri==="Alta"?"pratica":"estudo";
  return '<li class="ex">'+chk(a.id, '<span class="pill p-'+cls+'">'+esc(a.pri)+'</span> <a href="'+esc(a.url)+'" target="_blank" rel="noopener"><b>'+esc(a.title)+'</b></a> <span class="small muted">· MIT News, '+esc(a.dt)+'/2026'+(a.score?' · nota '+a.score+'/100, '+a.pos+'º lugar':'')+'</span>')+
    '<p class="small muted" style="padding-left:30px">Análise: '+esc(a.why)+(PQ[a.url]?' <a href="ingles.html#'+PQ[a.url]+'">Fazer as 10 questões prováveis →</a>':'')+'</p></li>';
}
function dayBody(d){
  var tp = d.topic ? T[d.topic] : null, h = [];
  if (d.edital) h.push('<div class="alert">Edital: '+esc(d.edital)+'</div>');
  if (d.rev.length) h.push('<section><div class="eyebrow">Revisão espaçada (aquecimento, 10 min)</div><ul class="tasks">'+d.rev.map(function(r){var t=T[r.topic], fd=firstDay[r.topic];
      return '<li>'+chk("rev:"+d.id+":"+r.topic, 'Revisar <a href="'+dayHref(fd)+'">'+esc(t.titulo)+'</a> (revisão de '+r.k+' dia'+(r.k>1?'s':'')+'): refazer os exercícios 1 e 3 sem olhar e passar os flashcards')+'</li>';}).join("")+'</ul></section>');
  var tl = timeline(d); if (tl) h.push('<section><div class="eyebrow">Roteiro do dia · '+esc(d.dur)+'</div>'+tl+'</section>');
  if (tp){
    h.push('<section><div class="eyebrow">Conteúdo · '+esc(tp.bloco)+'</div><h2>'+esc(tp.titulo)+'</h2><div class="grid2">'+
      '<div class="card"><h3>O que estudar</h3><ul>'+tp.conteudo.map(function(c){return '<li>'+esc(c)+'</li>';}).join("")+'</ul></div>'+
      '<div class="card"><h3>Para memorizar</h3><ul>'+tp.memo.map(function(c){return '<li>'+esc(c)+'</li>';}).join("")+'</ul></div></div>'+
      '<ul class="tasks"><li>'+chk("c:"+d.id+":ler",'Leitura: '+esc(tp.leitura))+'</li>'+
      '<li>'+chk("c:"+d.id+":cards",'Criar 3 a 5 flashcards no Anki com os itens de "Para memorizar"')+'</li>'+
      '<li>'+chk("c:"+d.id+":blurt",'Blurting: escrever de memória o que lembra do tema e conferir')+'</li></ul></section>');
    h.push('<section><div class="eyebrow">Exercícios do dia</div><p class="small muted">Resolva no papel; para código, faça o teste de mesa. O 1º é o pré-teste.</p><div class="card">'+
      tp.ex.slice(0,4).map(function(e,j){return exHTML(e,"ex:"+tp.id+":"+j,"Exercício "+(j+1)+(j===0?" (pré-teste)":""));}).join("")+'</div>'+
      (tp.provas?'<ul class="tasks"><li>'+chk("pv:"+d.id,'Questões reais sobre este tema: '+esc(tp.provas))+'</li></ul>':'')+'</section>');
  }
  if (d.provas) h.push('<section><div class="eyebrow">Questões das provas antigas</div><ul class="tasks"><li>'+chk("pv:"+d.id, esc(d.provas))+'</li></ul><p class="small muted">Os PDFs estão em MESTRADO/provas. Use 3 min por questão e corrija com o gabarito.</p></section>');
  if (d.reserve.length) h.push('<section><div class="eyebrow">Exercícios de revisão (intercalados)</div><div class="card">'+
      d.reserve.map(function(r){var t=T[r]; return exHTML(t.ex[4],"rx:"+d.id+":"+r, t.titulo);}).join("")+'</div></section>');
  if (d.tasks.length) h.push('<section><div class="eyebrow">Tarefas de Específicas</div><ul class="tasks">'+d.tasks.map(function(x,j){return '<li>'+chk("t:"+d.id+":"+j, esc(x))+'</li>';}).join("")+'</ul></section>');
  if (d.ing) {
    var wa = ARTS.filter(function(a){ return a.wk === d.wk; }), showA = wa.length && /artigo/.test(d.ing);
    h.push('<section><div class="eyebrow">Inglês do dia</div><ul class="tasks"><li>'+chk("ing:"+d.id, esc(d.ing))+'</li></ul>'+
      (showA?'<div class="card"><b>Artigos da semana '+d.wk+'</b><ul class="tasks">'+wa.map(artItem).join("")+'</ul></div>':'')+
      '<p class="small muted">Método, vocabulário e textos de treino na <a href="ingles.html">página de Inglês</a>.</p></section>');
  }
  if (SIMDAY[d.id]) h.push('<div><a class="btn primary" href="simulados.html#sim-'+SIMDAY[d.id].toLowerCase()+'">Abrir o Simulado '+SIMDAY[d.id]+' →</a></div>');
  h.push('<div class="daydone">'+chk("day:"+d.id, 'Concluí o dia '+d.dm)+'</div>');
  return h.join("");
}

/* ---------- Mapa mental ---------- */
var MAP = {
  left: [
    {name:"Lógica · ~7 q", color:"--vio", leaves:[["L1","Conectivos e tabela-verdade"],["L2","Condicional e contrapositiva"],["L3","Negações (MANÉ)"],["L4","De Morgan, ↔, exportação"],["L5","Valor lógico por premissas"],["L6","Todo / algum / nenhum"],["L7","Argumentos e silogismos"]]},
    {name:"Python · ~8 q", color:"--pen", leaves:[["P1","Operadores e and/or"],["P2","Strings e fatiamento"],["P3","Listas e range"],["P4","Teste de mesa (loops)"],["P5","for-else, break"],["P6","Funções e escopo"],["P7","Mutabilidade"],["P8","Recursão I"],["P9","Recursão II"],["P10","Matrizes"]]},
    {name:"Inglês · 10 q (mín. 5)", color:"--ok", leaves:[["@ingles.html","1 texto sobre pesquisa em IA"],["@ingles.html#tipos","Perguntas na ordem do texto"],["@ingles.html#artigos","'+ARTS.length+' artigos prováveis"]]}
  ],
  right: [
    {name:"Estruturas de dados · ~6 q", color:"--warn", leaves:[["E1","Pilha: operações"],["E2","Pilha: balanceamento, pós-fixa"],["E3","Fila, circular, deque"],["E4","Lista encadeada"],["E5","Hash, dict, set"],["E6","Heap / heapq"],["E7","BST: inserção e busca"],["E8","Percursos e altura"],["C2","Custo das operações"]]},
    {name:"Busca · ~4 q", color:"--hot", leaves:[["G1","Grafos: representação"],["G2","BFS (fila)"],["G3","DFS (pilha)"],["B1","Busca binária e sequencial"]]},
    {name:"Ordenação · ~5 q", color:"--hot", leaves:[["O1","Bubble"],["O2","Selection"],["O3","Insertion"],["O4","Merge"],["O5","Quick"],["O6","Heap, counting, estabilidade"],["C1","Notação O e complexidade"]]},
    {name:"Currículo · até 40 pts", color:"--ok", leaves:[["@analise.html#curriculo","Experiência: 2 pts/ano (máx. 8)"],["@analise.html#curriculo","Anexo III: 2 PDFs"],["@analise.html#curriculo","Envio em 05/02"]]}
  ]
};
function mindmap(){
  var W=1500, LH=26, GAP=22, cx=W/2, CH=8.4;
  function sideH(s){ return s.reduce(function(a,b){return a+b.leaves.length*LH+GAP;},0)-GAP; }
  var H = Math.max(sideH(MAP.left), sideH(MAP.right)) + 48, cy = H/2;
  var out = ['<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Mapa mental do conteúdo da prova">'];
  function side(list, dir){
    var y0 = (H - sideH(list))/2;
    list.forEach(function(b){
      var n=b.leaves.length, top=y0, mid=top+n*LH/2, col="var("+b.color+")";
      var bw = Math.round(b.name.length*CH+28), inner = cx+dir*175, outer = inner+dir*bw, lx = outer+dir*70;
      out.push('<path class="mm-line" stroke="'+col+'" d="M'+(cx+dir*120)+','+cy+' C'+(cx+dir*150)+','+cy+' '+(inner-dir*40)+','+mid+' '+inner+','+mid+'"/>');
      b.leaves.forEach(function(l,i){
        var ly = top+i*LH+LH/2, done = T[l[0]] && firstDay[l[0]] && st["day:"+firstDay[l[0]].id];
        out.push('<path class="mm-line" stroke="'+col+'" stroke-opacity=".45" d="M'+outer+','+mid+' C'+(outer+dir*40)+','+mid+' '+(lx-dir*40)+','+ly+' '+lx+','+ly+'"/>');
        out.push('<circle cx="'+lx+'" cy="'+ly+'" r="5.5" fill="'+(done?col:"var(--sheet)")+'" stroke="'+col+'" stroke-width="2"/>');
        var href = l[0].charAt(0)==="@" ? l[0].slice(1) : (firstDay[l[0]] ? dayHref(firstDay[l[0]]) : HOME);
        var code = l[0].charAt(0)==="@" ? "" : '<tspan class="mm-code">'+esc(l[0])+'</tspan> ';
        out.push('<a href="'+href+'"><title>'+esc(l[1])+(done?" (concluído)":"")+'</title><text class="mm-leaf" x="'+(lx+dir*12)+'" y="'+(ly+4.5)+'" text-anchor="'+(dir>0?"start":"end")+'">'+(dir>0?code+esc(l[1]):esc(l[1])+' '+code.replace('</tspan> ','</tspan>'))+'</text></a>');
      });
      var rx = dir>0?inner:outer;
      out.push('<rect x="'+rx+'" y="'+(mid-17)+'" width="'+bw+'" height="34" rx="17" fill="var(--sheet)" stroke="'+col+'" stroke-width="2"/>');
      out.push('<text class="mm-branch" fill="'+col+'" x="'+(rx+bw/2)+'" y="'+(mid+5)+'" text-anchor="middle">'+esc(b.name)+'</text>');
      y0 += n*LH+GAP;
    });
  }
  side(MAP.left,-1); side(MAP.right,1);
  out.push('<rect x="'+(cx-120)+'" y="'+(cy-34)+'" width="240" height="68" rx="34" fill="var(--ink)"/>');
  out.push('<text class="mm-center" x="'+cx+'" y="'+(cy-5)+'" text-anchor="middle">Prova 04/02/2027</text>');
  out.push('<text x="'+cx+'" y="'+(cy+17)+'" text-anchor="middle" style="font:12px var(--f-mono);fill:var(--sheet)">10 inglês + 30 específicas</text></svg>');
  return out.join("");
}
var MAPNOTE = '<p class="muted">Quantidade de questões por bloco projetada para 30 específicas, a partir das provas de 2025. A bolinha fica cheia quando você conclui o dia do assunto. Clique num assunto para abrir o dia de estudo.</p>';
function mapBox(){ return '<div class="mapbox">'+mindmap()+'</div><p class="small muted maphint">No celular, arraste o mapa para o lado.</p>'; }
/* mapa detalhado de um bloco: raiz → temas → o que estudar + gancho de memória */
function blocoMap(bloco, color){
  var ids = Object.keys(T).filter(function(i){return T[i].bloco===bloco;});
  var dn = ids.filter(function(i){return firstDay[i] && st["day:"+firstDay[i].id];}).length;
  return '<div class="bmap" style="--c:var('+color+')"><div class="broot"><b>'+esc(bloco)+'</b><span>'+dn+'/'+ids.length+' temas concluídos</span></div><div class="bbranches">'+
    ids.map(function(i){ var tp=T[i], fd=firstDay[i], done = fd && st["day:"+fd.id];
      return '<div class="bbr'+(done?" done":"")+'"><a class="btopic" href="'+(fd?dayHref(fd):"temas.html")+'"><span class="dt">'+i+'</span>'+esc(tp.titulo)+(fd?'<small>'+fd.dm+'</small>':'')+'</a>'+
        '<ul class="bleaves">'+tp.conteudo.map(function(c){return '<li>'+esc(c)+'</li>';}).join("")+'</ul>'+
        (tp.memo&&tp.memo[0]?'<p class="bmemo"><b>Gancho:</b> '+esc(tp.memo[0])+'</p>':'')+'</div>';
    }).join("")+'</div></div>';
}
function mapa(){
  var B = [["Python","--pen","python"],["Estruturas de Dados","--warn","ed"],["Busca","--hot","busca"],["Ordenação","--hot","ordenacao"],["Lógica","--vio","logica"]];
  return '<section><div class="eyebrow">Tudo o que cai, num lugar só</div><h1>Mapa mental</h1><p class="muted">A visão geral mostra os blocos e os temas da prova. Cada aba de bloco abre o mapa detalhado, com o que estudar e o gancho de memória de cada tema. Para revisar, cubra os ramos e tente lembrar o conteúdo antes de olhar.</p></section>'+
  tabs("mapa", [{key:"geral", label:"Visão geral", html:MAPNOTE+mapBox()}].concat(B.map(function(b){ return {key:"m-"+b[2], label:b[0], html:blocoMap(b[0], b[1])}; })), "geral");
}

/* ---------- Página: plano de estudo (início) ---------- */
function home(){
  var exam = new Date(2027,1,4,19), days = Math.max(0, Math.ceil((exam - new Date())/86400000));
  var dc = DAYS.filter(function(d){ return st["day:"+d.id]; }).length, td = todayDay(), t = todayISO();
  var cal = WEEKS.map(function(w){
    var cells = new Array(7).fill(null);
    (byWeek[w.n]||[]).forEach(function(d){ cells[(new Date(d.id+"T12:00:00").getDay()+6)%7] = d; });
    return '<div class="wk"><a class="lab" href="'+weekFile(w.n)+'">Semana '+w.n+' ›</a><div class="days">'+cells.map(function(d){
      if(!d) return '<span class="chip empty" aria-hidden="true"></span>';
      return '<a class="chip k-'+d.kind+(st["day:"+d.id]?" done":"")+(d.id===t?" today":"")+'" href="'+dayHref(d)+'" title="'+esc(d.title)+'"><span class="dt">'+d.wd+' '+d.dm+'</span><span class="tt">'+esc(d.title)+'</span></a>';
    }).join("")+'</div></div>';
  }).join("");
  var wl = WEEKS.map(function(w){ var ds = byWeek[w.n]||[], dn = ds.filter(function(d){return st["day:"+d.id];}).length;
    return '<a class="card" style="text-decoration:none;color:inherit" href="'+weekFile(w.n)+'"><div class="eyebrow">Semana '+w.n+' · '+esc(w.range)+'</div><h3>'+esc(w.title)+'</h3><p class="small muted">'+esc(w.cp)+'</p>'+pbar(dn, ds.length, "dias")+'</a>'; }).join("");
  var head = '<section><div class="eyebrow">Plano de estudo · 03/11/2026 a 05/02/2027</div><h1>Plano de estudo</h1>'+
    '<div class="facts"><div class="fact"><b>'+days+'</b><span>dias até a prova (04/02, à noite)</span></div>'+
    '<div class="fact"><b>'+dc+'/'+DAYS.length+'</b><span>dias concluídos</span></div>'+
    '<div class="fact"><b>Semana '+td.wk+'</b><span>'+esc(WEEKS[td.wk-1].title)+'</span></div>'+
    '<div class="fact"><b>18h/semana</b><span>Seg a sex: 2h (1h40 de Específicas + 20 min de Inglês). Sáb e dom: 4h (3h + 1h de Inglês).</span></div></div>'+pbar(dc, DAYS.length, "dias")+'</section>';
  var hoje = '<div class="panelhead"><div class="eyebrow">'+td.wd+' '+td.dm+' · semana '+td.wk+'</div><h2>'+esc(td.title)+'</h2><div class="meta"><span class="pill p-'+td.kind+'">'+KIND[td.kind]+'</span><span>'+esc(td.dur)+'</span></div>'+
    '<div class="nav"><a class="btn primary" href="'+dayHref(td)+'">Abrir na página da semana →</a></div></div>'+dayBody(td);
  var mm = '<section><div class="sechead"><h2>Mapa mental</h2><a class="btn" href="mapa.html">Mapas detalhados por bloco →</a></div>'+MAPNOTE+mapBox()+'</section>';
  return head + mm + tabs("plano", [
    {key:"hoje", label:"Hoje", html:hoje},
    {key:"semanas", label:"Semanas", html:'<div class="grid2">'+wl+'</div>'},
    {key:"calendario", label:"Calendário", html:'<div class="legend"><span><i style="background:var(--pen)"></i>Conteúdo novo</span><span><i style="background:var(--warn)"></i>Prática</span><span><i style="background:var(--vio)"></i>Revisão</span><span><i style="background:var(--hot)"></i>Simulado / prova</span><span><i style="background:var(--ok)"></i>Tarefas do edital</span><span><i style="background:var(--line)"></i>Leve / livre</span></div><div class="cal">'+cal+'</div>'}
  ], "hoje");
}

/* ---------- Página: análise da prova ---------- */
function analise(){
  var A = DATA.analise;
  return '<section><div class="eyebrow">Edital 25/2026 · provas de 2022 a 2025</div><h1>Análise da prova</h1><p class="muted">O que o edital pede, o que a banca costuma cobrar e a previsão para 04/02/2027, tirada das 5 provas anteriores.</p></section>'+
  tabs("analise", [
    {key:"resumo", label:"Resumo", html:A.resumo.replace(/id="countdown">[^<]*/, 'id="countdown">'+Math.max(0, Math.ceil((new Date(2027,1,4,19) - new Date())/86400000))+" dias")},
    {key:"metodo", label:"Método de previsão", html:A.metodo},
    {key:"ranking", label:"Ranking de temas", html:A.ranking},
    {key:"prova", label:"Prova provável", html:A.prova},
    {key:"pegadinhas", label:"Pegadinhas", html:A.pegadinhas},
    {key:"diad", label:"Dia da prova", html:A.diad},
    {key:"curriculo", label:"Currículo", html:A.curriculo+'<div class="card"><b>No plano</b><p>O dossiê é montado em 17/12 e 20/12 (<a href="'+weekFile(7)+'">semana 7</a>) e enviado em 05/02.</p></div>'},
    {key:"pasta", label:"Provas na pasta", html:A.pasta}
  ]);
}

/* ---------- Página: semana (uma aba por dia) ---------- */
function semana(){
  var n = +document.body.getAttribute("data-week"), w = WEEKS[n-1], ds = byWeek[n] || [];
  var dn = ds.filter(function(d){return st["day:"+d.id];}).length, td = todayISO();
  var def = (ds.filter(function(d){return d.id===td;})[0] || ds.filter(function(d){return !st["day:"+d.id];})[0] || ds[0]);
  var topics = ds.filter(function(d){return d.topic;}).map(function(d){return T[d.topic].titulo;});
  var wsel = '<select class="btn" id="weeksel" aria-label="Ir para outra semana">'+WEEKS.map(function(x){ return '<option value="'+weekFile(x.n)+'"'+(x.n===n?" selected":"")+'>Semana '+x.n+' · '+esc(x.range)+'</option>'; }).join("")+'</select>';
  var h = '<nav class="pager" aria-label="Semanas">'+(n>1?'<a class="btn" href="'+weekFile(n-1)+'">← Semana '+(n-1)+'</a>':'<span></span>')+wsel+(n<WEEKS.length?'<a class="btn" href="'+weekFile(n+1)+'">Semana '+(n+1)+' →</a>':'<span></span>')+'</nav>'+
    '<section><div class="eyebrow">Semana '+n+' de '+WEEKS.length+' · '+esc(w.range)+'</div><h1>'+esc(w.title)+'</h1>'+
    (topics.length?'<p class="muted">Conteúdo novo: '+esc(topics.join(" · "))+'.</p>':'')+
    (w.cp?'<div class="card"><b>Checkpoint da semana</b><p>'+esc(w.cp)+'</p></div>':'')+pbar(dn, ds.length, "dias")+'</section>';
  h += tabs("semana-"+n, ds.map(function(d){
    return {key:"dia-"+d.id, cls:(st["day:"+d.id]?"done":"")+(d.id===td?" istoday":""), label:d.wd+' '+d.dm+'<small>'+esc(KIND[d.kind])+'</small>',
      html:'<div class="panelhead"><h2>'+esc(d.title)+'</h2><div class="meta"><span class="pill p-'+d.kind+'">'+KIND[d.kind]+'</span><span>'+d.wd+' '+d.dm+'</span><span>· '+esc(d.dur)+'</span>'+(d.topic?'<span>· '+esc(T[d.topic].bloco)+'</span>':'')+'</div></div>'+dayBody(d)};
  }), "dia-"+def.id);
  h += '<nav class="pager" aria-label="Semanas">'+(n>1?'<a class="btn" href="'+weekFile(n-1)+'">← Semana anterior</a>':'<span></span>')+(n<WEEKS.length?'<a class="btn primary" href="'+weekFile(n+1)+'">Próxima semana →</a>':'<span></span>')+'</nav>';
  return h;
}

/* ---------- Página: temas (uma aba por bloco) ---------- */
function temas(){
  var blocos = ["Lógica","Python","Estruturas de Dados","Busca","Ordenação"], ids = Object.keys(T);
  return '<section><div class="eyebrow">Banco de conteúdo</div><h1>Temas para revisão</h1><p class="muted">Os 31 temas com conteúdo, memorização e os 5 exercícios de cada um. Use esta página nas revisões espaçadas e na reta final. O que você marcar aqui também aparece marcado nos dias de estudo.</p></section>'+
  tabs("temas", blocos.map(function(b){
    var list = ids.filter(function(i){return T[i].bloco===b;});
    return {key:"b-"+b.replace(/ /g,"-").normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase(), label:b+'<small>'+list.length+' temas</small>', html:list.map(function(i){ var tp=T[i], fd=firstDay[i];
      return '<details class="day"><summary><span class="dt">'+i+'</span><span class="tt">'+esc(tp.titulo)+'</span>'+(fd?'<span class="small muted">estudado em '+fd.dm+'</span>':'')+'</summary><div class="body">'+
        '<div class="grid2"><div class="card"><h3>O que estudar</h3><ul>'+tp.conteudo.map(function(c){return '<li>'+esc(c)+'</li>';}).join("")+'</ul><p class="small muted">Leitura: '+esc(tp.leitura)+'</p></div>'+
        '<div class="card"><h3>Para memorizar</h3><ul>'+tp.memo.map(function(c){return '<li>'+esc(c)+'</li>';}).join("")+'</ul>'+(tp.provas?'<p class="small muted">Nas provas: '+esc(tp.provas)+'</p>':'')+'</div></div>'+
        '<div class="card">'+tp.ex.map(function(e,j){return exHTML(e,"ex:"+i+":"+j,"Exercício "+(j+1));}).join("")+'</div>'+
        (fd?'<a class="btn" href="'+dayHref(fd)+'">Abrir o dia deste tema →</a>':'')+'</div></details>'; }).join("")};
  }));
}

/* ---------- Página: técnicas ---------- */
function tecnicas(){
  var C = [
    ["Recuperação ativa (efeito de teste)","Lembrar é o que fixa, reler não. Todo dia termina com 5 min de blurting: numa folha em branco, escreva tudo o que lembra do tema. Depois confira e complete com outra cor.","Último bloco de todo dia de conteúdo"],
    ["Repetição espaçada 1-3-7-14-30","Cada tema volta 1, 3, 7, 14 e 30 dias depois do primeiro estudo. A agenda já agenda isso: o bloco 'Revisão espaçada' de cada dia mostra o que vence naquele dia.","Bloco 'Revisão espaçada' dos dias"],
    ["Anki com cartões mínimos","Um fato por cartão. Para código, cartões 'código → saída'; para lógica, 'proposição → negação'; para inglês, a palavra com a frase original. Faça 15 a 20 min por dia e não deixe acumular.","Aquecimento de todo dia"],
    ["Pré-teste","Tente o exercício 1 ANTES de estudar o conteúdo. Errar primeiro deixa o cérebro procurando a resposta, e a leitura fixa mais.","Minutos 10 a 15 dos dias de conteúdo"],
    ["Palácio da memória (método de loci)","Ponha cada equivalência lógica num cômodo da sua casa, com uma imagem exagerada: porta = condicional (¬p ∨ q), sala = contrapositiva, cozinha = De Morgan, quarto = exportação, banheiro = bicondicional. Na prova, percorra a casa de memória.","Tema L4 e revisões de lógica"],
    ["Mnemônicos","MANÉ para negar a condicional (MAntém, Nega, E) · BIM é estável / QSH não · CATALÃO 1-1-2-5-14-42 · Largura = Leque = fiLa / Profundidade = Pilha · AND para no Falso, OR para no Verdadeiro · a escada 1 < log n < n < n log n < n² < 2ⁿ < n!","Caixa 'Para memorizar' de cada tema"],
    ["Dual coding (desenho + palavra)","Desenhe a pilha, a fila, a árvore e o grafo em cada exercício. Imagem e texto juntos criam duas rotas para a mesma lembrança.","Estruturas, busca e ordenação"],
    ["Prática intercalada","Os dias de prática misturam temas, como na prova real. É mais difícil no começo, mas treina reconhecer o tipo de questão.","Dias de prática e blocos mistos"],
    ["Caderno de erros","Para cada erro, anote o tema, o tipo (conceito, leitura, cálculo ou pegadinha) e a regra que teria evitado o erro. Na reta final você revisa só o caderno.","Depois de cada bateria e simulado"],
    ["Técnica de Feynman","Explique o tema em voz alta, como para um leigo, em 2 minutos. Onde travar está a lacuna para voltar ao livro.","Fim dos dias de conteúdo"],
    ["Estudar no horário da prova","A memória funciona melhor quando o contexto do estudo parece com o da prova. Estude às 20h e faça os simulados às 19h, de preferência numa quinta-feira.","Todo o cronograma"],
    ["Sono e pausas","O sono consolida o que foi estudado. Durma 7h ou mais e faça pausas de 5 min a cada 25 a 30 min (pomodoro).","Sempre, principalmente na última semana"]
  ];
  return '<section><div class="eyebrow">Memorização</div><h1>Técnicas avançadas, já embutidas na agenda</h1><p class="muted">Você não precisa decidir quando usar cada técnica: cada dia já traz a sequência pronta. Aqui está o porquê de cada uma.</p></section>'+
    tabs("tecnicas", [{key:"lista", label:"As 12 técnicas", html:'<div class="grid2">'+C.map(function(c){return '<div class="card"><h3>'+esc(c[0])+'</h3><p>'+esc(c[1])+'</p><p class="small muted">Onde aparece: '+esc(c[2])+'</p></div>';}).join("")+'</div>'},
      {key:"roteiro", label:"Roteiro do dia", html:'<div class="eyebrow">Dia de semana com conteúdo novo (2h)</div>'+timeline({kind:"estudo",wd:"Seg"})+'<div class="eyebrow">Sábado ou domingo com conteúdo novo (4h)</div>'+timeline({kind:"estudo",wd:"Sáb"})+'<div class="eyebrow">Dias de prática e revisão</div>'+timeline({kind:"pratica",wd:"Seg"})+timeline({kind:"pratica",wd:"Sáb"})}]);
}

/* ---------- Página: inglês ---------- */
var EN = {
  exams: [
    ["2022","ULTRARAM, nova memória de computador (Lancaster) + Typealike, gestos no teclado (Waterloo)","VerveTimes · ScienceDaily","20 (2 textos)"],
    ["2024-2","Pesquisadores falam dos riscos e benefícios da IA e dos LLMs","Virginia Tech","10"],
    ["2025-1","'Indoor training effect': treinar IA num ambiente com menos ruído","MIT News","10"],
    ["2025-2","Estudo do MIT Media Lab: ChatGPT e engajamento cognitivo em redações","TIME (sobre estudo do MIT)","10"],
    ["2025-2R","LLMs mudam recomendações médicas por causa de erros de digitação e estilo","Estudo do MIT","10"]
  ],
  tipos: [
    ["Detalhe explícito","≈ 45%","According to the text, what… / What did X do to…","A resposta está escrita no texto, quase sempre com sinônimos. Ache a palavra-chave da pergunta no parágrafo e compare frase a frase."],
    ["Causa e motivação","≈ 15%","Why did the researchers… / What motivated…","Procure because, since, to + verbo, in order to, so that e led to."],
    ["Inferência e implicação","≈ 15%","What does the study imply… / What could be a potential implication…","A alternativa certa é a conclusão mais prudente. Desconfie de always, never, completely e all."],
    ["Objetivo e ideia principal","≈ 10%","What was the primary goal… / What is the primary purpose of the passage?","Releia o título e o 1º parágrafo; a resposta resume o texto todo, não um detalhe."],
    ["Opinião de pessoa citada","≈ 8%","According to the lead author… / What worries X…","Ache o nome, depois o verbo de fala (says, notes, argues, warns) e leia a frase da citação."],
    ["Vocabulário e expressão","≈ 5%","What does the word 'uncertainty' mean in this context?","Leia a frase inteira; o sentido no contexto vale mais que o do dicionário."],
    ["Tom e analogia","≈ 2%","Which best describes the tone… / What analogy do the researchers use…","Textos de divulgação são quase sempre informativos e cautelosamente otimistas."]
  ],
  vocab: [
    ["Pesquisa acadêmica",[["study","estudo"],["findings","resultados, achados"],["researchers","pesquisadores"],["lead author","autor principal"],["paper","artigo científico"],["peer-reviewed","revisado por pares"],["approach","abordagem"],["framework","estrutura, arcabouço"],["outcome","resultado"],["assess / evaluate","avaliar"],["survey","pesquisa de opinião"],["sample","amostra"],["participants / subjects","participantes"],["evidence","evidência"],["claim","afirmação, alegação"]]],
    ["IA e computação",[["training data","dados de treino"],["dataset","conjunto de dados"],["model","modelo"],["benchmark","teste de referência"],["outperform","ter desempenho melhor que"],["accuracy","acurácia"],["bias","viés"],["fairness","justiça, equidade"],["prompt","instrução dada ao modelo"],["hallucination","resposta inventada pelo modelo"],["deploy","colocar em uso"],["robust","robusto"],["noise","ruído"],["agent","agente"],["fine-tune","ajustar o modelo"]]],
    ["Conectores (mudam o sentido!)",[["however / yet","porém"],["although / though","embora"],["despite / in spite of","apesar de"],["whereas / while","enquanto (contraste)"],["therefore / thus","portanto"],["hence","por isso"],["moreover / furthermore","além disso"],["instead","em vez disso"],["unless","a menos que"],["rather than","em vez de"],["as a result","como resultado"],["on the other hand","por outro lado"]]],
    ["Falsos cognatos",[["actually","na verdade"],["eventually","por fim"],["pretend","fingir"],["realize","perceber"],["assist","ajudar"],["sensible","sensato"],["argue","defender, argumentar"],["attend","frequentar"],["library","biblioteca"],["college","faculdade"],["data","dados"],["exquisite","refinado"]]],
    ["Verbos de opinião e hedge",[["suggest","sugerir, indicar"],["imply","implicar, dar a entender"],["warn","alertar"],["caution","advertir"],["note","observar"],["highlight","destacar"],["likely","provável"],["may / might / could","pode (possibilidade)"],["rely on","depender de"],["enhance","melhorar"],["mitigate","reduzir, atenuar"],["drawback","desvantagem"]]]
  ],
  treino: [
    ["en-diag","03/11","Prova 2025-2R, questões 1 a 10 (no simulado diagnóstico)"],
    ["en-22a","08/11","Prova 2022, texto 1 (Q1–10)"],
    ["en-22b","14/11","Prova 2022, texto 2 (Q11–20)"],
    ["en-24","21/11","Prova 2024-2, Q1–10"],
    ["en-251","28/11","Prova 2025-1, Q1–10 (checkpoint 1)"],
    ["en-own","05/12","Texto de treino desta página (10 questões)"],
    ["en-252","19/12","Prova 2025-2, Q1–10 (checkpoint 2)"],
    ["en-redo","30/01","Refazer as 60 questões de inglês das provas, só as que errou"]
  ],
  texto: {
    title:"Study finds AI coding assistants help beginners, but only when students explain first",
    paras:[
      "A new study suggests that AI coding assistants can speed up how quickly beginners learn to program, but only if students are required to explain their own reasoning before receiving help. The findings, which will be presented at an education conference next spring, challenge the common assumption that more assistance always leads to better learning.",
      "The researchers divided 240 first-year computer science students into three groups for an eight-week course. The first group used a chatbot that wrote complete solutions on request. The second group had no AI support at all. The third group used the same chatbot, but the tool would only respond after the student typed a short explanation of what they thought was wrong with their code.",
      "At the end of the course, all students took a written exam without any digital tools. Students in the \"explain-first\" group scored 18 percent higher than those in the unrestricted group, and slightly higher than the group with no AI. \"The unrestricted group finished their assignments faster, but they struggled when the chatbot was taken away,\" says the study's lead author. \"They had outsourced the thinking, not just the typing.\"",
      "The team also measured how often students copied code without changes. In the unrestricted group, copying increased steadily over the weeks, reaching nearly 70 percent of submissions by the end of the course. In contrast, the explain-first students rarely copied entire answers.",
      "Despite these results, the authors caution that the study has limitations. All participants came from a single university, and the course lasted only two months. \"We don't yet know whether the benefits last, or whether they apply to more advanced students,\" the lead author notes. The team now plans a year-long study across several institutions.",
      "The researchers argue that the design of AI tools matters as much as their accuracy. \"A small amount of friction can turn a shortcut into a learning opportunity,\" they write."
    ],
    qs:[
      ["What is the main finding of the study?",["AI assistants always make beginners learn faster.","Students learn better without any AI support.","AI assistants help beginners learn when students must explain their reasoning first.","Chatbots write better code than first-year students.","Written exams are not a good way to measure programming skills."],2],
      ["What was different about the third group?",["It used a different, more accurate chatbot.","Its chatbot answered only after the student explained the problem.","It studied for twelve weeks instead of eight.","It had no access to computers.","It received complete solutions on request."],1],
      ["How did the explain-first group perform on the final exam?",["It scored 18% higher than the unrestricted group and slightly higher than the no-AI group.","It scored lower than the no-AI group.","It scored the same as the unrestricted group.","It scored 70% higher than all the other groups.","It did not take the final exam."],0],
      ["In paragraph 3, \"they had outsourced the thinking\" means that the students…",["hired other people to do their homework.","thought more carefully than the other groups.","typed faster than the other groups.","let the chatbot do the reasoning for them.","refused to use the chatbot."],3],
      ["What happened to code copying in the unrestricted group?",["It decreased over time.","It stayed at about 18% during the course.","It increased steadily, reaching nearly 70% of submissions.","It was never measured.","It was the same as in the explain-first group."],2],
      ["In paragraph 5, the word \"Despite\" introduces…",["an example.","a contrast with the positive results.","a cause of the results.","a definition.","a final conclusion."],1],
      ["Which of the following is a limitation mentioned by the authors?",["The chatbot made many mistakes.","Students did not like the course.","The exam used digital tools.","The groups had different teachers.","All participants were from one university and the course was short."],4],
      ["What do the researchers plan to do next?",["Stop using chatbots in classrooms.","Run a year-long study at several institutions.","Sell their chatbot to universities.","Repeat the same study with the same students.","Publish the students' code online."],1],
      ["\"A small amount of friction\" refers to…",["requiring students to explain before getting help.","slowing down the computers in the lab.","giving students harder exams.","removing the chatbot in the last week.","limiting the length of the code."],0],
      ["Which best describes the tone of the passage?",["Angry and critical","Humorous","Cautiously optimistic and balanced","Completely neutral, with no conclusions","Pessimistic about technology"],2]
    ]
  }
};
function ingles(){
  var done = ARTS.filter(function(a){return st[a.id];}).length;
  var wks = {}; ARTS.forEach(function(a){ (wks[a.wk] = wks[a.wk] || []).push(a); });
  var P = {}; var h = '<section><div class="eyebrow">Etapa 1 · N1 · eliminatória e classificatória</div><h1>Prova de Inglês</h1>'+
    '<p class="muted">São 10 questões de múltipla escolha sobre um texto de Computação, e cada acerto vale 1 ponto direto na nota final. Quem tira 4 ou menos é eliminado. A meta é 8 ou mais.</p>'+
    '<div class="facts"><div class="fact"><b>10</b><span>questões, 1 ponto cada</span></div><div class="fact"><b>≥ 5</b><span>para não ser eliminado</span></div><div class="fact"><b>8+</b><span>meta deste plano</span></div><div class="fact"><b>~25 min</b><span>tempo-alvo na prova</span></div></div>'+
    '</section>';
  P.raiox = '<section><div class="eyebrow">Raio-X</div><h2>O que caiu em cada prova</h2><div class="tablebox"><table><thead><tr><th>Prova</th><th>Texto</th><th>Fonte</th><th>Questões</th></tr></thead><tbody>'+
    EN.exams.map(function(r){return '<tr><td>'+r[0]+'</td><td>'+esc(r[1])+'</td><td>'+esc(r[2])+'</td><td>'+r[3]+'</td></tr>';}).join("")+'</tbody></table></div>'+
    '<div class="card"><b>Padrão</b><ul><li>É sempre uma notícia de divulgação sobre <b>pesquisa universitária em IA ou computação</b>, publicada de 3 a 9 meses antes da prova</li><li>Nas 3 provas de 2025, todos os textos eram sobre estudos do MIT (2 publicados pelo MIT News e 1 pela revista TIME)</li><li>Desde 2024, o tema é o efeito da IA e dos LLMs nas pessoas ou o treino de modelos de IA</li><li>As 10 perguntas são em inglês e seguem a ordem dos parágrafos</li></ul></div></section>';
  P.tipos = '<section><div class="eyebrow">Tipos de pergunta</div><h2>Como a banca pergunta</h2><p class="muted small">Percentuais aproximados, contando as 50 questões de inglês das provas da pasta.</p><div class="tablebox"><table><thead><tr><th>Tipo</th><th>Peso</th><th>Como aparece</th><th>Como atacar</th></tr></thead><tbody>'+
    EN.tipos.map(function(r){return '<tr><td><b>'+esc(r[0])+'</b></td><td>'+r[1]+'</td><td><i>'+esc(r[2])+'</i></td><td>'+esc(r[3])+'</td></tr>';}).join("")+'</tbody></table></div></section>';
  P.metodo = '<section><div class="eyebrow">Método na prova (25 min)</div><h2>Passo a passo</h2><div class="timeline">'+
    '<div><b>0–3 min</b>Leia as 10 perguntas (sem as alternativas) e sublinhe as palavras-chave</div>'+
    '<div><b>3–8</b>Leia o título e o 1º e o último parágrafo: objetivo, achado e próximo passo</div>'+
    '<div><b>8–20</b>Responda em ordem; cada pergunta fica num parágrafo, então ache a palavra-chave nele (scanning)</div>'+
    '<div><b>20–23</b>Nas dúvidas, elimine alternativas extremas (always, never, all) e as que falam de algo fora do texto</div>'+
    '<div><b>23–25</b>Passe as respostas para o cartão</div></div></section>';
  P.vocab = '<section><div class="eyebrow">Vocabulário essencial</div><h2>Palavras que aparecem nesses textos</h2><p class="muted small">Passe tudo para o Anki. Marque o grupo quando souber todas as palavras sem olhar.</p>'+
    EN.vocab.map(function(g,i){return '<div class="card"><h3>'+esc(g[0])+'</h3><div class="vocab">'+g[1].map(function(p){return '<div><b>'+esc(p[0])+'</b> — '+esc(p[1])+'</div>';}).join("")+'</div>'+chk("voc:"+i,"Domino este grupo")+'</div>';}).join("")+'</section>';
  P.treino = '<section><div class="eyebrow">Treino com provas</div><h2>Cronograma de treino com provas antigas</h2><ul class="tasks">'+
    EN.treino.map(function(t){return '<li>'+chk(t[0], '<b>'+t[1]+'</b> · '+esc(t[2]))+'</li>';}).join("")+'</ul><p class="small muted">Os PDFs estão em MESTRADO/provas. Cronometre 25 min por texto.</p></section>';
  var tx = EN.texto;
  P.texto = '<section><div class="eyebrow">Texto de treino · escrito para este plano (não é uma notícia real)</div><h2>'+esc(tx.title)+'</h2><div class="reading">'+tx.paras.map(function(p,i){return '<p><span class="small muted">['+(i+1)+']</span> '+esc(p)+'</p>';}).join("")+'</div>'+
    '<div class="card" id="quiz">'+tx.qs.map(function(q,i){return '<div class="ex"><b>'+(i+1)+'. '+esc(q[0])+'</b><ul class="opts">'+q[1].map(function(o,j){return '<li><label data-q="'+i+'" data-o="'+j+'"><input type="radio" name="q'+i+'" value="'+j+'"> <span>'+"abcde"[j]+') '+esc(o)+'</span></label></li>';}).join("")+'</ul></div>';}).join("")+
    '<div class="nav"><button class="btn primary" type="button" id="corrigir">Corrigir</button><span id="nota" class="meta"></span></div></div></section>';
  P.artigos = '<section><div class="eyebrow">Leitura semanal</div><h2>'+ARTS.length+' artigos prováveis</h2>'+
    '<p class="muted">Notícias de IA do MIT News de maio a outubro de 2026, com o perfil dos textos das provas. São 3 por semana, da semana 3 à 13. Leia cada uma em 20 min respondendo: <b>What was the goal? What did they find? What is the limitation? What comes next?</b> Depois escreva 3 perguntas de múltipla escolha como se fosse a banca e ponha 5 palavras no Anki.</p>'+
    pbar(done, ARTS.length, "lidos")+
    '<div class="card"><h3>Varredura de artigos novos</h3><p>O texto da prova pode sair até janeiro de 2027. Toda segunda-feira, abra <a href="https://news.mit.edu/topic/artificial-intelligence2" target="_blank" rel="noopener">MIT News · Artificial Intelligence</a>, e de vez em quando <a href="https://www.sciencedaily.com/news/computers_math/artificial_intelligence/" target="_blank" rel="noopener">ScienceDaily · AI</a> e <a href="https://time.com/tag/artificial-intelligence/" target="_blank" rel="noopener">TIME · AI</a>. Se aparecer um estudo sobre LLMs ou sobre o efeito da IA nas pessoas, leia na mesma semana como prioridade máxima.</p><ul class="tasks">';
  for (var w=6; w<=13; w++) P.artigos += '<li>'+chk("scan:"+w, 'Semana '+w+' ('+WEEKS[w-1].range+'): conferir artigos novos')+'</li>';
  P.artigos += '</ul></div>';
  Object.keys(wks).sort(function(a,b){return a-b;}).forEach(function(w){
    P.artigos += '<div class="card"><div class="eyebrow"><a href="'+weekFile(+w)+'">Semana '+w+' · '+esc(WEEKS[w-1].range)+'</a></div><ul class="tasks">'+wks[w].map(artItem).join("")+'</ul></div>';
  });
  P.artigos += '<div class="card"><h3>Reta final (semanas 12 e 13)</h3><p>Releia os artigos de prioridade <b>Máxima</b>: só o seu resumo e as palavras do Anki.</p></div></section>';
  return h + tabs("ingles", [{key:"raiox",label:"Raio-X das provas",html:P.raiox},{key:"tipos",label:"Tipos de pergunta",html:P.tipos},{key:"metodo",label:"Método",html:P.metodo},{key:"vocab",label:"Vocabulário",html:P.vocab},{key:"treino",label:"Treino com provas",html:P.treino},{key:"texto",label:"Texto de treino",html:P.texto},{key:"artigos",label:"Artigos prováveis",html:P.artigos},{key:"provaveis",label:"Prováveis + questões",html:provHTML()}]);
}
function bindQuiz(){
  var b = document.getElementById("corrigir"); if (!b) return;
  b.addEventListener("click", function(){
    var qs = EN.texto.qs, ok = 0;
    document.querySelectorAll("#quiz label[data-q]").forEach(function(l){ l.classList.remove("right","wrong"); });
    qs.forEach(function(q,i){
      var sel = document.querySelector('input[name="q'+i+'"]:checked');
      document.querySelector('#quiz label[data-q="'+i+'"][data-o="'+q[2]+'"]').classList.add("right");
      if (sel && +sel.value === q[2]) ok++; else if (sel) sel.parentNode.classList.add("wrong");
    });
    document.getElementById("nota").textContent = "Você acertou "+ok+" de 10. A alternativa certa está em verde.";
    st["en-own-score"] = ok; if (ok >= 5) st["en-own"] = true; save();
  });
}


/* ---------- Inglês: pré-análise dos artigos e questões prováveis ---------- */
function pqBlock(z, q, i){
  var name = "pq-"+z.id+"-"+i, sel = st["pqans:"+z.id+":"+i];
  return '<div class="ex pq" data-z="'+z.id+'" data-ans="'+q.ans+'"><div><b>'+(i+1)+'.</b> '+esc(q.stem)+'</div><ul class="opts">'+
    q.opts.map(function(o,j){ return '<li><label data-o="'+j+'"><input type="radio" name="'+name+'" value="'+j+'"'+(sel===j?" checked":"")+'> <span>'+"abcde"[j]+') '+esc(o)+'</span></label></li>'; }).join("")+'</ul>'+
    '<p class="small muted why" hidden>Resposta: <b>'+"abcde"[q.ans]+')</b> · onde está no texto: '+esc(q.par)+' · '+esc(q.why)+'</p></div>';
}
function pqPanel(z){
  var r = st["pqres:"+z.id];
  return '<div class="panelhead"><div class="eyebrow">Nota '+z.total+'/100 · MIT News, '+esc(z.dt)+'/2026</div><h3><a href="'+esc(z.url)+'" target="_blank" rel="noopener">'+esc(z.title)+' ↗</a></h3>'+
    '<p class="muted">Leia o artigo no MIT News em até 15 min (abre em outra aba) e responda sem voltar ao texto. Depois corrija e releia só os parágrafos das questões que errou. Os § contam os intertítulos como parágrafos.</p>'+
    (r?'<div class="card"><b>Última correção ('+esc(r.date)+'):</b> '+r.ok+'/10</div>':'')+'</div>'+
    '<div class="card">'+z.qs.map(function(q,i){ return pqBlock(z, q, i); }).join("")+'</div>'+
    '<div class="nav"><button class="btn primary" type="button" data-pqgrade="'+z.id+'">Corrigir</button><button class="btn" type="button" data-pqreset="'+z.id+'">Limpar</button><span class="meta" id="pqres-'+z.id+'"></span></div>';
}
function scanHTML(P){
  return (P.scans||[]).slice().reverse().map(function(sc){ return '<div class="card"><h3>Varredura de '+esc(sc[0])+'</h3><p class="small muted">Artigos novos no MIT News · AI desde a varredura anterior, avaliados com a mesma régua.</p><ul>'+
    sc[1].map(function(x){ return '<li><b>'+esc(x[1])+'</b> <span class="small muted">('+esc(x[0])+')</span>: '+esc(x[2])+'</li>'; }).join("")+'</ul></div>'; }).join("");
}
function pqPos(z){ return DATA.prov.rank.filter(function(r){return r.url===z.url;})[0].pos; }
function provHTML(){
  var P = DATA.prov; if (!P) return "";
  var top = P.rank.slice(0, 6);
  var rub = '<div class="card"><h3>Como a nota foi calculada (100 pontos)</h3><ul>'+P.rubric.map(function(r){ return '<li><b>'+esc(r[1])+' (até '+r[2]+')</b>: '+esc(r[3])+'</li>'; }).join("")+'</ul>'+
    '<p class="small muted">Máxima: 80 ou mais. Alta: 70 a 79. Média: abaixo de 70. A nota é uma estimativa; o texto da prova pode ser um artigo publicado depois de outubro. Por isso a varredura semanal continua valendo, e você pode dar nota aos artigos novos com a mesma régua.</p></div>';
  var rows = P.rank.map(function(r){ var cls = r.tier==="Máxima"?"simulado":r.tier==="Alta"?"pratica":"estudo";
    return '<tr><td><b>'+r.pos+'º</b></td><td><a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.title)+'</a><div class="small muted">'+esc(r.note)+'</div></td><td>'+esc(r.dt)+'</td>'+
      r.s.map(function(v){return '<td>'+v+'</td>';}).join("")+'<td><b>'+r.total+'</b></td><td><span class="pill p-'+cls+'">'+r.tier+'</span></td></tr>'; }).join("");
  var tbl = '<div class="tablebox"><table><thead><tr><th>#</th><th>Artigo</th><th>Data</th><th>Formato<br>/30</th><th>Tema<br>/30</th><th>Janela<br>/15</th><th>Tam.<br>/15</th><th>Acess.<br>/10</th><th>Total</th><th>Prioridade</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  var lead = '<section><div class="eyebrow">Pré-análise dos '+P.rank.length+' artigos</div><h2>Os mais prováveis e as questões de cada um</h2>'+
    '<p class="muted">Cada artigo recebeu nota de 0 a 100 numa régua tirada das provas de 2022 a 2025-2R. Para os '+P.quizzes.length+' primeiros, há 10 questões no formato da banca: em inglês, 5 alternativas, na ordem do texto, terminando com implicação ou lição geral. Cada simulado tem 2 respostas de cada letra, como nas provas de 2025.</p>'+
    '<div class="facts">'+top.slice(0,4).map(function(r){ return '<div class="fact"><b>'+r.total+'</b><span>'+r.pos+'º · '+esc(r.title)+'</span></div>'; }).join("")+'</div></section>';
  return lead + tabs("prov", [{key:"ranking", label:"Ranking dos "+P.rank.length, html:rub+tbl+scanHTML(P)}].concat(P.quizzes.slice().sort(function(a,b){ return pqPos(a)-pqPos(b); }).map(function(z,k){
    var r = st["pqres:"+z.id]; return {key:z.id, cls:r?"done":"", label:pqPos(z)+'º · '+esc(z.title.replace(/^Q&A:\s*/,'').split(/[:—]/)[0].slice(0,34))+'<small>'+(r?r.ok+'/10':z.total+' pts')+'</small>', html:pqPanel(z)}; })), "ranking");
}
function bindProv(){
  if (PAGE !== "ingles" || !DATA.prov) return;
  app.addEventListener("change", function(e){ var n = e.target.name; if (!n || n.indexOf("pq-") !== 0) return;
    var p = n.split("-"); st["pqans:"+p[1]+":"+p[2]] = +e.target.value; save(); });
  app.addEventListener("click", function(e){
    var g = e.target.getAttribute && e.target.getAttribute("data-pqgrade"), rs = e.target.getAttribute && e.target.getAttribute("data-pqreset");
    if (!g && !rs) return;
    var id = g || rs, ok = 0, blank = 0;
    document.querySelectorAll('.pq[data-z="'+id+'"]').forEach(function(el){
      var ans = +el.getAttribute("data-ans"), sel = el.querySelector("input:checked");
      el.querySelectorAll("label").forEach(function(l){ l.classList.remove("right","wrong"); });
      if (rs) { el.querySelectorAll("input").forEach(function(i){ i.checked = false; }); el.querySelector(".why").hidden = true; return; }
      el.querySelector('label[data-o="'+ans+'"]').classList.add("right"); el.querySelector(".why").hidden = false;
      if (!sel) blank++; else if (+sel.value === ans) ok++; else sel.parentNode.classList.add("wrong");
    });
    var out = document.getElementById("pqres-"+id);
    if (rs) { Object.keys(st).forEach(function(k){ if (k.indexOf("pqans:"+id+":")===0) delete st[k]; }); save(); out.textContent = ""; return; }
    var now = new Date(); st["pqres:"+id] = {ok:ok, date:pad(now.getDate())+"/"+pad(now.getMonth()+1)}; save();
    var tb = document.getElementById("tb-"+id); if (tb) tb.classList.add("done");
    out.textContent = "Você acertou "+ok+" de 10"+(blank?" ("+blank+" em branco)":"")+". "+(ok>=8?"Meta atingida.":ok>=5?"Passaria, mas a meta é 8.":"Na prova, 4 ou menos elimina.")+" Veja o parágrafo de cada erro.";
  });
}

/* ---------- Página: simulados ---------- */
var SIMDATE = {A:"2027-01-16", B:"2027-01-17", C:"2027-01-23", D:"2027-01-24", E:"2027-01-30"};
var SIMDAY = {}; Object.keys(SIMDATE).forEach(function(k){ SIMDAY[SIMDATE[k]] = k; });
function simMin(s){ return s.en ? 150 : 90; }
function qBlock(sim, num, q, isEn){
  var name = "s"+sim+"-"+num, sel = st["simans:"+sim+":"+num];
  return '<div class="ex simq" data-sim="'+sim+'" data-num="'+num+'" data-ans="'+q.ans+'"><div><b>'+num+'.</b> '+(isEn?'':'<span class="pill p-estudo">'+esc(q.bloco)+'</span> ')+esc(q.stem)+'</div>'+
    (q.code?'<pre>'+esc(q.code)+'</pre>':'')+
    '<ul class="opts">'+q.opts.map(function(o,j){ return '<li><label data-o="'+j+'"><input type="radio" name="'+name+'" value="'+j+'"'+(sel===j?" checked":"")+'> <span>'+"abcde"[j]+') '+esc(o)+'</span></label></li>'; }).join("")+'</ul>'+
    '<p class="small muted why" hidden>Resposta: <b>'+"abcde"[q.ans]+')</b> '+esc(q.why||"")+'</p></div>';
}
function simPanel(s){
  var id = s.id, res = st["simres:"+id], h = [];
  var d = DAYS.filter(function(x){return x.id===SIMDATE[id];})[0];
  h.push('<div class="panelhead"><div class="eyebrow">Simulado '+id+(d?' · agendado para '+d.wd+' '+d.dm:'')+'</div><h2>Simulado '+id+': '+(s.en?'40 questões (10 de Inglês + 30 de Específicas)':'30 questões de Específicas')+'</h2>'+
    '<p class="muted">Tempo: '+(simMin(s)===150?'2h30':'1h30')+'. Resolva no papel primeiro, sem computador, e marque aqui só no fim, como no cartão-resposta. A ordem dos blocos é a da prova: Python, Estruturas de Dados, Busca, Ordenação e Lógica.</p>'+
    (res?'<div class="card"><b>Última correção ('+esc(res.date)+')</b><p>Inglês: '+(s.en?res.n1+'/10 · ':'')+'Específicas: '+res.n2+'/30 · N1 + 2·N2 = '+((s.en?res.n1:0)+2*res.n2)+'</p></div>':'')+
    '<div class="nav"><button class="btn primary" type="button" data-timer="'+id+'">Iniciar cronômetro</button><span class="meta" id="timer-'+id+'"></span></div></div>');
  if (s.en) h.push('<section><div class="eyebrow">Inglês · texto de treino escrito para este plano (não é uma notícia real)</div><h3>'+esc(s.en.title)+'</h3><div class="reading">'+s.en.paras.map(function(p,i){return '<p><span class="small muted">['+(i+1)+']</span> '+esc(p)+'</p>';}).join("")+'</div><div class="card">'+
    s.en.qs.map(function(q,i){ return qBlock(id, i+1, q, true); }).join("")+'</div></section>');
  var off = s.en ? 11 : 1;
  h.push('<section><div class="eyebrow">Conhecimentos Específicos</div><div class="card">'+s.esp.map(function(q,i){ return qBlock(id, i+off, q, false); }).join("")+'</div></section>');
  h.push('<section><div class="nav"><button class="btn primary" type="button" data-grade="'+id+'">Corrigir simulado '+id+'</button><button class="btn" type="button" data-reset="'+id+'">Limpar respostas</button></div><div id="result-'+id+'"></div></section>');
  return h.join("");
}
function simResults(){
  var rows = DATA.sims.map(function(s){ var r = st["simres:"+s.id];
    return '<tr><td><b>'+s.id+'</b></td><td>'+(SIMDATE[s.id].split("-").reverse().slice(0,2).join("/"))+'</td><td>'+(r?(s.en?r.n1+'/10':'—'):'')+'</td><td>'+(r?r.n2+'/30':'')+'</td><td>'+(r?((s.en?r.n1:0)+2*r.n2):'')+'</td><td>'+(r?(r.n2>=24?'<span class="pill p-admin">meta</span>':r.n2>=15?'<span class="pill p-pratica">aprovado no corte</span>':'<span class="pill p-simulado">abaixo de 15</span>'):'<span class="small muted">não feito</span>')+'</td></tr>'; }).join("");
  return '<div class="tablebox"><table><thead><tr><th>Simulado</th><th>Data</th><th>Inglês</th><th>Específicas</th><th>N1 + 2·N2</th><th>Situação</th></tr></thead><tbody>'+rows+'</tbody></table></div>'+
    '<div class="card"><b>Metas</b><ul><li>Específicas: 15/30 é o corte; 24/30 em 2 de 3 simulados da semana 12 é a meta do plano</li><li>Inglês: 5/10 é o corte; 8/10 é a meta</li><li>Depois de cada simulado, lance os erros no caderno de erros com o tipo (conceito, leitura, cálculo ou pegadinha)</li></ul></div>';
}
function simulados(){
  return '<section><div class="eyebrow">Banco de simulados · formato da prova 2027</div><h1>Simulados A a E</h1><p class="muted">São 150 questões de Específicas inéditas, distribuídas como na prova provável (Python 8, Estruturas de Dados 6, Busca 4, Ordenação 5 e Lógica 7), e 4 textos de Inglês. Os gabaritos foram conferidos: as questões de código executando o código e as de lógica por tabela-verdade. As letras estão balanceadas, como a banca faz.</p></section>'+
    tabs("sim", DATA.sims.map(function(s){ var r = st["simres:"+s.id]; return {key:"sim-"+s.id.toLowerCase(), cls:r?"done":"", label:'Simulado '+s.id+'<small>'+(s.en?'40 q · 2h30':'30 q · 1h30')+'</small>', html:simPanel(s)}; })
      .concat([{key:"resultados", label:"Resultados<small>histórico</small>", html:simResults()}]));
}
function grade(id){
  var s = DATA.sims.filter(function(x){return x.id===id;})[0], n1 = 0, n2 = 0, byB = {}, blank = 0;
  document.querySelectorAll('.simq[data-sim="'+id+'"]').forEach(function(el){
    var num = +el.getAttribute("data-num"), ans = +el.getAttribute("data-ans"), sel = el.querySelector("input:checked");
    el.querySelectorAll("label").forEach(function(l){ l.classList.remove("right","wrong"); });
    el.querySelector('label[data-o="'+ans+'"]').classList.add("right");
    el.querySelector(".why").hidden = false;
    var isEn = s.en && num <= 10, ok = sel && +sel.value === ans;
    if (!sel) blank++; else if (!ok) sel.parentNode.classList.add("wrong");
    if (isEn) { if (ok) n1++; }
    else { var q = s.esp[num - (s.en ? 11 : 1)]; byB[q.bloco] = byB[q.bloco] || [0,0]; byB[q.bloco][1]++; if (ok) { n2++; byB[q.bloco][0]++; } }
  });
  var now = new Date(); st["simres:"+id] = {n1:n1, n2:n2, date: pad(now.getDate())+"/"+pad(now.getMonth()+1)}; save();
  var tb = document.getElementById("tb-sim-"+id.toLowerCase()); if (tb) tb.classList.add("done");
  var elim = (s.en && n1 <= 4) || n2 < 15;
  document.getElementById("result-"+id).innerHTML = '<div class="card"><h3>Resultado do simulado '+id+'</h3>'+
    '<div class="facts">'+(s.en?'<div class="fact"><b>'+n1+'/10</b><span>Inglês (N1)</span></div>':'')+'<div class="fact"><b>'+n2+'/30</b><span>Específicas (N2)</span></div><div class="fact"><b>'+((s.en?n1:0)+2*n2)+'</b><span>N1 + 2·N2</span></div><div class="fact"><b>'+blank+'</b><span>em branco</span></div></div>'+
    '<div class="tablebox"><table><thead><tr><th>Bloco</th><th>Acertos</th></tr></thead><tbody>'+Object.keys(byB).map(function(b){return '<tr><td>'+esc(b)+'</td><td>'+byB[b][0]+'/'+byB[b][1]+'</td></tr>';}).join("")+'</tbody></table></div>'+
    (elim?'<div class="alert">Nas regras do edital, essa nota eliminaria (Inglês ≤ 4 ou Específicas < 15). Reforce o bloco com menos acertos.</div>':'<p>As respostas certas estão em verde; as suas erradas, em vermelho, com a explicação embaixo de cada questão.</p>')+'</div>';
}
var TIMERS = {};
function startTimer(id, fresh){
  var s = DATA.sims.filter(function(x){return x.id===id;})[0];
  if (fresh || !st["simstart:"+id]) { st["simstart:"+id] = Date.now(); save(); }
  clearInterval(TIMERS[id]);
  function tick(){ var el = document.getElementById("timer-"+id); if (!el) return;
    var left = Math.round((st["simstart:"+id] + simMin(s)*60000 - Date.now())/1000);
    if (left <= 0) { el.textContent = "Tempo esgotado"; clearInterval(TIMERS[id]); return; }
    el.textContent = "Restam " + Math.floor(left/3600) + "h" + pad(Math.floor(left%3600/60)) + "min" + pad(left%60) + "s"; }
  tick(); TIMERS[id] = setInterval(tick, 1000);
}
function bindSim(){
  if (PAGE !== "simulados") return;
  DATA.sims.forEach(function(s){ var t0 = st["simstart:"+s.id]; if (t0 && Date.now() - t0 < simMin(s)*60000) startTimer(s.id, false); });
  app.addEventListener("click", function(e){
    var g = e.target.getAttribute && (e.target.getAttribute("data-grade") || e.target.getAttribute("data-reset") || e.target.getAttribute("data-timer"));
    if (!g) return;
    if (e.target.hasAttribute("data-grade")) grade(g);
    else if (e.target.hasAttribute("data-timer")) startTimer(g, true);
    else { Object.keys(st).forEach(function(k){ if (k.indexOf("simans:"+g+":")===0) delete st[k]; }); delete st["simstart:"+g]; save();
      document.querySelectorAll('.simq[data-sim="'+g+'"]').forEach(function(el){ el.querySelectorAll("input").forEach(function(i){i.checked=false;}); el.querySelectorAll("label").forEach(function(l){l.classList.remove("right","wrong");}); el.querySelector(".why").hidden = true; });
      document.getElementById("result-"+g).innerHTML = ""; var tm = document.getElementById("timer-"+g); if (tm) tm.textContent = ""; clearInterval(TIMERS[g]); }
  });
  app.addEventListener("change", function(e){ var n = e.target.name; if (!n || n.charAt(0) !== "s" || e.target.type !== "radio") return;
    var parts = n.slice(1).split("-"); st["simans:"+parts[0]+":"+parts[1]] = +e.target.value; save(); });
}

/* ---------- inicialização ---------- */
nav();
var R = {home:home, mapa:mapa, semana:semana, temas:temas, tecnicas:tecnicas, ingles:ingles, analise:analise, simulados:simulados};
app.innerHTML = (R[PAGE] || home)();
bindQuiz();
bindProv();
bindSim();
app.addEventListener("change", function(e){
  var k = e.target.getAttribute && e.target.getAttribute("data-k"); if (!k) return;
  st[k] = e.target.checked; save();
  if (k.indexOf("day:")===0) { var tb = document.getElementById("tb-dia-"+k.slice(4)); if (tb) tb.classList.toggle("done", e.target.checked); }
});
app.addEventListener("click", function(e){ var b = e.target.closest && e.target.closest("[role=tab]"); if (!b) return; activate(b.getAttribute("data-tg"), b.getAttribute("data-tk"), true); var sec = b.closest("section"); if (sec && sec.getBoundingClientRect().top < 0) sec.scrollIntoView(); });
var ws = document.getElementById("weeksel"); if (ws) ws.addEventListener("change", function(e){ if (e.target.value) location.href = e.target.value; });
function openHash(){ var h = location.hash.replace("#",""); if (!h) return;
  for (var g in TABGROUPS) if (TABGROUPS[g].indexOf(h) >= 0) { activate(g, h, false); return; }
  var el = document.getElementById(h); if (!el) return; if (el.tagName==="DETAILS") el.open = true; el.scrollIntoView(); }
window.addEventListener("hashchange", openHash);
setTimeout(openHash, 0);
})();
