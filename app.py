import streamlit as st
import google.generativeai as genai
import time
import os
import re
import uuid
from textwrap import dedent
from streamlit.components.v1 import html as components_html

# ----------------------------
# Config & API initialization
# ----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(
    page_title="Meet Enviro",
    page_icon="🌎",
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
# -------------------------------------------
def advanced_markdown(text: str) -> str:
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = re.sub(r"^### (.*)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.*)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.*)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)\*(?<!\*)", r"<em>\1</em>", text)

    def code_repl(m):
        code = m.group(1).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<code>{code}</code>"
    text = re.sub(r"`([^`]+)`", code_repl, text)

    def pre_repl(m):
        code = m.group(1).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre>{code}</pre>"
    text = re.sub(r"```(.*?)```", pre_repl, text, flags=re.DOTALL)

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)

    lines = text.split("\n")
    out, in_ul, in_ol = [], False, False
    for ln in lines:
        m_ul = re.match(r"^\s*[-\*\u2022]\s+(.*)$", ln)
        m_ol = re.match(r"^\s*(\d+)\.\s+(.*)$", ln)
        if m_ul:
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{m_ul.group(1)}</li>")
        elif m_ol:
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{m_ol.group(2)}</li>")
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            out.append(ln)
    if in_ul: out.append("</ul>")
    if in_ol: out.append("</ol>")
    text = "\n".join(out)

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    formatted = []
    for p in paragraphs:
        if p.startswith(("<h1", "<h2", "<h3", "<ul", "<ol", "<pre", "<li")):
            formatted.append(p)
        else:
            formatted.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    return "\n".join(formatted)

# -------------------------------------------------------
# Quantum Canvas injection
# -------------------------------------------------------
def inject_quantum_canvas():
    key = str(uuid.uuid4())
    components_html(dedent(f"""
    <div id="qc-wrap-{key}" style="position:fixed; inset:0; z-index:1; pointer-events:none;">
      <canvas id="qc-canvas-{key}" style="width:100%; height:100%; display:block;"></canvas>
    </div>
    <script>
    (function(){{
      const canvas = document.getElementById("qc-canvas-{key}");
      const ctx = canvas.getContext("2d");
      let w, h, dpr;
      function resize(){{
        dpr = window.devicePixelRatio || 1;
        w = canvas.clientWidth; h = canvas.clientHeight;
        canvas.width = Math.floor(w * dpr);
        canvas.height = Math.floor(h * dpr);
        ctx.setTransform(dpr,0,0,dpr,0,0);
      }}
      resize();
      window.addEventListener("resize", resize);
      // simple animate
      function step(){{
        ctx.clearRect(0,0,w,h);
        ctx.fillStyle="rgba(139,92,246,0.15)";
        ctx.fillRect(0,0,w,h);
        requestAnimationFrame(step);
      }}
      requestAnimationFrame(step);
    }})();
    </script>
    """), height=0)

# ------------------------
# Typing / streaming effect
# ------------------------
def stream_response(response_text: str):
    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        """
        <div class="message assistant-message">
            <div class="msg-header enviro-header">
                <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-globe" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 010 20a15.3 15.3 0 010-20z"/></svg>
                Enviro
            </div>
            <div class="msg-content"><em>Analyzing environmental data…</em></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(0.6)

    words = response_text.split()
    streamed, placeholder = "", st.empty()
    for w in words:
        streamed += w + " "
        html = advanced_markdown(streamed.strip())
        placeholder.markdown(
            f"""
            <div class="message assistant-message">
                <div class="msg-header enviro-header">
                    <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-globe" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 010 20a15.3 15.3 0 010-20z"/></svg>
                    Enviro
                </div>
                <div class="msg-content">{html}<span style="color:#8B5CF6;animation: blink 1s infinite;font-weight:bold;">|</span></div>
            </div>
            <style>@keyframes blink {{0%,50%{{opacity:1}} 51%,100%{{opacity:0}}}}</style>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.02 if not w.endswith((".", "!", "?")) else 0.08)

    final_html = advanced_markdown(streamed.strip())
    placeholder.markdown(
        f"""
        <div class="message assistant-message">
            <div class="msg-header enviro-header">
                <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-globe" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 010 20a15.3 15.3 0 010-20z"/></svg>
                Enviro
            </div>
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
    st.markdown('<div class="header"><h1 class="title">Meet Enviro</h1></div>', unsafe_allow_html=True)
    inject_quantum_canvas()
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown(
            """
            <div class="welcome">
                <h2>Welcome to EnviroCast AI</h2>
                <p>I’m Enviro, your quantum-enhanced environmental assistant.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for m in st.session_state.messages:
        content = advanced_markdown(m["content"])
        if m["role"] == "user":
            st.markdown(
                f"""
                <div class="message user-message">
                    <div class="msg-header user-header">
                        <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-user" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0113 0"/></svg>
                        You
                    </div>
                    <div class="msg-content">{content}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="message assistant-message">
                    <div class="msg-header enviro-header">
                        <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-globe" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 010 20a15.3 15.3 0 010-20z"/></svg>
                        Enviro
                    </div>
                    <div class="msg-content">{content}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    prompt = st.chat_input("Ask about environmental science...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        user_html = advanced_markdown(prompt)
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="message user-message">
                    <div class="msg-header user-header">
                        <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-user" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="7" r="4"/><path d="M5.5 21a8.38 8.38 0 0113 0"/></svg>
                        You
                    </div>
                    <div class="msg-content">{user_html}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            full = stream_response(response.text)
            st.markdown("</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": full})
            st.rerun()
        except Exception as e:
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="message assistant-message" style="border-left-color:#ef4444;">
                        <div class="msg-header" style="color:#f87171;">
                            <svg xmlns="http://www.w3.org/2000/svg" class="lucide lucide-alert-triangle" width="18" height="18" stroke="currentColor" fill="none" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                            Error
                        </div>
                        <div class="msg-content"><strong>Error:</strong> {str(e)}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

if __name__ == "__main__":
    main()
