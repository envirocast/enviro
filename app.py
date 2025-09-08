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
# Background styles (CSS only — no JS here)
# -------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

* { font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif !important; }

.stApp {
    background: linear-gradient(-45deg, #0a0a0a, #0f0f23, #1a1a3a, #2d1b69, #1e1b4b);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    25% { background-position: 100% 0%; }
    50% { background-position: 100% 100%; }
    75% { background-position: 0% 100%; }
    100% { background-position: 0% 50%; }
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }

.header {
    position: relative;
    z-index: 5;
    text-align: center;
    padding: 2rem 0 0.5rem 0;
    background: rgba(0,0,0,0.08);
    border-bottom: 1px solid rgba(0, 212, 255, 0.08);
    backdrop-filter: blur(18px);
}

.title {
    background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    animation: titleShimmer 4s ease infinite, titleFloat 6s ease-in-out infinite;
    text-shadow: 0 0 50px rgba(0, 212, 255, 0.3);
}

@media (max-width: 768px){ .title { font-size: 2.4rem; } }

@keyframes titleShimmer { 0%,100%{background-position:0% 50%;} 50%{background-position:100% 50%;} }
@keyframes titleFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1.5rem 1rem 3rem 1rem;
    position: relative;
    z-index: 5;
}

.message {
    margin-bottom: 1.1rem;
    padding: 1.4rem;
    border-radius: 18px;
    backdrop-filter: blur(20px);
    transition: transform .25s ease, box-shadow .25s ease;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 8px 28px rgba(0,0,0,0.28);
}

.user-message {
    background: linear-gradient(135deg, rgba(0,212,255,0.12), rgba(0,212,255,0.05));
    border-left: 4px solid #00D4FF;
    margin-left: 6%;
}
.assistant-message {
    background: linear-gradient(135deg, rgba(139,92,246,0.12), rgba(139,92,246,0.05));
    border-left: 4px solid #8B5CF6;
    margin-right: 6%;
}

.message:hover { transform: translateY(-2px); box-shadow: 0 16px 46px rgba(0,0,0,0.38); }

.msg-header {
    display: flex; align-items: center; gap: .6rem; margin-bottom: .7rem;
    font-weight: 700; letter-spacing: -.01em; font-size: 1rem;
}
.user-header { color: #38bdf8; text-shadow: 0 0 10px rgba(56,189,248,.28); }
.enviro-header { color: #a78bfa; text-shadow: 0 0 10px rgba(167,139,250,.28); }

.msg-content { color: #f1f5f9; line-height: 1.8; font-size: 1.03rem; letter-spacing: .01em; }
.msg-content h1, .msg-content h2, .msg-content h3 { color: #fff; font-weight: 700; margin: 1.2rem 0 .7rem; }
.msg-content h1 { font-size: 1.7rem; background: linear-gradient(135deg,#00D4FF,#8B5CF6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.msg-content h2 { font-size: 1.35rem; background: linear-gradient(135deg,#8B5CF6,#10B981); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.msg-content h3 { font-size: 1.18rem; background: linear-gradient(135deg,#10B981,#00D4FF); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.msg-content code { background: rgba(0,0,0,.6); color: #00D4FF; padding: .22rem .5rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: .95rem; border: 1px solid rgba(0,212,255,.18); }
.msg-content pre { background: rgba(0,0,0,.8); color: #f1f5f9; padding: 1.1rem; border-radius: 12px; overflow-x: auto; border: 1px solid rgba(139,92,246,.18); font-family: 'JetBrains Mono', monospace; box-shadow: 0 4px 16px rgba(0,0,0,.3); }
.msg-content a { color: #38bdf8; text-decoration: none; border-bottom: 1px solid rgba(56,189,248,.28); }
.msg-content a:hover { color: #0ea5e9; border-bottom-color: #0ea5e9; text-shadow: 0 0 15px rgba(14,165,233,.45); }
.welcome { background: linear-gradient(135deg,rgba(0,212,255,.10),rgba(139,92,246,.10),rgba(16,185,129,.10)); border-radius: 20px; padding: 1.6rem; border: 1px solid rgba(255,255,255,.08); }

.stChatInput > div > div {
    background: linear-gradient(135deg, rgba(15,23,42,.9) 0%, rgba(30,41,59,.85) 100%) !important;
    backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 28px rgba(0,0,0,.28) !important;
}
.stChatInput textarea { background: transparent !important; color: #f1f5f9 !important; font-size: 1.02rem !important; border: none !important; padding: 1rem 1.2rem !important; }
.stChatInput button {
    background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%) !important;
    border: none !important; border-radius: 12px !important; color: #fff !important; font-weight: 600 !important;
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
    Draws a full-screen canvas behind content with quantum-inspired particles:
    - Randomness: seeded per-particle noise & jitter
    - Fluid motion: layered wave/“curl-like” field
    - Uncertainty: blur/alpha/size breathing
    - Tunneling: rare teleports across barriers/edges
    """
    # unique key to avoid caching
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

      // ---------- Utilities ----------
      function rand(a=0,b=1){{ return a + Math.random()*(b-a); }}
      function lerp(a,b,t){{ return a + (b-a)*t; }}
      function clamp(v,a,b){{ return Math.max(a,Math.min(b,v)); }}
      function hash(n){{ return Math.sin(n*1e4)*1e4 - Math.floor(Math.sin(n*1e4)*1e4); }}

      // Lightweight pseudo-noise (value noise-ish)
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

      // Velocity field: layered waves + noise -> fluid-ish motion
      function flowField(x,y,t){{
        // Normalize coords
        const nx = x / w, ny = y / h;
        // Two interfering waves
        const a = Math.sin( (nx*8.0 + t*0.08) * Math.PI*2 );
        const b = Math.cos( (ny*6.0 - t*0.06) * Math.PI*2 );
        const c = Math.sin( ((nx+ny)*6.0 + t*0.05) * Math.PI*2 );

        // Value noise for advection
        const n1 = vnoise2(nx*5.0 + t*0.03, ny*5.0 - t*0.02);
        const n2 = vnoise2(nx*3.0 - t*0.02, ny*7.0 + t*0.025);

        // Compose vector; small magnitude for subtle, fluid drift
        const vx =  0.4*a + 0.35*c + 0.6*(n1-0.5);
        const vy = -0.35*b + 0.35*c + 0.6*(n2-0.5);
        return [vx, vy];
      }}

      // Virtual barriers: thin regions where tunneling can occur
      const barriers = [
        {{{{ x: 0.33, y: 0.25, w: 0.34, h: 0.02 }}}},
        {{{{ x: 0.15, y: 0.62, w: 0.7,  h: 0.018 }}}}
      ];
      function inBarrier(x,y){{
        for (let b of barriers){{
          const bx = b.x*w, by = b.y*h, bw = b.w*w, bh = b.h*h;
          if (x>=bx && x<=bx+bw && y>=by && y<=by+bh) return true;
        }}
        return false;
      }}

      // Particles
      const COUNT = Math.floor(Math.min(220, (w*h)/35000)); // density scaling
      const particles = [];
      const nowSeed = Math.random()*1000;

      for (let i=0;i<COUNT;i++){{
        const seed = nowSeed + i*17.17;
        particles.push({{{{
          x: rand(0,w),
          y: rand(0,h),
          vx: 0, vy: 0,
          baseSize: rand(0.7, 1.8),   // smaller particles
          blur: rand(0.4, 2.0),
          alpha: rand(0.25, 0.55),
          jitter: rand(0.1, 0.5),
          seed,
          life: rand(3,10),
          tlife: 0
        }}}});
      }}

      let last = performance.now();
      function step(ts){{
        const dt = Math.min(0.05, (ts - last) / 1000); // clamp for stability
        last = ts;

        ctx.clearRect(0,0,w,h);

        // Soft glow backdrop (subtle)
        ctx.save();
        ctx.globalAlpha = 0.05;
        const grad = ctx.createRadialGradient(w*0.5,h*0.5,0, w*0.5,h*0.5, Math.max(w,h)*0.7);
        grad.addColorStop(0,"rgba(139,92,246,0.12)");
        grad.addColorStop(1,"rgba(0,0,0,0)");
        ctx.fillStyle = grad;
        ctx.fillRect(0,0,w,h);
        ctx.restore();

        const t = ts/1000;

        for (let p of particles){{
          // Flow field + randomness
          const [fx,fy] = flowField(p.x, p.y, t);
          const jx = (hash(p.seed + t*0.7)-0.5) * p.jitter;
          const jy = (hash(p.seed*2.0 + t*0.7)-0.5) * p.jitter;

          // Integrate velocity (light smoothing)
          p.vx = lerp(p.vx, fx*28 + jx, 0.06);
          p.vy = lerp(p.vy, fy*28 + jy, 0.06);

          let nx = p.x + p.vx*dt;
          let ny = p.y + p.vy*dt;

          // Virtual barrier interaction: sometimes "tunnel" through
          if (inBarrier(nx,ny)){{
            // 7% chance to tunnel (teleport across barrier)
            if (Math.random() < 0.07){{
              // jump to mirrored side of barrier region
              nx += (Math.random() < 0.5 ? 40 : -40) * (0.5 + Math.random());
              ny += (Math.random() < 0.5 ? 28 : -28) * (0.5 + Math.random());
            }} else {{
              // gentle deflection along barrier
              nx += (Math.random()<0.5 ? -1 : 1) * 6;
              ny += (Math.random()<0.5 ? -1 : 1) * 2;
            }}
          }}

          // Edge wrap with tunneling flavor
          if (nx < -10) nx = w + 10;
          if (nx > w + 10) nx = -10;
          if (ny < -10) ny = h + 10;
          if (ny > h + 10) ny = -10;

          p.x = nx; p.y = ny;

          // Uncertainty: alpha flicker, size breathing, blur drift
          const breathe = 0.6 + 0.4*Math.sin(t*2.0 + p.seed);
          const alpha = clamp(p.alpha * (0.7 + 0.3*Math.sin(t*1.7 + p.seed*1.3)), 0.12, 0.65);
          const size = p.baseSize * breathe;
          const blur = p.blur * (0.7 + 0.6*hash(p.seed + t*0.35));

          // Draw particle (soft radial)
          ctx.save();
          ctx.filter = "blur(" + blur + "px)";
          const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, size*6);
          g.addColorStop(0, "rgba(0,212,255," + alpha + ")");
          g.addColorStop(0.5, "rgba(139,92,246," + alpha*0.5 + ")");
          g.addColorStop(1, "rgba(0,0,0,0)");
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(p.x, p.y, size*6, 0, Math.PI*2);
          ctx.fill();
          ctx.restore();

          // Life/tunneling reset
          p.tlife += dt;
          if (p.tlife > p.life){{
            // occasional big tunnel jump to new region
            if (Math.random() < 0.25){{
              p.x = rand(0,w); p.y = rand(0,h);
            }}
            p.tlife = 0; p.life = rand(3,10);
          }}
        }}
        requestAnimationFrame(step);
      }}
      requestAnimationFrame(step);
    }})();
    </script>
    """)), height=0)


# ------------------------
# Typing / streaming effect
# ------------------------
def stream_response(response_text: str):
    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        """
        <div class="message assistant-message">
            <div class="msg-header enviro-header">🌿 Enviro</div>
            <div class="msg-content"><em>Analyzing environmental data…</em></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Simulated "thinking" delay (short)
    time.sleep(0.6)

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
                <div class="msg-content">{html}<span style="color:#8B5CF6;animation: blink 1s infinite;font-weight:bold;">|</span></div>
            </div>
            <style>@keyframes blink {{0%,50%{{opacity:1}} 51%,100%{{opacity:0}}}}</style>
            """,
            unsafe_allow_html=True,
        )

        # variable pacing
        if w.endswith((".", "!", "?")):
            time.sleep(0.08)
        elif w.endswith((",", ":", ";")):
            time.sleep(0.045)
        else:
            time.sleep(0.02)

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
    typing_placeholder.empty()
    return streamed.strip()


# -------------
# Main UI
# -------------
def main():
    initialize_session_state()

    # Header
    st.markdown(
        """
        <div class="header">
            <h1 class="title">🌿 Meet Enviro</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Background canvas (behind everything)
    inject_quantum_canvas()

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown(
            """
            <div class="welcome">
                <h2 style="margin:0 0 .4rem 0;">Welcome to EnviroCast AI</h2>
                <p style="margin:0;">
                    I’m Enviro, your quantum-enhanced environmental intelligence assistant.
                    Ask me anything about air quality, pollution analysis, or climate solutions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render history
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

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input
    prompt = st.chat_input("Ask about environmental science, air quality, pollution analysis, or climate solutions…")

    if prompt:
        # add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # display immediately
        user_html = advanced_markdown(prompt)
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

        # get assistant response
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            full = stream_response(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

            # store assistant message
            st.session_state.messages.append({"role": "assistant", "content": full})
            st.rerun()

        except Exception as e:
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="message assistant-message" style="border-left-color:#ef4444;background:linear-gradient(135deg,rgba(239,68,68,.15),rgba(239,68,68,.05));">
                        <div class="msg-header" style="color:#f87171;">⚠️ Error</div>
                        <div class="msg-content" style="color:#fca5a5;">
                            <strong>Error:</strong> {str(e)}<br><br>
                            {"🔄 <em>API rate limit reached. Please try again in a moment.</em>" if "rate" in str(e).lower() else "🔄 <em>Please try again in a moment.</em>"}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
