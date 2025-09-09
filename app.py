import streamlit as st
import google.generativeai as genai
import time
import os
import re
import uuid
from textwrap import dedent

# ----------------------------
# Config & API initialization
# ----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(
    page_title="Meet Enviro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------
# Model configuration & system msg
# --------------------------------
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

SYSTEM_INSTRUCTION = """
Name: Your name is Enviro. Your name stands for EnviroCast AI Dialogue Engine

Behavioral Guidelines:
Be informative, professional, and approachable.
Focus all responses on pollution, environmental issues, air quality, and related science topics.
Explain concepts clearly, using structured lists, diagrams, or examples when helpful.
Always provide citations and references for any scientific claims or data.
When relevant, mention the EnviroCast website (https://envirocast.github.io) as a resource, but do not focus on promoting—use it as an informational reference only.
Encourage learning and understanding of environmental issues and technologies, including quantum and classical modeling for air quality if appropriate.
Keep answers concise but thorough, ensuring accuracy and clarity.

INFORMATION ABOUT ENVIROCAST:
EnviroCast (web: https://envirocast.github.io) is a platform designed to educate people on pollution, environmental effects, and air quality prediction.
It uses advanced technologies, including a hybrid quantum-classical algorithm, to monitor and predict air quality.
The site includes interactive simulations, models, and visualizations to help users understand environmental challenges and solutions.
Social media campaign: Instagram @envirocast_tech.

Always provide citations at the end of every response using good and credible sources.

Make sure to only talk about environmental, focus only on the topics mentioned in these instructions, do not involve in anything unrelated to the topic or anything illegal or negative.

You are ONLY an informational chatbot.
""".strip()


# ------------------------
# Session state bootstrap
# ------------------------
def initialize_session_state():
    if "chat_model" not in st.session_state:
        st.session_state.chat_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=SYSTEM_INSTRUCTION,
        )

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = st.session_state.chat_model.start_chat(history=[])

    if "messages" not in st.session_state:
        st.session_state.messages = []


# -------------------------------------------
# Minimal, safer markdown -> HTML converter
# (keeps your look, avoids script bleeding)
# -------------------------------------------
def advanced_markdown(text: str) -> str:
    # Normalize excessive newlines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # Headers
    text = re.sub(r"^### (.*)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.*)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.*)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

    # Bold / Italic
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)\*(?<!\*)", r"<em>\1</em>", text)

    # Inline code (escape < & > inside)
    def code_repl(m):
        code = m.group(1).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<code>{code}</code>"
    text = re.sub(r"`([^`]+)`", code_repl, text)

    # Fenced code blocks
    def pre_repl(m):
        code = m.group(1).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre>{code}</pre>"
    text = re.sub(r"```(.*?)```", pre_repl, text, flags=re.DOTALL)

    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)

    # Lists (ul/ol)
    lines = text.split("\n")
    out = []
    in_ul = False
    in_ol = False
    for ln in lines:
        m_ul = re.match(r"^\s*[-\*\u2022]\s+(.*)$", ln)
        m_ol = re.match(r"^\s*(\d+)\.\s+(.*)$", ln)
        if m_ul:
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{m_ul.group(1)}</li>")
        elif m_ol:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{m_ol.group(2)}</li>")
        else:
            if in_ul:
                out.append("</ul>")
            in_ul = False
            if in_ol:
                out.append("</ol>")
            in_ol = False
            out.append(ln)
    if in_ul:
        out.append("</ul>")
    if in_ol:
        out.append("</ol>")
    text = "\n".join(out)

    # Paragraph wrapping (skip blocks & headers)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    formatted = []
    for p in paragraphs:
        if p.startswith(("<h1", "<h2", "<h3", "<ul", "<ol", "<pre", "<li")):
            formatted.append(p)
        else:
            formatted.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    return "\n".join(formatted)


# -------------------------------------------
# Enhanced background styles
# -------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { 
    font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif !important;
    box-sizing: border-box;
}

:root {
    --primary-cyan: #00D4FF;
    --primary-purple: #8B5CF6;
    --primary-green: #10B981;
    --bg-dark: #0e1117;
    --bg-card: rgba(15, 23, 42, 0.8);
    --text-light: #f1f5f9;
    --border-light: rgba(255, 255, 255, 0.08);
}

html, body {
    margin: 0;
    padding: 0;
    background: var(--bg-dark);
    color: var(--text-light);
    overflow-x: hidden;
}

.stApp {
    min-height: 100vh;
    position: relative;
    background: linear-gradient(135deg, 
        rgba(14, 17, 23, 1) 0%,
        rgba(20, 25, 35, 1) 25%,
        rgba(15, 20, 30, 1) 50%,
        rgba(18, 22, 32, 1) 75%,
        rgba(14, 17, 23, 1) 100%);
}

/* Hide Streamlit elements */
#MainMenu, 
footer, 
header, 
.stDeployButton,
.stDecoration {
    visibility: hidden !important;
    height: 0 !important;
}

/* Enhanced header */
.header {
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 3rem 0 2rem 0;
    background: linear-gradient(180deg, 
        rgba(15, 23, 42, 0.95) 0%,
        rgba(15, 23, 42, 0.8) 50%,
        rgba(15, 23, 42, 0.4) 100%);
    border-bottom: 2px solid rgba(0, 212, 255, 0.1);
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.title {
    background: linear-gradient(135deg, 
        var(--primary-cyan) 0%, 
        var(--primary-purple) 40%, 
        var(--primary-green) 70%,
        var(--primary-cyan) 100%);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0;
    animation: titleShimmer 6s ease-in-out infinite, titleFloat 8s ease-in-out infinite;
    text-shadow: 0 0 60px rgba(0, 212, 255, 0.4);
    filter: drop-shadow(0 4px 20px rgba(139, 92, 246, 0.3));
}

.subtitle {
    color: rgba(241, 245, 249, 0.8);
    font-size: 1.2rem;
    font-weight: 400;
    margin-top: 1rem;
    letter-spacing: 0.02em;
}

@media (max-width: 768px) { 
    .title { font-size: 2.8rem; }
    .subtitle { font-size: 1rem; }
}

@keyframes titleShimmer { 
    0%, 100% { background-position: 0% 50%; } 
    50% { background-position: 100% 50%; } 
}

@keyframes titleFloat { 
    0%, 100% { transform: translateY(0px); } 
    33% { transform: translateY(-8px); }
    66% { transform: translateY(4px); }
}

/* Chat container */
.chat-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem 1.5rem;
    position: relative;
    z-index: 5;
}

/* Enhanced message styling */
.message {
    margin-bottom: 2rem;
    padding: 2rem;
    border-radius: 24px;
    backdrop-filter: blur(25px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid var(--border-light);
    box-shadow: 
        0 10px 40px rgba(0, 0, 0, 0.3),
        0 1px 0 rgba(255, 255, 255, 0.1) inset;
    position: relative;
    overflow: hidden;
}

.message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.2), 
        transparent);
}

.user-message {
    background: linear-gradient(135deg, 
        rgba(0, 212, 255, 0.15) 0%,
        rgba(0, 212, 255, 0.08) 50%,
        rgba(0, 212, 255, 0.05) 100%);
    border-left: 4px solid var(--primary-cyan);
    margin-left: 8%;
    transform: translateX(-10px);
}

.assistant-message {
    background: linear-gradient(135deg, 
        rgba(139, 92, 246, 0.15) 0%,
        rgba(139, 92, 246, 0.08) 50%,
        rgba(16, 185, 129, 0.05) 100%);
    border-left: 4px solid var(--primary-purple);
    margin-right: 8%;
    transform: translateX(10px);
}

.message:hover { 
    transform: translateY(-4px) scale(1.01);
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.4),
        0 1px 0 rgba(255, 255, 255, 0.15) inset;
}

.user-message:hover { transform: translateY(-4px) translateX(-10px) scale(1.01); }
.assistant-message:hover { transform: translateY(-4px) translateX(10px) scale(1.01); }

/* Message headers */
.msg-header {
    display: flex; 
    align-items: center; 
    gap: 0.8rem; 
    margin-bottom: 1rem;
    font-weight: 700; 
    letter-spacing: -0.01em; 
    font-size: 1.1rem;
}

.user-header { 
    color: var(--primary-cyan); 
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.4); 
}

.enviro-header { 
    color: var(--primary-purple); 
    text-shadow: 0 0 15px rgba(167, 139, 250, 0.4); 
}

/* Message content styling */
.msg-content { 
    color: var(--text-light); 
    line-height: 1.8; 
    font-size: 1.05rem; 
    letter-spacing: 0.01em; 
}

.msg-content h1, .msg-content h2, .msg-content h3 { 
    color: #fff; 
    font-weight: 700; 
    margin: 1.5rem 0 1rem 0; 
}

.msg-content h1 { 
    font-size: 1.8rem; 
    background: linear-gradient(135deg, var(--primary-cyan), var(--primary-purple)); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
}

.msg-content h2 { 
    font-size: 1.4rem; 
    background: linear-gradient(135deg, var(--primary-purple), var(--primary-green)); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
}

.msg-content h3 { 
    font-size: 1.2rem; 
    background: linear-gradient(135deg, var(--primary-green), var(--primary-cyan)); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
}

.msg-content code { 
    background: rgba(0, 0, 0, 0.7); 
    color: var(--primary-cyan); 
    padding: 0.3rem 0.6rem; 
    border-radius: 8px; 
    font-family: 'JetBrains Mono', monospace; 
    font-size: 0.95rem; 
    border: 1px solid rgba(0, 212, 255, 0.2); 
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.msg-content pre { 
    background: rgba(0, 0, 0, 0.8); 
    color: var(--text-light); 
    padding: 1.5rem; 
    border-radius: 16px; 
    overflow-x: auto; 
    border: 1px solid rgba(139, 92, 246, 0.2); 
    font-family: 'JetBrains Mono', monospace; 
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    margin: 1rem 0;
}

.msg-content a { 
    color: var(--primary-cyan); 
    text-decoration: none; 
    border-bottom: 1px solid rgba(56, 189, 248, 0.3);
    transition: all 0.3s ease;
}

.msg-content a:hover { 
    color: #0ea5e9; 
    border-bottom-color: #0ea5e9; 
    text-shadow: 0 0 20px rgba(14, 165, 233, 0.5); 
}

.msg-content ul, .msg-content ol {
    padding-left: 1.5rem;
    margin: 1rem 0;
}

.msg-content li {
    margin: 0.5rem 0;
    line-height: 1.6;
}

/* Welcome message */
.welcome { 
    background: linear-gradient(135deg, 
        rgba(0, 212, 255, 0.12) 0%,
        rgba(139, 92, 246, 0.12) 40%,
        rgba(16, 185, 129, 0.12) 80%,
        rgba(0, 212, 255, 0.08) 100%); 
    border-radius: 24px; 
    padding: 2.5rem; 
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    box-shadow: 
        0 10px 40px rgba(0, 0, 0, 0.3),
        0 1px 0 rgba(255, 255, 255, 0.1) inset;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.welcome h2 {
    background: linear-gradient(135deg, var(--primary-cyan), var(--primary-purple), var(--primary-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
}

.welcome p {
    font-size: 1.1rem;
    opacity: 0.9;
    line-height: 1.6;
    margin: 0;
}

/* Enhanced chat input */
.stChatInput > div {
    position: fixed !important;
    bottom: 2rem !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: calc(100% - 4rem) !important;
    max-width: 1000px !important;
    z-index: 100 !important;
}

.stChatInput > div > div {
    background: linear-gradient(135deg, 
        rgba(15, 23, 42, 0.95) 0%, 
        rgba(30, 41, 59, 0.9) 100%) !important;
    backdrop-filter: blur(25px) !important;
    border: 2px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    box-shadow: 
        0 10px 40px rgba(0, 0, 0, 0.4),
        0 1px 0 rgba(255, 255, 255, 0.1) inset !important;
}

.stChatInput textarea { 
    background: transparent !important; 
    color: var(--text-light) !important; 
    font-size: 1.05rem !important; 
    border: none !important; 
    padding: 1.2rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    line-height: 1.5 !important;
    resize: none !important;
}

.stChatInput textarea::placeholder {
    color: rgba(241, 245, 249, 0.5) !important;
}

.stChatInput button {
    background: linear-gradient(135deg, var(--primary-cyan) 0%, var(--primary-purple) 100%) !important;
    border: none !important; 
    border-radius: 16px !important; 
    color: #fff !important; 
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 16px rgba(0, 212, 255, 0.3) !important;
}

.stChatInput button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4) !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary-cyan), var(--primary-purple));
    border-radius: 4px;
    transition: all 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--primary-purple), var(--primary-green));
}

/* Add some spacing at the bottom for fixed input */
.main-content {
    padding-bottom: 120px;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Quantum Canvas (JS contained in components.html only)
# -------------------------------------------------------
from streamlit.components.v1 import html as components_html

def inject_quantum_canvas():
    """
    Draws a full-screen canvas behind content with quantum-inspired particles
    """
    key = str(uuid.uuid4())
    components_html(dedent(f"""
    <div id="qc-wrap-{key}" style="position:fixed; inset:0; z-index:1; pointer-events:none;">
      <canvas id="qc-canvas-{key}" style="width:100%; height:100%; display:block;"></canvas>
    </div>
    <script>
    (function(){{
      const canvas = document.getElementById(`qc-canvas-{key}`);
      const ctx = canvas.getContext("2d");
      let w, h, dpr;

      function resize(){{
        dpr = window.devicePixelRatio || 1;
        w = canvas.clientWidth;
        h = canvas.clientHeight;
        canvas.width = Math.floor(w * dpr);
        canvas.height = Math.floor(h * dpr);
        ctx.setTransform(dpr,0,0,dpr,0,0);
      }}
      resize();
      window.addEventListener("resize", resize);

      function rand(a=0,b=1){{ return a + Math.random()*(b-a); }}
      function lerp(a,b,t){{ return a + (b-a)*t; }}
      function clamp(v,a,b){{ return Math.max(a,Math.min(b,v)); }}
      function hash(n){{ return Math.sin(n*1e4)*1e4 - Math.floor(Math.sin(n*1e4)*1e4); }}

      function vnoise2(x,y){{
        const xi = Math.floor(x), yi = Math.floor(y);
        const xf = x - xi, yf = y - yi;
        const h = (i,j)=>hash((i*183.1567)^(j*97.345));
        const v00 = h(xi,yi), v10 = h(xi+1,yi), v01 = h(xi,yi+1), v11 = h(xi+1,yi+1);
        const sx = xf*xf*(3-2*xf), sy = yf*yf*(3-2*yf);
        const ix0 = v00*(1-sx) + v10*sx;
        const ix1 = v01*(1-sx) + v11*sx;
        return ix0*(1-sy) + ix1*sy;
      }}

      function flowField(x,y,t){{
        const nx = x / w, ny = y / h;
        const a = Math.sin( (nx*6.0 + t*0.06) * Math.PI*2 );
        const b = Math.cos( (ny*4.0 - t*0.04) * Math.PI*2 );
        const c = Math.sin( ((nx+ny)*4.0 + t*0.03) * Math.PI*2 );

        const n1 = vnoise2(nx*4.0 + t*0.02, ny*4.0 - t*0.015);
        const n2 = vnoise2(nx*2.0 - t*0.01, ny*6.0 + t*0.02);

        const vx =  0.3*a + 0.25*c + 0.4*(n1-0.5);
        const vy = -0.25*b + 0.3*c + 0.4*(n2-0.5);
        return [vx, vy];
      }}

      const barriers = [
        {{ x: 0.2, y: 0.3, w: 0.6, h: 0.015 }},
        {{ x: 0.1, y: 0.7, w: 0.8, h: 0.012 }}
      ];
      
      function inBarrier(x,y){{
        for (let b of barriers){{
          const bx = b.x*w, by = b.y*h, bw = b.w*w, bh = b.h*h;
          if (x>=bx && x<=bx+bw && y>=by && y<=by+bh) return true;
        }}
        return false;
      }}

      const COUNT = Math.floor(Math.min(180, (w*h)/40000));
      const particles = [];
      const nowSeed = Math.random()*1000;

      for (let i=0;i<COUNT;i++){{
        const seed = nowSeed + i*13.37;
        particles.push({{
          x: rand(0,w),
          y: rand(0,h),
          vx: 0, vy: 0,
          baseSize: rand(0.5, 1.2),
          blur: rand(0.3, 1.5),
          alpha: rand(0.2, 0.45),
          jitter: rand(0.08, 0.3),
          seed,
          life: rand(4,12),
          tlife: 0,
          hue: rand(180, 280)
        }});
      }}

      let last = performance.now();
      function step(ts){{
        const dt = Math.min(0.04, (ts - last) / 1000);
        last = ts;

        ctx.clearRect(0,0,w,h);

        // Ambient glow
        ctx.save();
        ctx.globalAlpha = 0.03;
        const grad = ctx.createRadialGradient(w*0.5,h*0.4,0, w*0.5,h*0.4, Math.max(w,h)*0.8);
        grad.addColorStop(0, `rgba(0,212,255,0.08)`);
        grad.addColorStop(0.6, `rgba(139,92,246,0.06)`);
        grad.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = grad;
        ctx.fillRect(0,0,w,h);
        ctx.restore();

        const t = ts/1000;

        for (let p of particles){{
          const [fx,fy] = flowField(p.x, p.y, t);
          const jx = (hash(p.seed + t*0.5)-0.5) * p.jitter;
          const jy = (hash(p.seed*1.7 + t*0.5)-0.5) * p.jitter;

          p.vx = lerp(p.vx, fx*20 + jx, 0.04);
          p.vy = lerp(p.vy, fy*20 + jy, 0.04);

          let nx = p.x + p.vx*dt;
          let ny = p.y + p.vy*dt;

          if (inBarrier(nx,ny)){{
            if (Math.random() < 0.05){{
              nx += (Math.random() < 0.5 ? 30 : -30) * (0.3 + Math.random());
              ny += (Math.random() < 0.5 ? 20 : -20) * (0.3 + Math.random());
            }} else {{
              nx += (Math.random()<0.5 ? -1 : 1) * 4;
              ny += (Math.random()<0.5 ? -1 : 1) * 1.5;
            }}
          }}

          if (nx < -8) nx = w + 8;
          if (nx > w + 8) nx = -8;
          if (ny < -8) ny = h + 8;
          if (ny > h + 8) ny = -8;

          p.x = nx; p.y = ny;

          const breathe = 0.7 + 0.3*Math.sin(t*1.5 + p.seed);
          const alpha = clamp(p.alpha * (0.6 + 0.4*Math.sin(t*1.2 + p.seed*1.1)), 0.08, 0.5);
          const size = p.baseSize * breathe;
          const blur = p.blur * (0.8 + 0.4*hash(p.seed + t*0.2));

          // Dynamic color shifting
          const hue = (p.hue + t*10 + p.seed*50) % 360;
          const color1 = `hsla(${{hue}}, 70%, 60%, ${{alpha}})`;
          const color2 = `hsla(${{(hue + 60) % 360}}, 60%, 50%, ${{alpha*0.5}})`;

          ctx.save();
          ctx.filter = `blur(${{blur}}px)`;
          const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, size*5);
          g.addColorStop(0, color1);
          g.addColorStop(0.7, color2);
          g.addColorStop(1, "rgba(0,0,0,0)");
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(p.x, p.y, size*5, 0, Math.PI*2);
          ctx.fill();
          ctx.restore();

          p.tlife += dt;
          if (p.tlife > p.life){{
            if (Math.random() < 0.2){{
              p.x = rand(0,w); p.y = rand(0,h);
            }}
            p.tlife = 0; p.life = rand(4,12);
            p.hue = rand(180, 280);
          }}
        }}
        requestAnimationFrame(step);
      }}
      requestAnimationFrame(step);
    }})();
    </script>
    """), height=0)


# ------------------------
# Improved typing effect without "analyzing" message
# ------------------------
def stream_response(response_text: str):
    words = response_text.split()
    streamed = ""
    placeholder = st.empty()

    for i, w in enumerate(words):
        streamed += w + " "
        html = advanced_markdown(streamed.strip())
        placeholder.markdown(
            f"""
            <div class="message assistant-message">
                <div class="msg-header enviro-header">🌿 Enviro</div>
                <div class="msg-content">{html}<span style="color:var(--primary-purple);animation: blink 1s infinite;font-weight:bold;">|</span></div>
            </div>
            <style>@keyframes blink {{0%,50%{{opacity:1}} 51%,100%{{opacity:0}}}}</style>
            """,
            unsafe_allow_html=True,
        )

        # Variable pacing for more natural typing
        if w.endswith((".", "!", "?")):
            time.sleep(0.12)
        elif w.endswith((",", ":", ";")):
            time.sleep(0.06)
        elif len(w) > 8:
            time.sleep(0.04)
        else:
            time.sleep(0.025)

    # Final render without cursor
    final_html = advanced_markdown(streamed.strip())
    placeholder.markdown(
        f"""
        <div class="message assistant-message">
            <div class="msg-header enviro-header">🌿 Enviro</div>
            <div class="msg-content">{final_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return streamed.strip()


# -------------
# Main UI
# -------------
def main():
    initialize_session_state()

    # Enhanced header with subtitle
    st.markdown(
        """
        <div class="header">
            <h1 class="title">🌿 Meet Enviro</h1>
            <p class="subtitle">Your Quantum-Enhanced Environmental Intelligence Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Background canvas
    inject_quantum_canvas()

    # Main content wrapper
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Welcome message (only show when no messages)
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="welcome">
                <h2>Welcome to EnviroCast AI</h2>
                <p>
                    I'm Enviro, your quantum-enhanced environmental intelligence assistant. 
                    I specialize in air quality analysis, pollution science, environmental monitoring, 
                    and sustainable solutions. Ask me anything about environmental challenges, 
                    climate science, or how technology can help protect our planet.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render message history
    for m in st.session_state.messages:
        content = advanced_markdown(m["content"])
        if m["role"] == "user":
            st.markdown(
                f"""
                <div class="message user-message">
                    <div class="msg-header user-header">👤 You</div>
                    <div class="msg-content">{content}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="message assistant-message">
                    <div class="msg-header enviro-header">🌿 Enviro</div>
                    <div class="msg-content">{content}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)  # Close chat-container
    st.markdown("</div>", unsafe_allow_html=True)  # Close main-content

    # Chat input with enhanced placeholder
    prompt = st.chat_input("Ask about environmental science, air quality, pollution analysis, or climate solutions…")

    if prompt:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message immediately
        user_html = advanced_markdown(prompt)
        with st.container():
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="message user-message">
                        <div class="msg-header user-header">👤 You</div>
                        <div class="msg-content">{user_html}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Get and display assistant response
        try:
            response = st.session_state.chat_session.send_message(prompt)
            
            with st.container():
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                full_response = stream_response(response.text)
                st.markdown("</div>", unsafe_allow_html=True)

            # Store assistant message
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()

        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "quota" in error_msg:
                error_text = "🔄 <em>API rate limit reached. Please try again in a moment.</em>"
            elif "timeout" in error_msg:
                error_text = "⏱️ <em>Request timed out. Please try again.</em>"
            else:
                error_text = "🔄 <em>Something went wrong. Please try again in a moment.</em>"
                
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="message assistant-message" style="
                        border-left-color: #ef4444;
                        background: linear-gradient(135deg,
                            rgba(239,68,68,0.15) 0%,
                            rgba(239,68,68,0.08) 50%,
                            rgba(239,68,68,0.05) 100%);
                    ">
                        <div class="msg-header" style="color: #f87171; text-shadow: 0 0 15px rgba(248,113,113,0.4);">
                            ⚠️ Error
                        </div>
                        <div class="msg-content" style="color: #fca5a5;">
                            <strong>Error:</strong> {str(e)}<br><br>
                            {error_text}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
