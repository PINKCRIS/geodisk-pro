<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Laboratorio del Macizo Rocoso</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Concepto: cuaderno de campo del geólogo. Una barra fija muestra los tres resultados vivos (RQD, Q, RMR);
   cada panel pone los controles a un lado y el resultado al otro; el RQD del paso 1 alimenta a Q y RMR. */
:root{
  --bg:#eef1f1; --surface:#fbfcfc; --surface2:#e3e9ea; --ink:#12191c; --muted:#56666c; --line:#cdd7d9;
  --accent:#0e6a74; --accent-ink:#ffffff; --bar:#eef1f1;
  --j1:#d8483c; --j2:#2b74c9; --j3:#b98a0a;
  --disp:'Barlow Semi Condensed','Arial Narrow',system-ui,sans-serif;
  --body:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0f1517; --surface:#161e21; --surface2:#1f2a2e; --ink:#e6edee; --muted:#93a6ab; --line:#2b3a3f;
    --accent:#53c2cc; --accent-ink:#06282c; --bar:#0f1517;
    --j1:#ff7a6e; --j2:#6aa8f0; --j3:#f0c040; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#0f1517; --surface:#161e21; --surface2:#1f2a2e; --ink:#e6edee; --muted:#93a6ab; --line:#2b3a3f;
  --accent:#53c2cc; --accent-ink:#06282c; --bar:#0f1517;
  --j1:#ff7a6e; --j2:#6aa8f0; --j3:#f0c040; color-scheme:dark;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.5}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--bar)}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top{padding-block:28px 20px}
.kicker{font:500 12px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 12px}
h1{font:700 clamp(32px,5.4vw,52px)/1 var(--disp);letter-spacing:-.005em;margin:0 0 12px;text-wrap:balance}
.lede{max-width:64ch;color:var(--muted);margin:0}
h2{font:600 clamp(22px,3vw,30px)/1.1 var(--disp);margin:0 0 8px;text-wrap:balance}
h3{font:600 19px/1.15 var(--disp);margin:0}
p{margin:0 0 10px}
.muted{color:var(--muted)}
code,.mono{font-family:var(--mono)}

.barwrap{position:sticky;top:env(safe-area-inset-top,0px);z-index:31;background:var(--bar);border-bottom:1px solid var(--line);border-top:1px solid var(--line)}
.bar{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;padding-block:8px}
.tabbtn{font:inherit;color:var(--ink);background:transparent;border:1px solid transparent;border-bottom:3px solid transparent;border-radius:4px;padding:6px 8px 5px;text-align:left;cursor:pointer;min-width:0}
.tabbtn:hover{background:var(--surface2)}
.tabbtn[aria-selected="true"]{background:var(--surface);border-color:var(--line);border-bottom-color:var(--accent)}
.t-lab{display:flex;align-items:center;gap:6px;font:500 11px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.t-lab i{width:9px;height:9px;border-radius:50%;background:var(--line);display:inline-block;flex:none}
.t-val{display:block;font:600 22px/1.1 var(--disp);font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

main{padding-block:26px 18px}
.panel[hidden]{display:none!important}
.lead{max-width:74ch;margin-bottom:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:16px;min-width:0}
.card+.card{margin-top:16px}
.card-h{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}
.split{display:grid;grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:18px;align-items:start}
.split>div{min-width:0}
.split>div>.card+.card{margin-top:16px}
@media (max-width:880px){.split{grid-template-columns:minmax(0,1fr)}}
.hint{color:var(--muted);font-size:13.5px;margin:0 0 10px}

.btn{font:500 14px var(--body);border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:7px 12px;border-radius:4px;cursor:pointer}
.btn:hover{border-color:var(--accent)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn.pri{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.actions{display:flex;gap:8px;flex-wrap:wrap}
.seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:5px;overflow:hidden;margin-bottom:16px;background:var(--surface)}
.seg button{font:500 14px var(--body);border:0;background:transparent;color:var(--ink);padding:9px 14px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink)}
.seg button+button{border-left:1px solid var(--line)}

.row{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:center;margin-top:10px}
.row label,.fld>label,.chk{font-size:14px;font-weight:500}
.row output,.out{font:500 14px var(--mono);font-variant-numeric:tabular-nums;min-width:4.2em;text-align:right}
input[type=range]{width:100%;accent-color:var(--accent);margin:0}
input[type=checkbox]{accent-color:var(--accent);width:16px;height:16px;margin:0 6px 0 0;vertical-align:-3px}
select{width:100%;font:14px var(--body);color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:8px 8px}
.fld{margin-top:14px}
.fld:first-child{margin-top:0}
.fld>label{display:flex;justify-content:space-between;gap:8px;margin-bottom:5px}
.fld>label small{font:400 12px var(--mono);color:var(--muted)}
.chk{display:inline-flex;align-items:center}

#core-svg,#palm-svg,#q-mx{display:block;width:100%;height:auto;max-width:100%}
#core-svg{cursor:crosshair;touch-action:manipulation;min-width:620px}
.calc{margin-top:14px;padding:12px 14px;background:var(--surface2);border-radius:5px;font:14px/1.7 var(--mono)}
.calc b{font-weight:600}
.num{font:700 clamp(40px,7vw,58px)/1 var(--disp);font-variant-numeric:tabular-nums}
.chip{display:inline-block;font:600 13px/1 var(--mono);padding:6px 10px;border-radius:3px;margin-left:12px;vertical-align:middle}
.mainnum{display:flex;align-items:center;flex-wrap:wrap;gap:4px}

.gz{position:relative;height:18px;margin:16px 0 0;border-radius:3px}
.gs{position:absolute;top:0;bottom:0;border-right:2px solid var(--surface)}
.gs:first-child{border-radius:3px 0 0 3px}
.gs:last-of-type{border-right:0}
.gm{position:absolute;top:-11px;width:0;height:0;transform:translateX(-50%);border-left:7px solid transparent;border-right:7px solid transparent;border-top:11px solid var(--ink);z-index:2}
.gm::after{content:"";position:absolute;left:-1px;top:-11px;width:2px;height:31px;background:var(--ink)}
.gt{position:relative;height:20px;margin-top:6px;font:11.5px var(--mono);color:var(--muted)}
.gt span{position:absolute;white-space:nowrap}

.tbl{width:100%;border-collapse:collapse;font-size:14px}
.tbl th{font:500 11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;text-align:left;color:var(--muted);padding:6px 8px;border-bottom:1px solid var(--line)}
.tbl td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr.on td{background:var(--surface2);font-weight:600}
.tbl .sw{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:8px;vertical-align:-1px}
.scroll{overflow-x:auto;max-width:100%}
.scroll .tbl.wide{min-width:520px}
.scroll .tbl.mid{min-width:380px}
.t-lab .n{font-weight:500}
@media (max-width:520px){.t-lab .n{display:none}.t-lab{letter-spacing:.02em;font-size:10px;gap:5px}.t-val{font-size:19px}.tabbtn{padding:6px 5px 5px}}

.setrow{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:center;margin-top:10px}
.setrow .dot{width:10px;height:10px;border-radius:2px;display:inline-block;margin-right:6px}

.fac3{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-top:16px}
.fac{border:1px solid var(--line);border-radius:5px;padding:12px;background:var(--bg)}
.fac .fh{display:flex;justify-content:space-between;gap:8px;font-size:13px}
.fac .fh code{color:var(--muted);font-size:12px}
.fac .fv{font:700 30px/1.2 var(--disp);font-variant-numeric:tabular-nums}
.trk{height:6px;background:var(--surface2);border-radius:3px;overflow:hidden;margin:4px 0 8px}
.trk i{display:block;height:100%;background:var(--accent)}
.fac p{font-size:13px;color:var(--muted);margin:0}

.eq{font:500 17px/2.2 var(--mono);margin-top:14px;overflow-x:auto}
.eq2{font:500 15px/2.2 var(--mono);color:var(--muted);overflow-x:auto}
.frac{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 .2em;line-height:1.25;font-size:.92em}
.frac>span:first-child{border-bottom:1.5px solid currentColor;padding:0 .3em}
.frac>span:last-child{padding:0 .3em}

.qleg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:6px 14px;font-size:12.5px;margin-top:12px}
.qleg span{display:flex;gap:7px;align-items:center;padding:2px 4px;border-radius:3px}
.qleg i{width:14px;height:14px;border-radius:2px;flex:none}
.qleg .on{outline:2px solid var(--ink);font-weight:600}
.minfo{min-height:2.9em;margin-top:8px;font:13px/1.5 var(--mono);color:var(--muted)}
@media (max-width:640px){.cell-txt{display:none}}

.prow{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 4.6em;gap:10px;align-items:center;padding:7px 0;border-bottom:1px solid var(--line);font-size:14px}
.prow .pb{height:8px;background:var(--surface2);border-radius:4px;overflow:hidden}
.prow .pb i{display:block;height:100%;background:var(--accent)}
.prow .pv{font:500 14px var(--mono);text-align:right;font-variant-numeric:tabular-nums}
.prow.adj .pn{color:var(--muted)}

.det{border:1px solid var(--line);border-radius:5px;background:var(--surface);margin-top:14px}
.det summary{cursor:pointer;padding:10px 14px;font-weight:600;font-size:14px}
.det>div{padding:0 14px 14px}
.try{margin:16px 0 0;padding:12px 14px;border-left:3px solid var(--accent);background:var(--surface2);border-radius:0 5px 5px 0;font-size:14px}
.try b{font:500 11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent);display:block;margin-bottom:4px}
.guesses{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin:10px 0}
.guess{font:500 14px var(--body);padding:9px 6px;border-radius:4px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer;text-align:center}
.guess small{display:block;font:11.5px var(--mono);color:var(--muted)}
.guess:disabled{cursor:default}
.guess.ok{border-color:#1a8a3f;box-shadow:inset 0 0 0 2px #1a8a3f}
.guess.bad{border-color:#dc2626;box-shadow:inset 0 0 0 2px #dc2626}
.legend3{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--muted);margin:8px 0 0}
.legend3 i{display:inline-block;width:14px;height:10px;border-radius:2px;margin-right:6px;vertical-align:0}
.gl{margin-top:16px}
.gl:first-of-type{margin-top:0}
.gl h3{margin-bottom:4px;display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.gl h3 span{font:600 15px var(--mono)}
.read p{max-width:70ch}
footer{padding-block:8px 40px;color:var(--muted);font-size:13px;max-width:78ch}
@media (prefers-reduced-motion:no-preference){.trk i,.prow .pb i,.gm{transition:width .25s,left .25s}}
</style>
</head>
<body>

<div class="wrap top">
  <p class="kicker">Geomecánica · clasificación de macizos</p>
  <h1>Laboratorio del macizo rocoso</h1>
  <p class="lede">Mueve los parámetros y mira cómo cambian el RQD, el índice Q de Barton y el RMR de Bieniawski. El RQD del primer paso alimenta a los otros dos, igual que en un informe de campo.</p>
</div>

<div class="barwrap">
  <nav class="wrap bar" id="bar" aria-label="Pasos del laboratorio">
    <button type="button" class="tabbtn" id="t-rqd" data-tab="rqd" aria-selected="true"><span class="t-lab"><i id="d-rqd"></i><b class="n">1 · </b>RQD</span><span class="t-val" id="v-rqd">–</span></button>
    <button type="button" class="tabbtn" id="t-q" data-tab="q" aria-selected="false"><span class="t-lab"><i id="d-q"></i><b class="n">2 · </b>Q Barton</span><span class="t-val" id="v-q">–</span></button>
    <button type="button" class="tabbtn" id="t-rmr" data-tab="rmr" aria-selected="false"><span class="t-lab"><i id="d-rmr"></i><b class="n">3 · </b>RMR</span><span class="t-val" id="v-rmr">–</span></button>
    <button type="button" class="tabbtn" id="t-comparar" data-tab="comparar" aria-selected="false"><span class="t-lab"><i style="background:var(--accent)"></i><b class="n">4 · </b>Comparar</span><span class="t-val">3 en 1</span></button>
  </nav>
</div>

<main class="wrap" id="main">

<!-- ================= 1 · RQD ================= -->
<section class="panel" id="p-rqd">
  <div class="lead">
    <h2>RQD: cuánta roca se conserva en trozos de 10 cm o más</h2>
    <p>El RQD se obtiene de los testigos de perforación. Mide qué porcentaje de la roca extraída se conserva en trozos de más de 10 cm y permite estimar rápido el grado de fracturamiento del macizo.</p>
    <details class="det"><summary>Fórmulas y definiciones</summary><div>
      <p><b>Con testigos:</b> RQD = (suma de los trozos de 10 cm o más ÷ longitud total del tramo) × 100.</p>
      <p><b>Sin testigos, con juntas visibles en afloramiento o túnel (Palmström, 1982):</b> RQD = 115 − 3,3 · Jv. Si Jv &lt; 4,5, el RQD vale 100.</p>
      <p><b>Jv</b> es el número de juntas por metro cúbico: Jv = 1/S₁ + 1/S₂ + 1/S₃ + …, donde S₁, S₂, S₃ son los espaciamientos medios, en metros, de cada familia de discontinuidades.</p>
    </div></details>
  </div>

  <div class="seg" role="group" aria-label="Fuente del RQD">
    <button type="button" id="m-core" aria-pressed="true">Con testigos</button>
    <button type="button" id="m-palm" aria-pressed="false">Sin testigos · Palmström</button>
  </div>

  <div class="card" id="c-core">
    <div class="card-h"><h3>Tramo de testigo de 100 cm</h3>
      <div class="actions"><button type="button" class="btn" id="b-shuffle">Redistribuir</button><button type="button" class="btn" id="b-challenge">Reto</button></div>
    </div>
    <p class="hint" id="core-hint">Toca el testigo para abrir una fractura; toca una fractura para cerrarla. Cuentan los trozos de 10 cm o más (medidas en cm).</p>
    <div class="scroll"><svg id="core-svg" viewBox="0 0 1000 150" role="img" aria-label="Tramo de testigo de 100 centímetros con fracturas"></svg></div>
    <div class="legend3"><span><i style="background:var(--accent)"></i>≥ 10 cm: cuenta</span><span><i style="background:var(--surface2);border:1px solid var(--muted)"></i>&lt; 10 cm: no cuenta</span></div>
    <div class="row"><label for="n-frac">Fracturas</label><input type="range" id="n-frac" min="0" max="30" value="7"><output id="n-out" for="n-frac">7</output></div>
    <div class="calc" id="core-calc"></div>
    <div id="challenge" hidden>
      <p style="margin:14px 0 0" id="ch-msg"></p>
      <div class="guesses" id="guesses"></div>
      <div class="actions"><button type="button" class="btn pri" id="ch-next" hidden>Siguiente caso</button><span class="muted mono" id="ch-score" style="align-self:center;font-size:13px"></span></div>
    </div>
  </div>

  <div class="card" id="c-palm" hidden>
    <div class="card-h"><h3>Pared de túnel o afloramiento · 2 m × 1,2 m</h3></div>
    <p class="hint">Activa cada familia de juntas y ajusta su espaciamiento medio. El bloque sombreado es el bloque típico entre las familias 1 y 2.</p>
    <svg id="palm-svg" viewBox="0 0 640 384" role="img" aria-label="Pared con tres familias de juntas"></svg>
    <div id="palm-ctl"></div>
    <div class="calc" id="palm-calc"></div>
  </div>

  <div class="card" id="c-rqdres">
    <div class="card-h"><h3>Resultado y clasificación</h3></div>
    <div class="mainnum" id="rqd-big"></div>
    <div id="g-rqd"></div>
    <div style="margin-top:16px" class="scroll"><table class="tbl" id="t-rqdtab"></table></div>
    <p class="hint" style="margin-top:8px">Tabla 5 · Clasificación de la calidad del macizo rocoso según el índice RQD (Deere).</p>
  </div>

  <div class="try"><b>Para probar</b>Parte un trozo de 15 cm por la mitad: de contar 15 cm pasas a contar 0. Una fractura bien puesta puede bajar mucho el RQD, y diez fracturas juntas en un solo tramo casi no lo cambian.</div>
</section>

<!-- ================= 2 · Q ================= -->
<section class="panel" id="p-q" hidden>
  <div class="lead">
    <h2>Q de Barton: bloques, juntas y terreno en un solo número</h2>
    <p>Es un índice numérico de 0,001 a 1000 que clasifica la calidad del macizo combinando el tamaño de los bloques, la rugosidad y alteración de las juntas, el agua y los esfuerzos del terreno. Sirve para estimar con rapidez la calidad de la roca y qué soporte necesita.</p>
    <details class="det"><summary>Tabla 6 · Parámetros del índice Q</summary><div class="scroll"><table class="tbl" style="min-width:560px">
      <thead><tr><th>Parámetro</th><th>Descripción</th><th>Rango de valores</th></tr></thead>
      <tbody>
      <tr><td><b>RQD</b></td><td>Calidad del testigo</td><td>0–100 (mínimo nominal 10)</td></tr>
      <tr><td><b>Jn</b></td><td>Número de familias de juntas</td><td>0,5–1 (roca masiva) a 20 (roca triturada)</td></tr>
      <tr><td><b>Jr</b></td><td>Rugosidad de las juntas</td><td>0,5 (planas y pulidas) a 4 (discontinuas)</td></tr>
      <tr><td><b>Ja</b></td><td>Alteración de las juntas</td><td>0,75 (cementadas) a 20 (zonas gruesas de arcilla)</td></tr>
      <tr><td><b>Jw</b></td><td>Reducción por agua</td><td>1 (excavación seca) a 0,05 (afluencia excepcional mantenida)</td></tr>
      <tr><td><b>SRF</b></td><td>Reducción por esfuerzos</td><td>0,5 (alta cobertura) a 20 (rockburst fuerte, deformación plástica fuerte)</td></tr>
      </tbody></table></div></details>
  </div>

  <div class="split">
    <div>
      <div class="card">
        <h3>Parámetros</h3>
        <div class="fld"><label for="q-rqd"><span>RQD</span><small id="q-rqd-lab"></small></label>
          <div class="chk" style="margin-bottom:6px"><input type="checkbox" id="q-use" checked><label for="q-use" style="font-weight:400">Usar el RQD del paso 1</label></div>
          <div class="row" style="margin-top:0"><span></span><input type="range" id="q-rqd" min="0" max="100" step="1" value="70"><output id="q-rqd-o" for="q-rqd"></output></div></div>
        <div class="fld"><label for="q-jn"><span>Jn · familias de juntas</span><small>0,5–20</small></label><select id="q-jn"></select></div>
        <div class="fld"><label for="q-jr"><span>Jr · rugosidad</span><small>0,5–4</small></label><select id="q-jr"></select></div>
        <div class="fld"><label for="q-ja"><span>Ja · alteración</span><small>0,75–20</small></label><select id="q-ja"></select></div>
        <div class="fld"><label for="q-jw"><span>Jw · agua</span><small>1–0,05</small></label><select id="q-jw"></select></div>
        <div class="fld"><label for="q-srf"><span>SRF · esfuerzos</span><small>0,5–20</small></label><select id="q-srf"></select></div>
      </div>
      <div class="card">
        <h3>Excavación</h3>
        <div class="fld"><label for="q-span"><span>Luz o altura</span></label><div class="row" style="margin-top:0"><span></span><input type="range" id="q-span" min="2" max="30" step="0.5" value="8"><output id="q-span-o" for="q-span"></output></div></div>
        <div class="fld"><label for="q-esr"><span>Uso (ESR)</span></label><select id="q-esr"></select></div>
      </div>
    </div>
    <div>
      <div class="card">
        <div class="card-h"><h3>Índice Q</h3></div>
        <div class="mainnum" id="q-main"></div>
        <div class="eq" id="q-eq"></div>
        <div class="eq2" id="q-eq2"></div>
        <div id="g-q"></div>
        <div class="fac3" id="q-fac"></div>
      </div>
      <div class="card">
        <div class="card-h"><h3>Mapa de Q: tamaño de bloque contra resistencia entre bloques</h3></div>
        <p class="hint">Cada celda es una combinación de RQD/Jn (horizontal) y Jr/Ja (vertical). El color sale de multiplicarlas por tu Jw/SRF. Toca una celda para leerla.</p>
        <svg id="q-mx" viewBox="0 0 640 400" role="img" aria-label="Mapa de Q con tu caso marcado"></svg>
        <div class="minfo" id="m-info"></div>
        <div class="qleg" id="q-leg"></div>
      </div>
      <div class="card">
        <div class="card-h"><h3>Soporte y luz sin soportar</h3></div>
        <div id="q-sup"></div>
      </div>
    </div>
  </div>
  <div class="try"><b>Para probar</b>Pasa Jw de excavación seca a afluencia grande y mira cómo se corren los colores del mapa mientras tu punto se queda quieto: el agua no cambia el bloque ni la junta, pero sí el resultado final.</div>
</section>

<!-- ================= 3 · RMR ================= -->
<section class="panel" id="p-rmr" hidden>
  <div class="lead">
    <h2>RMR de Bieniawski: cinco parámetros que suman hasta 100 puntos</h2>
    <p>Se suman los puntos de la resistencia de la roca, el RQD, el espaciamiento de las discontinuidades, su estado y el agua. Después se resta un ajuste por la orientación de las juntas respecto a la excavación.</p>
  </div>
  <div class="split">
    <div>
      <div class="card">
        <h3>Parámetros</h3>
        <div class="fld"><label for="r-ucs"><span>Resistencia a compresión simple</span><small>0–15 pts</small></label><select id="r-ucs"></select></div>
        <div class="fld"><label><span>RQD (viene del paso 1)</span><small>3–20 pts</small></label><div class="calc" style="margin-top:0;padding:8px 12px" id="r-rqdline"></div></div>
        <div class="fld"><label for="r-sp"><span>Espaciamiento de discontinuidades</span><small>5–20 pts</small></label><select id="r-sp"></select></div>
        <div class="fld"><label for="r-cond"><span>Estado de las discontinuidades</span><small>0–30 pts</small></label><select id="r-cond"></select></div>
        <div class="fld"><label for="r-wat"><span>Agua subterránea</span><small>0–15 pts</small></label><select id="r-wat"></select></div>
        <div class="fld"><label for="r-ori"><span>Orientación de las juntas (túneles)</span><small>0 a −12</small></label><select id="r-ori"></select></div>
      </div>
    </div>
    <div>
      <div class="card">
        <div class="card-h"><h3>Valoración RMR</h3></div>
        <div class="mainnum" id="r-main"></div>
        <div id="g-rmr"></div>
        <div style="margin-top:16px" id="r-rows"></div>
      </div>
      <div class="card">
        <div class="card-h"><h3>Clases del macizo según RMR</h3></div>
        <div class="scroll"><table class="tbl wide" id="r-tab"></table></div>
      </div>
    </div>
  </div>
  <div class="try"><b>Para probar</b>Baja el estado de las discontinuidades de 25 a 10 puntos y vuelve a Q: sube Ja de 2 a 6 y compara cuánto pierde cada sistema con el mismo cambio de campo.</div>
</section>

<!-- ================= 4 · Comparar ================= -->
<section class="panel" id="p-comparar" hidden>
  <div class="lead">
    <h2>Los tres sistemas, sobre el mismo macizo</h2>
    <p>Cada escala mide algo parecido con otra regla. Aquí ves dónde cae tu caso en cada una y si las dos clasificaciones principales se entienden entre sí.</p>
  </div>
  <div class="split" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">
    <div class="card">
      <div class="gl"><h3>RQD <span id="c-v1"></span></h3><div id="c-g1"></div></div>
      <div class="gl" style="margin-top:34px"><h3>Q de Barton <span id="c-v2"></span></h3><div id="c-g2"></div></div>
      <div class="gl" style="margin-top:34px"><h3>RMR <span id="c-v3"></span></h3><div id="c-g3"></div></div>
    </div>
    <div class="card read" id="c-read"></div>
  </div>
  <div class="card">
    <div class="card-h"><h3>Escalera de equivalencias</h3></div>
    <p class="hint">Q equivalente según la correlación empírica RMR = 9 · ln Q + 44 (Bieniawski, 1989). Es una guía: los dos sistemas miden con parámetros distintos y la dispersión es grande.</p>
    <div class="scroll"><table class="tbl mid" id="c-eq"></table></div>
  </div>
</section>
</main>

<footer class="wrap">Material didáctico con valores simplificados de las tablas de Deere (RQD), Barton (Q) y Bieniawski (RMR). Para diseño de soporte usa las tablas completas, los datos de campo y el criterio de un ingeniero geotécnico.</footer>

<script>
(function(){
'use strict';
var $=function(s){return document.querySelector(s);};
var num=function(a,b){return a-b;};
function fm(v,d){var s=(d===undefined)?String(v):v.toFixed(d);return s.replace('.',',');}
function fq(q){return fm(q,q>=100?0:q>=10?1:q>=0.1?2:3);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function sg(v){return v<0?'−'+Math.abs(v):(v>0?'+'+v:'0');}

/* ---------- datos ---------- */
var C5=['#1a8a3f','#84cc16','#facc15','#f97316','#dc2626'];
var C5T=['#ffffff','#1f2937','#1f2937','#ffffff','#ffffff'];
var ROM=['I','II','III','IV','V'];
var QCOL=['#7a1b1b','#b42323','#e0502a','#f08a24','#f2c230','#b8d93a','#6cc04a','#2e9e4f','#14703a'];
function txtOn(h){var r=parseInt(h.substr(1,2),16),g=parseInt(h.substr(3,2),16),b=parseInt(h.substr(5,2),16);return (0.299*r+0.587*g+0.114*b)/255>0.6?'#1f2937':'#ffffff';}

var RQDC=[{lo:0,hi:25,n:'Muy mala',c:5},{lo:25,hi:50,n:'Mala',c:4},{lo:50,hi:75,n:'Regular',c:3},{lo:75,hi:90,n:'Buena',c:2},{lo:90,hi:100,n:'Excelente',c:1}];
function rqdCls(v){for(var i=0;i<4;i++){if(v<RQDC[i].hi)return RQDC[i];}return RQDC[4];}

var QC=[{lo:0.001,hi:0.01,n:'Excepcionalmente mala'},{lo:0.01,hi:0.1,n:'Extremadamente mala'},{lo:0.1,hi:1,n:'Muy mala'},{lo:1,hi:4,n:'Mala'},{lo:4,hi:10,n:'Media'},{lo:10,hi:40,n:'Buena'},{lo:40,hi:100,n:'Muy buena'},{lo:100,hi:400,n:'Extremadamente buena'},{lo:400,hi:1000,n:'Excepcionalmente buena'}];
function qIdx(q){for(var i=0;i<8;i++){if(q<QC[i].hi)return i;}return 8;}

var RC=[
 {min:81,n:'Muy buena',coh:'> 400 kPa',fr:'> 45°',t:'20 años con 15 m de luz'},
 {min:61,n:'Buena',coh:'300–400 kPa',fr:'35–45°',t:'1 año con 10 m de luz'},
 {min:41,n:'Media',coh:'200–300 kPa',fr:'25–35°',t:'1 semana con 5 m de luz'},
 {min:21,n:'Mala',coh:'100–200 kPa',fr:'15–25°',t:'10 horas con 2,5 m de luz'},
 {min:-99,n:'Muy mala',coh:'< 100 kPa',fr:'< 15°',t:'30 minutos con 1 m de luz'}];
function rmrIdx(v){return v>=81?0:v>=61?1:v>=41?2:v>=21?3:4;}

var JN=[{v:1,t:'Roca masiva, sin juntas o muy pocas (0,5–1)'},{v:2,t:'Una familia de juntas'},{v:3,t:'Una familia y juntas aleatorias'},{v:4,t:'Dos familias'},{v:6,t:'Dos familias y juntas aleatorias'},{v:9,t:'Tres familias'},{v:12,t:'Tres familias y juntas aleatorias'},{v:15,t:'Cuatro o más familias, muy fracturada'},{v:20,t:'Roca triturada, parecida a un suelo'}];
var JR=[{v:4,t:'Juntas discontinuas'},{v:3,t:'Rugosas o irregulares, onduladas'},{v:2,t:'Lisas, onduladas'},{v:1.5,t:'Pulidas (espejo de falla), onduladas'},{v:1.5,t:'Rugosas o irregulares, planas'},{v:1,t:'Lisas, planas'},{v:0.5,t:'Pulidas (espejo de falla), planas'}];
var JA=[{v:0.75,t:'Cementadas, relleno duro e impermeable'},{v:1,t:'Paredes sanas, solo manchas de oxidación'},{v:2,t:'Ligeramente alteradas, recubrimiento no blando'},{v:3,t:'Recubrimiento de limo o arena, sin arcilla'},{v:4,t:'Recubrimiento de arcilla blanda o de baja fricción'},{v:6,t:'Relleno de arena o roca triturada, sin arcilla'},{v:8,t:'Relleno de arcilla sobreconsolidada, delgado'},{v:12,t:'Relleno de arcilla blanda o expansiva moderada'},{v:20,t:'Zonas gruesas de arcilla'}];
var JW=[{v:1,t:'Excavación seca o afluencia local pequeña'},{v:0.66,t:'Afluencia media, lavado ocasional de rellenos'},{v:0.5,t:'Afluencia grande en roca competente'},{v:0.33,t:'Afluencia grande con lavado de rellenos'},{v:0.2,t:'Afluencia excepcional que decae con el tiempo'},{v:0.05,t:'Afluencia excepcional mantenida'}];
var SRF=[{v:0.5,t:'Esfuerzo alto, roca muy compacta (alta cobertura)'},{v:1,t:'Esfuerzo medio, condición favorable'},{v:2.5,t:'Esfuerzo bajo, cerca de la superficie'},{v:5,t:'Zona de debilidad aislada con arcilla, o juntas abiertas sueltas'},{v:7.5,t:'Varias zonas de cizalla en roca competente'},{v:10,t:'Varias zonas de debilidad con arcilla, o rockburst moderado'},{v:15,t:'Roca fluyente o deformación plástica moderada'},{v:20,t:'Rockburst fuerte o deformación plástica fuerte'}];
var ESR=[{v:3.5,t:'Excavación minera temporal'},{v:1.6,t:'Minería permanente, túneles de agua, galerías'},{v:1.3,t:'Almacenes, túneles viales menores, cámaras de oscilación'},{v:1,t:'Centrales subterráneas, túneles viales o ferroviarios mayores'},{v:0.8,t:'Estaciones, instalaciones públicas o deportivas'}];

var UCS=[{r:15,t:'> 250 MPa'},{r:12,t:'100–250 MPa'},{r:7,t:'50–100 MPa'},{r:4,t:'25–50 MPa'},{r:2,t:'5–25 MPa'},{r:1,t:'1–5 MPa'},{r:0,t:'< 1 MPa'}];
var SPC=[{r:20,t:'Más de 2 m'},{r:15,t:'0,6–2 m'},{r:10,t:'0,2–0,6 m'},{r:8,t:'0,06–0,2 m'},{r:5,t:'Menos de 0,06 m'}];
var CND=[{r:30,t:'Muy rugosas, sin continuidad, sin separación, paredes sanas'},{r:25,t:'Ligeramente rugosas, separación < 1 mm, paredes poco alteradas'},{r:20,t:'Ligeramente rugosas, separación < 1 mm, paredes muy alteradas'},{r:10,t:'Pulidas, o relleno < 5 mm, o separación de 1–5 mm, continuas'},{r:0,t:'Relleno blando > 5 mm, o separación > 5 mm, continuas'}];
var WAT=[{r:15,t:'Seco'},{r:10,t:'Húmedo'},{r:7,t:'Mojado'},{r:4,t:'Con goteo'},{r:0,t:'Con flujo'}];
var ORI=[{r:0,t:'Muy favorable'},{r:-2,t:'Favorable'},{r:-5,t:'Regular'},{r:-10,t:'Desfavorable'},{r:-12,t:'Muy desfavorable'}];

/* ---------- estado ---------- */
var S={
  tab:'rqd',mode:'core',breaks:[9,24,33,48,54,71,85],seed:7,
  sets:[{on:true,s:0.2},{on:true,s:0.25},{on:true,s:0.5}],
  ch:{on:false,breaks:[],answered:false,guess:-1,right:0,tries:0},
  q:{use:true,rqd:70,jn:5,jr:4,ja:2,jw:0,srf:2,span:8,esr:2},
  r:{ucs:2,sp:3,cond:2,wat:1,ori:2}
};

/* ---------- cálculo ---------- */
function pieces(br){var a=[0].concat(br.slice().sort(num),[100]),o=[];for(var i=0;i<a.length-1;i++){o.push(Math.round((a[i+1]-a[i])*10)/10);}return o;}
function coreRqd(br){var s=0;pieces(br).forEach(function(l){if(l>=10)s+=l;});return Math.round(s*10)/10;}
function palm(){var jv=0;S.sets.forEach(function(x){if(x.on)jv+=1/x.s;});var r=jv<4.5?100:115-3.3*jv;return {jv:jv,rqd:clamp(r,0,100)};}
function rqd(){return S.mode==='core'?coreRqd(S.breaks):palm().rqd;}
function qCalc(){
  var rq=S.q.use?rqd():S.q.rqd,r=Math.max(rq,10);
  var jn=JN[S.q.jn].v,jr=JR[S.q.jr].v,ja=JA[S.q.ja].v,jw=JW[S.q.jw].v,srf=SRF[S.q.srf].v;
  var a=r/jn,b=jr/ja,c=jw/srf;
  return {rq:rq,r:r,jn:jn,jr:jr,ja:ja,jw:jw,srf:srf,a:a,b:b,c:c,Q:a*b*c};
}
function rqdRating(v){return v>=90?20:v>=75?17:v>=50?13:v>=25?8:3;}
function rmrCalc(){
  var rq=rqd(),p=[
    {k:'Resistencia de la roca',v:UCS[S.r.ucs].r,max:15},
    {k:'RQD',v:rqdRating(rq),max:20},
    {k:'Espaciamiento',v:SPC[S.r.sp].r,max:20},
    {k:'Estado de las juntas',v:CND[S.r.cond].r,max:30},
    {k:'Agua subterránea',v:WAT[S.r.wat].r,max:15}],basic=0;
  p.forEach(function(x){basic+=x.v;});
  var adj=ORI[S.r.ori].r,rmrp=basic-WAT[S.r.wat].r+15;
  return {parts:p,basic:basic,adj:adj,total:basic+adj,rmrp:rmrp,gsi:rmrp-5,rq:rq};
}

/* ---------- gráficos genéricos ---------- */
function gauge(sel,segs,v,pos,ticks){
  var h='<div class="gz">';
  segs.forEach(function(s){h+='<span class="gs" style="left:'+(pos(s.a)*100)+'%;width:'+((pos(s.b)-pos(s.a))*100)+'%;background:'+s.c+'"></span>';});
  h+='<span class="gm" style="left:'+(clamp(pos(v),0,1)*100)+'%"></span></div><div class="gt">';
  ticks.forEach(function(t){var p=pos(t.v),tr=p<=0.001?'0':p>=0.999?'-100%':'-50%';h+='<span style="left:'+(p*100)+'%;transform:translateX('+tr+')">'+t.l+'</span>';});
  $(sel).innerHTML=h+'</div>';
}
function posLin(a,b){return function(v){return (v-a)/(b-a);};}
function posLog(a,b){var la=Math.log(a),lb=Math.log(b);return function(v){return (Math.log(Math.max(v,a/10))-la)/(lb-la);};}
function chipHtml(txt,col){return '<span class="chip" style="background:'+col+';color:'+txtOn(col)+'">'+txt+'</span>';}
function gaugeRqd(sel,v){
  gauge(sel,RQDC.map(function(c){return {a:c.lo,b:c.hi,c:C5[c.c-1]};}),v,posLin(0,100),[0,25,50,75,90,100].map(function(x){return {v:x,l:String(x)};}));
}
function gaugeQ(sel,v){
  gauge(sel,QC.map(function(c,i){return {a:c.lo,b:c.hi,c:QCOL[i]};}),v,posLog(0.001,1000),[0.001,0.01,0.1,1,10,100,1000].map(function(x){return {v:x,l:fm(x)};}));
}
function gaugeRmr(sel,v){
  var b=[0,21,41,61,81,100],cc=[4,3,2,1,0];
  gauge(sel,cc.map(function(c,i){return {a:b[i],b:b[i+1],c:C5[c]};}),clamp(v,0,100),posLin(0,100),[0,20,40,60,80,100].map(function(x){return {v:x,l:String(x)};}));
}

/* ---------- RQD: testigo ---------- */
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function genBreaks(n,seed){
  var r=rng(seed),b=[],tries=0;
  while(b.length<n&&tries<3000){tries++;var p=Math.round((2+r()*96)*10)/10,ok=true;for(var i=0;i<b.length;i++){if(Math.abs(b[i]-p)<1.2){ok=false;break;}}if(ok)b.push(p);}
  return b.sort(num);
}
function drawCore(br,labels){
  var X0=20,K=9.6,a=[0].concat(br.slice().sort(num),[100]),n=a.length-1,o='';
  o+='<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" style="fill:var(--surface2)"/><line x1="0" y1="0" x2="0" y2="8" style="stroke:var(--muted);stroke-width:2;opacity:.55"/></pattern></defs>';
  for(var i=0;i<n;i++){
    var len=Math.round((a[i+1]-a[i])*10)/10,ok=len>=10;
    var xa=X0+a[i]*K+(i>0?3:0),xb=X0+a[i+1]*K-(i<n-1?3:0),w=Math.max(3,xb-xa);
    o+='<rect x="'+xa+'" y="44" width="'+w+'" height="62" rx="9" style="'+(ok?'fill:var(--accent)':'fill:url(#hatch);stroke:var(--muted);stroke-width:1.5')+'"/>';
    if(ok){
      o+='<rect x="'+(xa+4)+'" y="50" width="'+Math.max(0,w-8)+'" height="7" rx="3.5" style="fill:#fff;opacity:.22"/>';
      if(labels)o+='<text x="'+(xa+w/2)+'" y="86" text-anchor="middle" style="fill:var(--accent-ink);font:600 24px var(--mono)">'+(len%1===0?len:fm(len,1))+'</text>';
    }
  }
  br.forEach(function(b){var x=X0+b*K;o+='<g transform="translate('+x+' 26)"><circle r="10" style="fill:var(--surface);stroke:var(--muted);stroke-width:1.5"/><path d="M-4 -4L4 4M4 -4L-4 4" style="stroke:var(--ink);stroke-width:2;stroke-linecap:round;fill:none"/></g>';});
  o+='<line x1="'+X0+'" y1="120" x2="'+(X0+960)+'" y2="120" style="stroke:var(--muted);stroke-width:1.5"/>';
  for(var t=0;t<=100;t+=10){var xx=X0+t*K;o+='<line x1="'+xx+'" y1="114" x2="'+xx+'" y2="126" style="stroke:var(--muted);stroke-width:1.5"/><text x="'+xx+'" y="146" text-anchor="middle" style="fill:var(--muted);font:500 17px var(--mono)">'+t+'</text>';}
  $('#core-svg').innerHTML=o;
}
function pl(v){return v%1===0?String(v):fm(v,1);}
function updateCore(){
  var ch=S.ch,br=ch.on?ch.breaks:S.breaks,hide=ch.on&&!ch.answered;
  drawCore(br,!hide);
  if(!ch.on)$('#n-frac').value=S.breaks.length;
  $('#n-frac').disabled=ch.on;$('#b-shuffle').disabled=ch.on;
  $('#n-out').textContent=br.length;
  $('#b-challenge').textContent=ch.on?'Salir del reto':'Reto';
  $('#challenge').hidden=!ch.on;
  var p=pieces(br),ok=p.filter(function(l){return l>=10;}),sum=Math.round(ok.reduce(function(a,b){return a+b;},0)*10)/10;
  var lost=Math.round((100-sum)*10)/10;
  if(hide){
    $('#core-calc').innerHTML='<span class="muted">RQD = ?  Estima cuántos centímetros están en trozos de 10 cm o más.</span>';
  }else if(!ok.length){
    $('#core-calc').innerHTML='Ningún trozo llega a 10 cm<br><b>RQD = 0 %</b>';
  }else{
    $('#core-calc').innerHTML='Trozos ≥ 10 cm: '+ok.map(pl).join(' + ')+' = <b>'+pl(sum)+' cm</b><br>Trozos &lt; 10 cm (no cuentan): '+pl(lost)+' cm<br>RQD = '+pl(sum)+' ÷ 100 × 100 = <b>'+pl(sum)+' %</b>';
  }
  if(ch.on){
    var rq=coreRqd(br),cl=rqdCls(rq);
    $('#ch-msg').innerHTML=ch.answered
      ?(ch.guess===RQDC.indexOf(cl)?'<b>Correcto.</b> ':'<b>No coincide.</b> ')+'El RQD era '+pl(rq)+' %, clase «'+cl.n+'» ('+cl.lo+'–'+cl.hi+' %).'
      :'¿En qué clase de RQD cae este testigo?';
    var bs=document.querySelectorAll('#guesses .guess');
    for(var i=0;i<bs.length;i++){
      bs[i].disabled=ch.answered;
      bs[i].className='guess'+(ch.answered?(i===RQDC.indexOf(cl)?' ok':(i===ch.guess?' bad':'')):'');
    }
    $('#ch-next').hidden=!ch.answered;
    $('#ch-score').textContent='Aciertos: '+ch.right+' de '+ch.tries;
  }
}
function newChallenge(){
  var n=3+Math.floor(Math.random()*18);
  S.ch.breaks=genBreaks(n,Math.floor(Math.random()*1e9));S.ch.answered=false;S.ch.guess=-1;
}

/* ---------- RQD: Palmström ---------- */
function sFromT(t){var s=0.05*Math.pow(60,t/100);return s<1?Math.round(s*100)/100:Math.round(s*20)/20;}
function tFromS(s){return 100*Math.log(s/0.05)/Math.log(60);}
function drawPalm(){
  var W=640,H=384,sc=320,s=S.sets,g='',o='';
  var p1=s[0].s*sc,p2=s[1].s*sc,p3=s[2].s*sc*Math.SQRT2,o1=p1*0.4,o2=p2*0.55,o3=p3*0.3,x,c;
  o+='<defs><clipPath id="pclip"><rect width="640" height="384"/></clipPath></defs><rect width="640" height="384" style="fill:var(--surface2)"/>';
  if(s[0].on&&s[1].on){
    var i=Math.floor((W/2-o1)/p1),j=Math.floor((H/2-o2)/p2);
    g+='<rect x="'+(o1+i*p1)+'" y="'+(o2+j*p2)+'" width="'+p1+'" height="'+p2+'" style="fill:var(--accent);opacity:.3"/>';
  }
  if(s[0].on){for(x=o1;x<W;x+=p1)g+='<line x1="'+x+'" y1="0" x2="'+x+'" y2="'+H+'" stroke-width="2.5" style="stroke:var(--j1)"/>';}
  if(s[1].on){for(x=o2;x<H;x+=p2)g+='<line x1="0" y1="'+x+'" x2="'+W+'" y2="'+x+'" stroke-width="2.5" style="stroke:var(--j2)"/>';}
  if(s[2].on){for(c=o3;c<W+H;c+=p3)g+='<line x1="'+c+'" y1="0" x2="'+(c-H)+'" y2="'+H+'" stroke-width="2.5" style="stroke:var(--j3)"/>';}
  o+='<g clip-path="url(#pclip)">'+g+'</g>';
  o+='<g transform="translate(14 352)"><rect x="-6" y="-18" width="184" height="42" rx="4" style="fill:var(--surface);opacity:.9"/><line x1="0" y1="0" x2="160" y2="0" style="stroke:var(--ink);stroke-width:3"/><line x1="0" y1="-6" x2="0" y2="6" style="stroke:var(--ink);stroke-width:3"/><line x1="160" y1="-6" x2="160" y2="6" style="stroke:var(--ink);stroke-width:3"/><text x="80" y="18" text-anchor="middle" style="fill:var(--ink);font:500 13px var(--mono)">0,5 m</text></g>';
  $('#palm-svg').innerHTML=o;
}
function updatePalm(){
  drawPalm();
  var p=palm(),parts=[],vals=[];
  S.sets.forEach(function(x,i){$('#s'+i+'-o').textContent=fm(x.s,2)+' m';$('#s'+i+'-t').disabled=!x.on;if(x.on){parts.push('1/'+fm(x.s,2));vals.push(fm(1/x.s,1));}});
  var t='';
  if(!parts.length){t='Sin familias de juntas activas: Jv = 0<br>RQD = <b>100 %</b>';}
  else{
    t='Jv = '+parts.join(' + ')+'<br>Jv = '+vals.join(' + ')+' = <b>'+fm(p.jv,1)+' juntas/m³</b><br>';
    t+=p.jv<4.5?'Jv &lt; 4,5, entonces RQD = <b>100 %</b>':'RQD = 115 − 3,3 × '+fm(p.jv,1)+' = <b>'+fm(p.rqd,1)+' %</b>'+(p.jv>34.8?' (se limita a 0)':'');
  }
  $('#palm-calc').innerHTML=t;
}

/* ---------- panel RQD ---------- */
function updateRqd(){
  var core=S.mode==='core';
  $('#m-core').setAttribute('aria-pressed',core);$('#m-palm').setAttribute('aria-pressed',!core);
  $('#c-core').hidden=!core;$('#c-palm').hidden=core;
  if(core)updateCore();else updatePalm();
  var hideRes=core&&S.ch.on;
  $('#c-rqdres').hidden=hideRes;
  var r=Math.round(rqd()*10)/10,c=rqdCls(r);
  $('#rqd-big').innerHTML='<span class="num">'+pl(r).replace('.',',')+' %</span>'+chipHtml('Clase '+ROM[c.c-1]+' · '+c.n,C5[c.c-1]);
  gaugeRqd('#g-rqd',r);
  var rows='<thead><tr><th>RQD (%)</th><th>Calidad del macizo</th></tr></thead><tbody>';
  RQDC.forEach(function(k){rows+='<tr'+(k===c?' class="on"':'')+'><td class="mono">'+k.lo+'–'+k.hi+'</td><td><span class="sw" style="background:'+C5[k.c-1]+'"></span>'+k.n+'</td></tr>';});
  $('#t-rqdtab').innerHTML=rows+'</tbody>';
}

/* ---------- panel Q ---------- */
var FRAC_RANGES={a:[0.5,200],b:[0.02,6],c:[0.0025,2]};
function fillPct(v,r){return clamp((Math.log(v)-Math.log(r[0]))/(Math.log(r[1])-Math.log(r[0])),0,1)*100;}
function frac(a,b){return '<span class="frac"><span>'+a+'</span><span>'+b+'</span></span>';}
function interp(k,v){
  if(k==='a')return v<3?'Bloques muy pequeños: la roca se comporta casi como un suelo.':v<10?'Bloques pequeños a medianos.':v<30?'Bloques medianos a grandes.':'Bloques muy grandes: macizo casi continuo.';
  if(k==='b')return v<0.5?'Juntas muy débiles: los bloques deslizan con facilidad.':v<1?'Juntas débiles entre bloques.':v<2?'Resistencia al corte intermedia.':'Juntas con buena fricción: los bloques se traban.';
  return v<0.05?'Agua y esfuerzos muy desfavorables.':v<0.2?'Condición desfavorable.':v<0.5?'Condición moderada.':'Agua y esfuerzos poco problemáticos.';
}
function drawMatrix(c){
  var L=64,T=14,PW=560,PH=330,nx=13,ny=12,x0=Math.log10(0.5),x1=Math.log10(200),y0=Math.log10(0.02),y1=Math.log10(6);
  var dx=(x1-x0)/nx,dy=(y1-y0)/ny,cw=PW/nx,ch=PH/ny,o='';
  for(var i=0;i<nx;i++){for(var j=0;j<ny;j++){
    var xc=Math.pow(10,x0+(i+0.5)*dx),yc=Math.pow(10,y0+(j+0.5)*dy),q=xc*yc*c.c,k=qIdx(q);
    var rx=L+i*cw,ry=T+(ny-1-j)*ch;
    o+='<rect data-i="'+i+'" data-j="'+j+'" x="'+(rx+0.75)+'" y="'+(ry+0.75)+'" width="'+(cw-1.5)+'" height="'+(ch-1.5)+'" rx="2" style="fill:'+QCOL[k]+';cursor:pointer"/>';
    o+='<text class="cell-txt" x="'+(rx+cw/2)+'" y="'+(ry+ch/2+4)+'" text-anchor="middle" style="pointer-events:none;fill:'+txtOn(QCOL[k])+';font:500 10.5px var(--mono)">'+fq(q)+'</text>';
  }}
  var X=function(v){return L+(Math.log10(v)-x0)/(x1-x0)*PW;},Y=function(v){return T+PH-(Math.log10(v)-y0)/(y1-y0)*PH;};
  [1,10,100].forEach(function(v){o+='<line x1="'+X(v)+'" y1="'+(T+PH)+'" x2="'+X(v)+'" y2="'+(T+PH+6)+'" style="stroke:var(--muted);stroke-width:1.5"/><text x="'+X(v)+'" y="'+(T+PH+22)+'" text-anchor="middle" style="fill:var(--muted);font:500 13px var(--mono)">'+v+'</text>';});
  [0.1,1].forEach(function(v){o+='<line x1="'+(L-6)+'" y1="'+Y(v)+'" x2="'+L+'" y2="'+Y(v)+'" style="stroke:var(--muted);stroke-width:1.5"/><text x="'+(L-10)+'" y="'+(Y(v)+4)+'" text-anchor="end" style="fill:var(--muted);font:500 13px var(--mono)">'+fm(v)+'</text>';});
  o+='<text x="'+(L+PW/2)+'" y="'+(T+PH+46)+'" text-anchor="middle" style="fill:var(--ink);font:500 13px var(--mono)">RQD / Jn  →  bloques más grandes</text>';
  o+='<text transform="translate(14 '+(T+PH/2)+') rotate(-90)" text-anchor="middle" style="fill:var(--ink);font:500 13px var(--mono)">Jr / Ja  →  juntas más resistentes</text>';
  var cx=L+clamp((Math.log10(c.a)-x0)/(x1-x0),0,1)*PW,cy=T+PH-clamp((Math.log10(c.b)-y0)/(y1-y0),0,1)*PH;
  o+='<g style="pointer-events:none"><circle cx="'+cx+'" cy="'+cy+'" r="11" style="fill:none;stroke:var(--surface);stroke-width:6"/><circle cx="'+cx+'" cy="'+cy+'" r="11" style="fill:none;stroke:var(--ink);stroke-width:2.5"/><circle cx="'+cx+'" cy="'+cy+'" r="3.5" style="fill:var(--ink)"/>';
  var tx=cx>L+PW*0.7?cx-18:cx+18,an=cx>L+PW*0.7?'end':'start';
  o+='<text x="'+tx+'" y="'+(cy-20)+'" text-anchor="'+an+'" style="paint-order:stroke;stroke:var(--surface);stroke-width:4px;fill:var(--ink);font:600 13px var(--mono)">Tu caso</text></g>';
  var svg=$('#q-mx');svg.innerHTML=o;
  svg._m={x0:x0,dx:dx,y0:y0,dy:dy,c:c.c};
}
function mxInfo(t){
  var svg=$('#q-mx'),m=svg._m;if(!m||!t||t.getAttribute('data-i')===null)return;
  var i=+t.getAttribute('data-i'),j=+t.getAttribute('data-j');
  var xa=Math.pow(10,m.x0+i*m.dx),xb=Math.pow(10,m.x0+(i+1)*m.dx),ya=Math.pow(10,m.y0+j*m.dy),yb=Math.pow(10,m.y0+(j+1)*m.dy);
  var q=Math.sqrt(xa*xb)*Math.sqrt(ya*yb)*m.c,k=qIdx(q);
  $('#m-info').innerHTML='RQD/Jn de '+fm(xa,xa<10?1:0)+' a '+fm(xb,xb<10?1:0)+' · Jr/Ja de '+fm(ya,2)+' a '+fm(yb,2)+'<br>Q ≈ <b style="color:var(--ink)">'+fq(q)+'</b> · '+QC[k].n;
}
function supportText(Q){
  return Q>=40?'Sin soporte, con inspección periódica.'
   :Q>=10?'Sin soporte, o pernos puntuales donde haga falta.'
   :Q>=4?'Pernos puntuales y shotcrete simple de 4–5 cm en los sectores débiles.'
   :Q>=1?'Pernos sistemáticos y shotcrete simple de 5–6 cm.'
   :Q>=0.1?'Pernos sistemáticos y shotcrete con fibra de 6–12 cm.'
   :Q>=0.01?'Shotcrete con fibra de 12–15 cm, pernos y arcos reforzados con shotcrete.'
   :'Shotcrete con fibra de más de 15 cm, arcos de acero reforzados y cierre de solera.';
}
function updateQ(){
  var c=qCalc(),qi=qIdx(c.Q),e=ESR[S.q.esr].v;
  $('#q-rqd-lab').textContent=S.q.use?'paso 1: '+fm(Math.round(rqd()*10)/10)+' %':'manual';
  $('#q-rqd').disabled=S.q.use;if(S.q.use)$('#q-rqd').value=Math.round(rqd());
  $('#q-rqd-o').textContent=fm(Math.round(c.rq))+' %';
  $('#q-span-o').textContent=fm(S.q.span,1)+' m';
  $('#q-main').innerHTML='<span class="num">'+fq(c.Q)+'</span>'+chipHtml(QC[qi].n,QCOL[qi]);
  $('#q-eq').innerHTML='Q = '+frac('RQD','Jn')+'×'+frac('Jr','Ja')+'×'+frac('Jw','SRF');
  $('#q-eq2').innerHTML='= '+frac(fm(Math.round(c.r)),fm(c.jn))+'×'+frac(fm(c.jr),fm(c.ja))+'×'+frac(fm(c.jw),fm(c.srf))+' = '+fm(c.a,c.a>=10?1:2)+' × '+fm(c.b,2)+' × '+fm(c.c,2)+(c.rq<10?'<br><span style="font-size:12.5px">RQD menor que 10: se usa 10 (mínimo nominal).</span>':'');
  gaugeQ('#g-q',c.Q);
  var f=[{k:'a',t:'Tamaño de bloque',f:'RQD/Jn',v:c.a},{k:'b',t:'Resistencia entre bloques',f:'Jr/Ja',v:c.b},{k:'c',t:'Esfuerzo activo',f:'Jw/SRF',v:c.c}];
  $('#q-fac').innerHTML=f.map(function(x){return '<div class="fac"><div class="fh"><b>'+x.t+'</b><code>'+x.f+'</code></div><div class="fv">'+fm(x.v,x.v>=10?1:2)+'</div><div class="trk"><i style="width:'+fillPct(x.v,FRAC_RANGES[x.k])+'%"></i></div><p>'+interp(x.k,x.v)+'</p></div>';}).join('');
  drawMatrix(c);
  $('#m-info').innerHTML='Colores calculados con tu Jw/SRF = '+fm(c.c,2)+'. Tu caso: RQD/Jn = '+fm(c.a,1)+', Jr/Ja = '+fm(c.b,2)+'.';
  $('#q-leg').innerHTML=QC.map(function(k,i){return '<span'+(i===qi?' class="on"':'')+'><i style="background:'+QCOL[i]+'"></i>'+fm(k.lo)+'–'+fm(k.hi)+' · '+k.n+'</span>';}).join('');
  var maxSpan=2*e*Math.pow(c.Q,0.4),de=S.q.span/e,ok=S.q.span<=maxSpan;
  $('#q-sup').innerHTML='<p><b>'+supportText(c.Q)+'</b></p>'
   +'<p class="muted">Dimensión equivalente De = luz ÷ ESR = '+fm(S.q.span,1)+' ÷ '+fm(e)+' = <b style="color:var(--ink)">'+fm(de,1)+'</b>. Luz máxima sin soporte ≈ 2 · ESR · Q<sup>0,4</sup> = <b style="color:var(--ink)">'+fm(maxSpan,1)+' m</b>.</p>'
   +'<p style="margin:0">'+(ok?'Tu excavación de '+fm(S.q.span,1)+' m queda dentro de esa luz.':'Tu excavación de '+fm(S.q.span,1)+' m supera esa luz en '+fm(S.q.span-maxSpan,1)+' m: necesita soporte.')+'</p>'
   +'<p class="hint" style="margin:10px 0 0">Guía didáctica. El gráfico completo de Barton combina Q con De en categorías de soporte más finas.</p>';
}

/* ---------- panel RMR ---------- */
function updateRmr(){
  var m=rmrCalc(),k=rmrIdx(m.total),rq=Math.round(rqd()*10)/10;
  $('#r-rqdline').innerHTML='RQD '+fm(rq)+' % → <b>'+m.parts[1].v+' pts</b>';
  $('#r-main').innerHTML='<span class="num">'+Math.round(m.total)+'</span>'+chipHtml('Clase '+ROM[k]+' · '+RC[k].n,C5[k]);
  gaugeRmr('#g-rmr',m.total);
  var h=m.parts.map(function(p){return '<div class="prow"><span class="pn">'+p.k+'</span><span class="pb"><i style="width:'+(p.v/p.max*100)+'%"></i></span><span class="pv">'+p.v+' / '+p.max+'</span></div>';}).join('');
  h+='<div class="prow"><span class="pn"><b>Suma de parámetros</b></span><span></span><span class="pv"><b>'+m.basic+'</b></span></div>';
  h+='<div class="prow adj"><span class="pn">Ajuste por orientación</span><span></span><span class="pv">'+sg(m.adj)+'</span></div>';
  $('#r-rows').innerHTML=h;
  var t='<thead><tr><th>Clase</th><th>RMR</th><th>Calidad</th><th>Cohesión</th><th>Fricción</th><th>Autosoporte</th></tr></thead><tbody>';
  var rg=['81–100','61–80','41–60','21–40','< 21'];
  RC.forEach(function(r,i){t+='<tr'+(i===k?' class="on"':'')+'><td><span class="sw" style="background:'+C5[i]+'"></span>'+ROM[i]+'</td><td class="mono">'+rg[i]+'</td><td>'+r.n+'</td><td>'+r.coh+'</td><td>'+r.fr+'</td><td>'+r.t+'</td></tr>';});
  $('#r-tab').innerHTML=t+'</tbody>';
}

/* ---------- panel comparar ---------- */
function updateCmp(){
  var r=Math.round(rqd()*10)/10,rc=rqdCls(r),q=qCalc(),qi=qIdx(q.Q),m=rmrCalc(),mk=rmrIdx(m.total);
  $('#c-v1').textContent=fm(r)+' % · '+rc.n;$('#c-v2').textContent=fq(q.Q)+' · '+QC[qi].n;$('#c-v3').textContent=Math.round(m.total)+' · '+RC[mk].n;
  gaugeRqd('#c-g1',r);gaugeQ('#c-g2',q.Q);gaugeRmr('#c-g3',m.total);
  var rmrQ=9*Math.log(q.Q)+44,diff=Math.round(m.total-rmrQ),kq=rmrIdx(rmrQ);
  var msg;
  if(Math.abs(diff)<=10)msg='Los dos sistemas concuerdan dentro de la dispersión habitual de la correlación (±10 puntos).';
  else if(diff>10)msg='El RMR da una valoración mejor que la que sugiere Q. Revisa Jw y SRF: Q castiga más el agua y los esfuerzos, mientras que el RMR solo mira el agua como un parámetro de 15 puntos.';
  else msg='Q da una valoración mejor que el RMR. Revisa el estado de las juntas y la resistencia de la roca: el RMR los pondera con más peso que el cociente Jr/Ja.';
  var gsiTxt=m.rmrp>23?'Como referencia, el GSI se estima en <b>'+Math.round(m.gsi)+'</b> (RMR básico seco sin orientación, menos 5).':'El RMR básico es muy bajo para estimar un GSI con esta relación.';
  $('#c-read').innerHTML='<h3>Lectura de tu caso</h3>'
   +'<p style="margin-top:10px">El <b>RQD</b> de '+fm(r)+' % corresponde a un macizo de calidad <b>'+rc.n.toLowerCase()+'</b>. El índice <b>Q</b> de '+fq(q.Q)+' lo clasifica como <b>'+QC[qi].n.toLowerCase()+'</b>, y el <b>RMR</b> de '+Math.round(m.total)+' lo ubica en la clase <b>'+ROM[mk]+'</b> ('+RC[mk].n.toLowerCase()+').</p>'
   +'<p>Con RMR = 9 · ln Q + 44, tu Q equivale a un RMR de <b>'+Math.round(rmrQ)+'</b> (clase '+ROM[kq]+'). El RMR calculado es '+Math.round(m.total)+', una diferencia de '+sg(diff)+' puntos.</p>'
   +'<p>'+msg+'</p><p class="muted" style="margin:0">'+gsiTxt+'</p>';
  var bounds=[81,61,41,21],qv=bounds.map(function(b){return Math.exp((b-44)/9);});
  var qr=['> '+fq(qv[0]),fq(qv[1])+' – '+fq(qv[0]),fq(qv[2])+' – '+fq(qv[1]),fq(qv[3])+' – '+fq(qv[2]),'< '+fq(qv[3])],rg=['81–100','61–80','41–60','21–40','< 21'];
  var t='<thead><tr><th>Clase</th><th>Calidad</th><th>RMR</th><th>Q equivalente</th></tr></thead><tbody>';
  RC.forEach(function(x,i){t+='<tr'+(i===mk?' class="on"':'')+'><td><span class="sw" style="background:'+C5[i]+'"></span>'+ROM[i]+'</td><td>'+x.n+'</td><td class="mono">'+rg[i]+'</td><td class="mono">'+qr[i]+'</td></tr>';});
  $('#c-eq').innerHTML=t+'</tbody>';
}

/* ---------- navegación y actualización ---------- */
function setChip(k,txt,col){$('#v-'+k).textContent=txt;$('#d-'+k).style.background=col;}
function updateBar(){
  var r=rqd(),q=qCalc(),m=rmrCalc();
  setChip('rqd',fm(Math.round(r))+' %',C5[rqdCls(r).c-1]);
  setChip('q',fq(q.Q),QCOL[qIdx(q.Q)]);
  setChip('rmr',String(Math.round(m.total)),C5[rmrIdx(m.total)]);
}
var TABS=['rqd','q','rmr','comparar'];
function update(){
  updateBar();
  if(S.tab==='rqd')updateRqd();else if(S.tab==='q')updateQ();else if(S.tab==='rmr')updateRmr();else updateCmp();
}
function showTab(t,scroll){
  if(TABS.indexOf(t)<0)t='rqd';
  S.tab=t;
  TABS.forEach(function(k){$('#p-'+k).hidden=(k!==t);$('#t-'+k).setAttribute('aria-selected',k===t?'true':'false');});
  update();
  if(scroll){var y=document.querySelector('.barwrap').offsetTop;if(window.scrollY>y)window.scrollTo(0,y);}
}

/* ---------- inicialización ---------- */
function fill(id,arr,f){$(id).innerHTML=arr.map(function(o,i){return '<option value="'+i+'">'+f(o)+'</option>';}).join('');}
function bindSel(id,obj,key){var el=$(id);el.value=S[obj][key];el.addEventListener('change',function(){S[obj][key]=+el.value;update();});}

fill('#q-jn',JN,function(o){return fm(o.v)+' · '+o.t;});
fill('#q-jr',JR,function(o){return fm(o.v)+' · '+o.t;});
fill('#q-ja',JA,function(o){return fm(o.v)+' · '+o.t;});
fill('#q-jw',JW,function(o){return fm(o.v)+' · '+o.t;});
fill('#q-srf',SRF,function(o){return fm(o.v)+' · '+o.t;});
fill('#q-esr',ESR,function(o){return 'ESR '+fm(o.v)+' · '+o.t;});
fill('#r-ucs',UCS,function(o){return o.t+' · '+o.r+' pts';});
fill('#r-sp',SPC,function(o){return o.t+' · '+o.r+' pts';});
fill('#r-cond',CND,function(o){return o.r+' pts · '+o.t;});
fill('#r-wat',WAT,function(o){return o.t+' · '+o.r+' pts';});
fill('#r-ori',ORI,function(o){return o.t+' · '+sg(o.r);});
bindSel('#q-jn','q','jn');bindSel('#q-jr','q','jr');bindSel('#q-ja','q','ja');bindSel('#q-jw','q','jw');bindSel('#q-srf','q','srf');bindSel('#q-esr','q','esr');
bindSel('#r-ucs','r','ucs');bindSel('#r-sp','r','sp');bindSel('#r-cond','r','cond');bindSel('#r-wat','r','wat');bindSel('#r-ori','r','ori');

$('#q-use').addEventListener('change',function(){S.q.use=this.checked;if(!this.checked)S.q.rqd=Math.round(rqd());update();});
$('#q-rqd').addEventListener('input',function(){S.q.rqd=+this.value;update();});
$('#q-span').value=S.q.span;
$('#q-span').addEventListener('input',function(){S.q.span=+this.value;update();});

var ctl='';
['Familia 1','Familia 2','Familia 3'].forEach(function(n,i){
  ctl+='<div class="setrow"><label class="chk"><input type="checkbox" id="s'+i+'-on" checked><span class="dot" style="background:var(--j'+(i+1)+')"></span>'+n+'</label><input type="range" id="s'+i+'-t" min="0" max="100" step="0.5" aria-label="Espaciamiento de la '+n.toLowerCase()+'"><output class="out" id="s'+i+'-o"></output></div>';
});
$('#palm-ctl').innerHTML=ctl;
S.sets.forEach(function(x,i){
  $('#s'+i+'-t').value=tFromS(x.s);
  $('#s'+i+'-on').addEventListener('change',function(){x.on=this.checked;update();});
  $('#s'+i+'-t').addEventListener('input',function(){x.s=sFromT(+this.value);update();});
});

$('#m-core').addEventListener('click',function(){S.mode='core';update();});
$('#m-palm').addEventListener('click',function(){S.mode='palm';S.ch.on=false;update();});
$('#n-frac').addEventListener('input',function(){S.breaks=genBreaks(+this.value,S.seed);update();});
$('#b-shuffle').addEventListener('click',function(){S.seed++;S.breaks=genBreaks(S.breaks.length,S.seed);update();});
$('#core-svg').addEventListener('click',function(e){
  if(S.ch.on)return;
  var r=this.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*1000,cm=(x-20)/9.6;
  if(cm<0||cm>100)return;
  var thr=14/(r.width/1000)/9.6,idx=-1,best=1e9;
  S.breaks.forEach(function(b,i){var d=Math.abs(b-cm);if(d<best){best=d;idx=i;}});
  if(idx>=0&&best<=thr)S.breaks.splice(idx,1);
  else if(S.breaks.length<40)S.breaks.push(clamp(Math.round(cm*10)/10,1,99));
  S.breaks.sort(num);update();
});

var gb='';
RQDC.forEach(function(c,i){gb+='<button type="button" class="guess" data-g="'+i+'">'+c.n+'<small>'+c.lo+'–'+c.hi+' %</small></button>';});
$('#guesses').innerHTML=gb;
$('#guesses').addEventListener('click',function(e){
  var b=e.target.closest('.guess');if(!b||S.ch.answered)return;
  S.ch.guess=+b.getAttribute('data-g');S.ch.answered=true;S.ch.tries++;
  if(S.ch.guess===RQDC.indexOf(rqdCls(coreRqd(S.ch.breaks))))S.ch.right++;
  update();
});
$('#b-challenge').addEventListener('click',function(){S.ch.on=!S.ch.on;if(S.ch.on)newChallenge();update();});
$('#ch-next').addEventListener('click',function(){newChallenge();update();});

$('#q-mx').addEventListener('click',function(e){mxInfo(e.target);});
$('#q-mx').addEventListener('mouseover',function(e){mxInfo(e.target);});

TABS.forEach(function(k){$('#t-'+k).addEventListener('click',function(){
  showTab(k,true);
  try{history.replaceState(null,'','#'+k);}catch(err){}
});});
window.addEventListener('hashchange',function(){showTab(location.hash.slice(1),true);});
showTab(location.hash.slice(1)||'rqd',false);
})();
</script>

</body>
</html>
