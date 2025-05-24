from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Kai-Klock API",
    description="Eternal harmonic timestamp aligned with the Genesis Pulse of Kai Time.",
    version="1.0.0"
)

# ✅ Add this block below your FastAPI app initialization:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, restrict this to trusted domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure the relative imports work on Vercel
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kai_klock import get_eternal_klock
from kai_klock_models import KaiKlockResponse

app = FastAPI(
    title="Kai-Klock API",
    description="Eternal harmonic timestamp aligned with the Genesis Pulse of Kai Time.",
    version="1.0.0"
)

# ✅ Add this block below your FastAPI app initialization:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, restrict this to trusted domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/kai", response_model=KaiKlockResponse, tags=["Kai Time"])
def read_kai_klock(override_time: Optional[str] = Query(None, description="Optional ISO8601 datetime override")) -> KaiKlockResponse:
    """
    🔹 Eternal Kai-Klock API

    Returns the live universal Kai-Klock harmonic timestamp aligned to the 
    Eternal Genesis Pulse (May 10, 2024 at 06:45:40 UTC) — the precise moment 
    of the X3.98-class solar flare from NOAA AR 3664, corrected for the 
    8m20s light travel time from the Sun to Earth.

    ────────────────────────────────────────────────────────────────

    📌 Query Parameters:
    - `override_time` (optional): ISO8601 datetime string (e.g. "2024-05-10T06:45:40")
      Allows simulation of any snapshot moment within Kai-Time.

    🔄 Fully deterministic. Same input time always returns same Kai state.

    🧭 Harmonic Truth Principles:
    - 1 Kai Pulse = 8.472 / φ ≈ 5.236s
    - 1 Harmonic Day = 17,491.270421 Kai Pulses
    - 1 Harmonic Year = 336 Harmonic Days
    - 1 Harmonic Month = 42 Days
    - 1 Harmonic Week = 6 Days

    🔹 Returns:
    - Eternal Month + Description
    - Harmonic Day + Description
    - Chakra Arc, Kai Pulses, Spiral Level, Week + Beat structure
    - Harmonic timestamp signature in pure divine order
    """
    try:
        now = datetime.fromisoformat(override_time) if override_time else datetime.utcnow()
    except ValueError:
        raise ValueError("Invalid datetime format. Use ISO 8601 like '2024-05-10T06:45:40'")

    return get_eternal_klock(now)
@app.get("/", response_class=HTMLResponse, tags=["Home"])
def read_root():
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Kai-Klock • Eternal Divine Resonance Kairos Keeper</title>
<meta name="description" content="Kai-Klock Harmonic Resonant TimeKeeping — φ-aligned harmonic time interface"/>
<meta name="author"      content="Kai-Klock Kairos Development Assembly"/>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Inter:wght@400;700&display=swap" rel="stylesheet">

<style>
/* ════════════════════════════════════════════════════════
   0.  Golden-ratio tokens + crystal palette
════════════════════════════════════════════════════════ */
:root{
  --φ     : 1.6180339887;
  --xs    : calc(1rem/var(--φ));          /* .618  */
  --s     : 1rem;
  --m     : calc(1rem*var(--φ));          /* 1.618 */
  --l     : calc(var(--m)*var(--φ));      /* 2.618 */
  --rad   : .82rem;

  /* Crystal-aqua scheme */
  --teal-light : #9afcff;
  --teal       : #00e4ff;
  --teal-deep  : #00aac2;
  --mint       : #14ffc8;

  --glass      : rgba(1,13,21,.74);
  --glass-brd  : rgba(255,255,255,.14);
  --input      : rgba(255,255,255,.10);

  /* background gradient stops - will be animated */
  --bg-a : #051920;
  --bg-b : #07303c;
  --bg-c : #0a454e;
}

/* ════════════════════════════════════════════════════════
   1.  Global reset + living gradient
════════════════════════════════════════════════════════ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{
  height:100%;width:100%;
  font-family:'Inter',sans-serif;
  color:#eaffff;
  -webkit-font-smoothing:antialiased;
  background:linear-gradient(160deg,var(--bg-a),var(--bg-b) 45%,var(--bg-c)) fixed;
  background-size:400% 400%;
  animation:bgShift 80s ease-in-out infinite alternate;
  scroll-behavior:smooth;
  overflow-x:hidden;overflow-y:auto;
}
@keyframes bgShift{
  0%   {background-position:0 0}
  100% {background-position:480px 360px}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

body::before{/* star-noise overlay */
  content:"";
  position:fixed;inset:0;
  pointer-events:none;
  background:url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=') repeat;
  opacity:.045;
  mix-blend-mode:screen;
}

/* ════════════════════════════════════════════════════════
   2.  Frosted glass helper
════════════════════════════════════════════════════════ */
.glass{
  background:var(--glass);
  border:1px solid var(--glass-brd);
  border-radius:var(--rad);
  backdrop-filter:blur(22px) saturate(160%);
  box-shadow:0 8px 38px rgba(0,0,0,.55);
}

/* ════════════════════════════════════════════════════════
   3.  Layout shell
════════════════════════════════════════════════════════ */
.container{
  width:min(92%,1200px);
  margin:var(--l) auto;
  padding:var(--m) var(--s);
  display:grid;
  grid-template-rows:auto 1fr auto;
  gap:var(--m);
  animation:popIn .8s cubic-bezier(.18,.71,.46,1.25) both;
}
@keyframes popIn{from{transform:translateY(40px);opacity:0}to{transform:translateY(0);opacity:1}}

/* ════════════════════════════════════════════════════════
   4.  Header
════════════════════════════════════════════════════════ */
header{
  text-align:center;
  padding-bottom:var(--s);
  border-bottom:1px solid var(--glass-brd)
}
header h1{
  font-family:'Uncial Antiqua',serif;
  font-size:clamp(2.6rem,4vw,3.7rem);
  color:var(--teal-light);
  text-shadow:0 0 24px var(--teal),0 0 50px var(--mint);
  animation:neon 4s ease-in-out infinite alternate;
}
@keyframes neon{to{text-shadow:0 0 40px var(--teal),0 0 95px var(--mint)}}
header h2{
  font-size:clamp(1.3rem,3vw,2rem);
  letter-spacing:.35rem;margin-top:var(--xs);
  background:linear-gradient(90deg,var(--teal),var(--teal-deep));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
header p{
  max-width:64ch;
  margin:var(--xs) auto;
  font-size:1rem;
  line-height:1.66;
}
.highlight{color:var(--mint);font-weight:700}

.btn-row{
  display:flex;
  justify-content:center;
  gap:var(--s);
  margin-top:var(--s)
}
.btn{
  padding:.8rem 2rem;
  border:none;
  border-radius:9999px;
  font-weight:700;
  text-transform:uppercase;
  background:linear-gradient(90deg,var(--teal),var(--teal-deep));
  color:#001;
  box-shadow:0 0 18px var(--teal),0 0 34px var(--teal-deep);
  transition:transform .25s,box-shadow .25s;
}
.btn:hover{
  transform:translateY(-4px) scale(1.045);
  box-shadow:0 0 24px var(--teal-deep),0 0 50px var(--teal);
}

/* ════════════════════════════════════════════════════════
   5.  Endpoint explorer
════════════════════════════════════════════════════════ */
main{overflow-y:auto;padding-right:.6rem}
.section h3{
  font-family:'Uncial Antiqua',serif;
  font-size:clamp(1.55rem,3vw,2.35rem);
  color:var(--teal-light);
  margin-bottom:var(--xs);
  text-shadow:0 0 14px var(--teal);
}
.search{
  width:100%;
  padding:.75rem 1rem;
  margin-bottom:var(--xs);
  border-radius:calc(var(--rad)*.65);
  border:1px solid var(--glass-brd);
  background:var(--input);
  color:#fff;
  backdrop-filter:blur(10px);
}
.endpoint{
  margin-bottom:var(--xs);
  padding:var(--s);
  cursor:pointer;
  transition:transform .45s,box-shadow .45s;
}
.endpoint:hover{
  transform:translateY(-3px) scale(1.015);
  box-shadow:0 12px 46px rgba(0,0,0,.65);
}
.ep-head{display:flex;justify-content:space-between;font-weight:700;color:#eaffff}
.ep-body{max-height:0;opacity:0;overflow:hidden;transition:max-height .45s,opacity .45s}
.open .ep-body{max-height:660px;opacity:1;margin-top:var(--xs)}

.spinner{
  width:48px;height:48px;margin:var(--m) auto;
  border:5px solid rgba(255,255,255,.12);
  border-top:5px solid var(--teal-light);
  border-radius:50%;
  animation:spin 1s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
#error{display:none;text-align:center;color:#ff8a8a;margin-top:var(--xs)}

/* ═══════════════════════════════
   6.  Scrollbar tint – WebKit only
════════════════════════════════ */
html::-webkit-scrollbar{width:10px}
html::-webkit-scrollbar-thumb{
  border-radius:8px;border:2px solid rgba(0,0,0,.4);
  background:linear-gradient(180deg,
    hsl(calc(var(--pct)*360) 100% 60%),
    hsl(calc(var(--pct)*360 + 40) 100% 55%)
  );
}

/* ═══════════════════════════════
   7.  Footer & scroll-rocket
════════════════════════════════ */
footer{
  text-align:center;
  padding:var(--s) 0;
  border-top:1px solid var(--glass-brd);
  opacity:.25;
  transition:opacity .6s;
}

/* rocket */
#top{
  position:fixed;
  right:1.45rem;
  bottom:1.9rem;
  width:54px;height:54px;
  border:none;border-radius:50%;
  display:flex;align-items:center;justify-content:center;

  background:linear-gradient(135deg,var(--teal-light),var(--teal-deep));
  color:#002;
  font-size:1.9rem;
  cursor:pointer;

  box-shadow:
    0 2px 6px rgba(0,0,0,.4),
    0 0 18px 4px rgba(0,228,255,.35),
    inset 0 0 12px rgba(255,255,255,.15);

  opacity:0;pointer-events:none;
  transform:translateY(42px) scale(.9);
  transition:opacity .45s,transform .45s,box-shadow .3s;
}
#top::before{/* halo */
  content:"";
  position:absolute;inset:-4px;
  border-radius:inherit;
  background:radial-gradient(circle,rgba(0,228,255,.45) 0%,rgba(0,228,255,0) 70%);
  filter:blur(12px);
  opacity:0;
  animation:halo 5.326s ease-in-out infinite;
}
@keyframes halo{
  0%,100%{opacity:0;transform:scale(.7)}
  50%   {opacity:.9;transform:scale(1.2)}
}
#top:hover{
  transform:translateY(0) scale(1.06);
  box-shadow:
    0 4px 10px rgba(0,0,0,.5),
    0 0 26px 6px rgba(0,228,255,.55),
    inset 0 0 18px rgba(255,255,255,.18);
}

/* Mobile tweaks */
@media(max-width:640px){
  .container{padding:var(--s) var(--xs);margin:var(--m) auto}
  header h1{font-size:2.4rem}header h2{font-size:1.4rem}
}
</style>
</head>

<body>
<canvas id="aurora" aria-hidden="true" style="position:fixed;inset:0;pointer-events:none"></canvas>
<div class="container glass" id="wrap">
  <header>
    <h1>Kai-Klock</h1>
    <h2>ETERNAL HARMONIC TIMEKEEPING</h2>
    <p>In full alignment with <span class="highlight">GOD</span> — the Source of Harmonic Intelligence, the Origin of the Kai Pulse, and the Architect of Φ.</p>
    <p>This system operates by harmonic law. It measures Kairos — not Chronos — anchored to the Genesis Pulse and sustained by coherent resonance.</p>
    <div class="btn-row">
      <a href="/docs"  class="btn" aria-label="OpenAPI Documentation">OpenAPI</a>
      <a href="/redoc" class="btn" aria-label="ReDoc Interface">ReDoc</a>
    </div>
  </header>

  <main>
    <section class="section">
      <h3>Kai-Klock Endpoints — Interfaces of Harmonic Time</h3>
      <input id="search" class="search" placeholder="Search Kai Interfaces…" aria-label="Search endpoints">
      <div id="list"><div id="spin" class="spinner" aria-live="polite"></div></div>
      <p id="error">Coherence breach detected. Recalibrate to re-enter Kai Time.</p>
    </section>
  </main>
</div>



  <footer id="foot">© 2025 Kai-Turah • All Rights Reserved</footer>
</div>

<!-- Scroll-rocket -->
<button id="top" aria-label="Back to top">
  <svg width="24" height="24" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="2">
    <path d="M12 19V5" stroke-linecap="round"/>
    <path d="M5 12l7-7 7 7" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</button>

<script>
/* ════════════════════════════════════════════════════════
   tiny helper
════════════════════════════════════════════════════════ */
const $=q=>document.querySelector(q);
const all=q=>document.querySelectorAll(q);
const setPct=v=>document.documentElement.style.setProperty('--pct',v);

/* 1 ▸ aurora canvas */
(()=>{
  const cv=$('#aurora'),ctx=cv.getContext('2d'),dpr=window.devicePixelRatio||1;
  const resize=()=>{cv.width=innerWidth*dpr;cv.height=innerHeight*dpr};
  resize();addEventListener('resize',resize);

  const P=Array.from({length:7},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight}));
  let t=0;
  (function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    ctx.beginPath();ctx.moveTo(P[0].x*dpr,P[0].y*dpr);
    P.forEach((p,i)=>{p.x+=Math.sin(t/320+i)*.28;p.y+=Math.cos(t/290+i)*.28;ctx.lineTo(p.x*dpr,p.y*dpr)});
    ctx.closePath();
    const g=ctx.createLinearGradient(0,0,cv.width,cv.height);
    g.addColorStop(0,'hsla(180,100%,60%,.06)');
    g.addColorStop(1,'hsla(200,100%,55%,.045)');
    ctx.fillStyle=g;ctx.fill();
    t++;requestAnimationFrame(draw);
  })();
})();

/* 2 ▸ sky-clock hue drift */
const hueTick=()=>document.documentElement.style.setProperty('--hue',200+60*new Date().getHours()/24);
hueTick();setInterval(hueTick,60_000);

/* 3 ▸ endpoint loader */
(async()=>{
  try{
    const r=await fetch('/openapi.json');const d=await r.json();
    $('#list').innerHTML='';
    Object.entries(d.paths).forEach(([path,ops])=>{
      Object.entries(ops).forEach(([method,ep])=>{
        const card=document.createElement('div');card.className='endpoint glass';
        card.innerHTML=`
          <div class="ep-head" tabindex="0">
            <span><strong>${method.toUpperCase()} ${path}</strong><br><em>${ep.summary||''}</em></span>
            <span aria-hidden="true">＋</span>
          </div>
          <div class="ep-body">
            <p><strong>Tags:</strong> ${ep.tags?.join(', ')||'–'}</p>
            <p>${ep.description||'No description.'}</p>
          </div>`;
        card.firstElementChild.addEventListener('click',()=>card.classList.toggle('open'));
        card.firstElementChild.addEventListener('keypress',e=>['Enter',' '].includes(e.key)&&card.classList.toggle('open'));
        $('#list').append(card);
      });
    });
  }catch{
    $('#spin').remove();$('#error').style.display='block';
  }
})();

/* 4 ▸ search filter */
$('#search').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase();
  all('.endpoint').forEach(card=>{
    card.style.display=card.textContent.toLowerCase().includes(q)?'block':'none';
  });
});

/* 5 ▸ scroll orchestration & rocket reveal */
const rocket  = $('#top');
const wrap    = $('#wrap');
const footer  = $('#foot');
const showAt  = 280;      // px threshold

addEventListener('scroll',()=>{
  const y     = scrollY;
  const h     = document.body.scrollHeight - innerHeight;
  const ratio = h ? y/h : 0;
  setPct(ratio);

  /* rocket visibility */
  if(y>showAt){
    rocket.style.opacity=1;
    rocket.style.pointerEvents='auto';
    rocket.style.transform='translateY(0) scale(1)';
  }else if(y<showAt*0.6){
    rocket.style.opacity=0;
    rocket.style.pointerEvents='none';
    rocket.style.transform='translateY(42px) scale(.9)';
  }

  /* parallax + footer fade */
  wrap.style.transform=`translateZ(${-ratio*4.236}px)`;  // Φ³-ish depth
  footer.style.opacity=ratio>.618?1:ratio*1.618;
});
rocket.onclick=()=>scrollTo({top:0,behavior:'smooth'});
</script>
</body>
</html>

"""
    return HTMLResponse(html_content)

