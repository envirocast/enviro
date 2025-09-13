import streamlit as st
import google.generativeai as genai
import time
import os
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
# Styles
# -------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global reset and base styling */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, .stApp {
    background: #000000 !important;
    color: #ffffff !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    height: 100vh !important;
    overflow: hidden !important;
}

.stApp > div:first-child {
    height: 100vh !important;
    overflow: hidden !important;
}

/* Hide Streamlit elements */
#MainMenu, footer, header, .stDeployButton { 
    visibility: hidden !important; 
    height: 0 !important;
}

/* App container - full height with proper flex layout */
.app-container {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    position: relative !important;
    z-index: 10 !important;
}

/* Header - fixed height, no scroll */
.header {
    flex: 0 0 auto !important;
    text-align: center;
    padding: 2rem 0 1rem 0;
    position: relative;
    z-index: 20;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(20px);
}

.title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s ease-in-out infinite;
    margin: 0;
}

@keyframes shimmer {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Main content area - flexible height */
.main-content {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    position: relative !important;
    z-index: 15 !important;
}

/* Welcome section - only shown when no messages */
.welcome-section {
    flex: 0 0 auto !important;
    padding: 0 2rem 2rem 2rem;
}

.welcome {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(139, 92, 246, 0.05));
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    max-width: 800px;
    margin: 0 auto;
}

.welcome h2 {
    margin-bottom: 0.5rem;
    color: #ffffff;
    font-size: 1.8rem;
}

.welcome p {
    color: #cccccc;
    margin: 0;
    font-size: 1.1rem;
    line-height: 1.5;
}

/* Chat messages area - scrollable */
.chat-messages {
    flex: 1 1 auto !important;
    overflow-y: auto !important;
    padding: 0 2rem;
    margin-bottom: 1rem;
}

.chat-messages::-webkit-scrollbar {
    width: 8px;
}
.chat-messages::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}
.chat-messages::-webkit-scrollbar-thumb {
    background: #8B5CF6;
    border-radius: 10px;
}

/* Messages */
.message {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding: 1.5rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 1.5rem;
}

.user-message {
    flex-direction: row-reverse;
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 212, 255, 0.05));
    border-color: rgba(0, 212, 255, 0.3);
}

.assistant-message {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05));
    border-color: rgba(139, 92, 246, 0.3);
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}

.user-avatar {
    background: linear-gradient(135deg, #00D4FF, #0EA5E9);
}

.assistant-avatar {
    background: linear-gradient(135deg, #8B5CF6, #A78BFA);
}

.message-content {
    flex: 1;
    line-height: 1.6;
}

.message-content h1, .message-content h2, .message-content h3 {
    color: #ffffff;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

.message-content code {
    background: rgba(0, 0, 0, 0.5);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    color: #00D4FF;
    font-size: 0.9rem;
}

.message-content pre {
    background: rgba(0, 0, 0, 0.7);
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

/* Chat Input - fixed at bottom */
.chat-input-section {
    flex: 0 0 auto !important;
    padding: 1rem 2rem 2rem 2rem;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(20px);
    position: relative;
    z-index: 25;
}

.stChatInput > div {
    max-width: 800px !important;
    margin: 0 auto !important;
}

.stChatInput > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}

.stChatInput textarea {
    background: transparent !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 16px !important;
}

.stChatInput button {
    background: linear-gradient(135deg, #00D4FF, #8B5CF6) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

/* Typing indicator */
.typing {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    color: #8B5CF6;
}

.typing-dot {
    width: 6px;
    height: 6px;
    background: #8B5CF6;
    border-radius: 50%;
    animation: typing 1.5s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.3s; }
.typing-dot:nth-child(3) { animation-delay: 0.6s; }

@keyframes typing {
    0%, 60%, 100% { opacity: 0.3; }
    30% { opacity: 1; }
}

/* Quantum canvas - truly in background */
.quantum-background {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 1 !important;
    pointer-events: none !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------
# Quantum Canvas with Entanglement
# -------------------------------------------
from streamlit.components.v1 import html as components_html

def inject_quantum_canvas():
    key = str(uuid.uuid4())
    components_html(dedent(f"""
    <div class="quantum-background">
        <canvas id="canvas-{key}" style="width: 100%; height: 100%;"></canvas>
    </div>
    
    <script>
    (function() {{
        const canvas = document.getElementById('canvas-{key}');
        const ctx = canvas.getContext('2d');
        
        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        resize();
        window.addEventListener('resize', resize);
        
        class Particle {{
            constructor() {{
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.3;
                this.vy = (Math.random() - 0.5) * 0.3;
                this.size = Math.random() * 2 + 1;
                this.opacity = Math.random() * 0.4 + 0.1;
                this.color = 'rgba(0, 212, 255, ';
                this.entangled = null;
                this.trail = [];
                this.trailLength = 6;
            }}
            
            update() {{
                this.trail.push({{x: this.x, y: this.y}});
                if (this.trail.length > this.trailLength) {{
                    this.trail.shift();
                }}
                
                // Entangled particles move together
                if (this.entangled) {{
                    const dx = this.entangled.x - this.x;
                    const dy = this.entangled.y - this.y;
                    const distance = Math.sqrt(dx*dx + dy*dy);
                    
                    if (distance > 40) {{
                        this.vx += dx * 0.0008;
                        this.vy += dy * 0.0008;
                    }}
                }}
                
                // Gentle random movement
                this.vx += (Math.random() - 0.5) * 0.03;
                this.vy += (Math.random() - 0.5) * 0.03;
                
                // Apply velocity
                this.x += this.vx;
                this.y += this.vy;
                
                // Wrap around edges
                if (this.x < 0) this.x = canvas.width;
                if (this.x > canvas.width) this.x = 0;
                if (this.y < 0) this.y = canvas.height;
                if (this.y > canvas.height) this.y = 0;
                
                // Damping
                this.vx *= 0.98;
                this.vy *= 0.98;
            }}
            
            draw() {{
                // Draw particle trail
                if (this.trail.length > 1) {{
                    for (let i = 0; i < this.trail.length - 1; i++) {{
                        const alpha = (i / this.trail.length) * this.opacity * 0.3;
                        ctx.save();
                        ctx.globalAlpha = alpha;
                        ctx.strokeStyle = this.color + alpha + ')';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(this.trail[i].x, this.trail[i].y);
                        ctx.lineTo(this.trail[i + 1].x, this.trail[i + 1].y);
                        ctx.stroke();
                        ctx.restore();
                    }}
                }}
                
                // Draw particle
                ctx.save();
                ctx.globalAlpha = this.opacity;
                
                // Outer glow
                ctx.shadowBlur = this.entangled ? 40 : 25;
                ctx.shadowColor = this.color + '0.8)';
                
                // Core particle
                const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 3);
                gradient.addColorStop(0, this.color + '1)');
                gradient.addColorStop(0.4, this.color + '0.6)');
                gradient.addColorStop(1, this.color + '0)');
                
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw entanglement connection
                if (this.entangled && this.entangled.x < this.x) {{
                    ctx.globalAlpha = 0.5;
                    ctx.strokeStyle = this.color + '0.7)';
                    ctx.lineWidth = 1.5;
                    ctx.shadowBlur = 15;
                    ctx.shadowColor = this.color + '0.9)';
                    
                    const dashOffset = Date.now() * 0.02;
                    ctx.setLineDash([10, 8]);
                    ctx.lineDashOffset = dashOffset;
                    
                    ctx.beginPath();
                    ctx.moveTo(this.x, this.y);
                    ctx.lineTo(this.entangled.x, this.entangled.y);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }}
                
                ctx.restore();
            }}
        }}
        
        const particles = [];
        const particleCount = Math.floor((canvas.width * canvas.height) / 15000);
        
        for (let i = 0; i < particleCount; i++) {{
            particles.push(new Particle());
        }}
        
        function checkEntanglement() {{
            for (let i = 0; i < particles.length; i++) {{
                for (let j = i + 1; j < particles.length; j++) {{
                    const p1 = particles[i];
                    const p2 = particles[j];
                    
                    if (p1.entangled || p2.entangled) continue;
                    
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const distance = Math.sqrt(dx*dx + dy*dy);
                    
                    if (distance < 60) {{
                        p1.entangled = p2;
                        p2.entangled = p1;
                        
                        setTimeout(() => {{
                            if (Math.random() < 0.7) {{
                                if (p1.entangled === p2) p1.entangled = null;
                                if (p2.entangled === p1) p2.entangled = null;
                            }}
                        }}, Math.random() * 4000 + 3000);
                    }}
                }}
            }}
        }}
        
        function animate() {{
            // Clear with slight trail effect
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(particle => {{
                particle.update();
                particle.draw();
            }});
            
            if (Math.random() < 0.15) {{
                checkEntanglement();
            }}
            
            requestAnimationFrame(animate);
        }}
        
        animate();
    }})();
    </script>
    """), height=0)

# -------------------------------------------
# Chat Functions
# -------------------------------------------
def display_message(role, content, avatar_icon):
    avatar_class = "user-avatar" if role == "user" else "assistant-avatar"
    message_class = "user-message" if role == "user" else "assistant-message"
    
    st.markdown(f"""
    <div class="message {message_class}">
        <div class="avatar {avatar_class}">{avatar_icon}</div>
        <div class="message-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def typing_indicator():
    return """
    <div class="message assistant-message">
        <div class="avatar assistant-avatar">🌿</div>
        <div class="message-content">
            <div class="typing">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span style="margin-left: 0.5rem;">Enviro is analyzing...</span>
            </div>
        </div>
    </div>
    """

def stream_response(response_text):
    typing_placeholder = st.empty()
    typing_placeholder.markdown(typing_indicator(), unsafe_allow_html=True)
    
    time.sleep(1.5)
    
    typing_placeholder.empty()
    display_message("assistant", response_text, "🌿")
    
    return response_text

# -------------
# Main App
# -------------
def main():
    initialize_session_state()
    
    # Inject quantum canvas first (background)
    inject_quantum_canvas()
    
    # Main app container
    st.markdown('<div class="app-container">', unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
    <div class="header">
        <h1 class="title">🌿 Meet Enviro</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Welcome section (only show when no messages)
    if not st.session_state.messages:
        st.markdown('<div class="welcome-section">', unsafe_allow_html=True)
        st.markdown("""
        <div class="welcome">
            <h2>Welcome to EnviroCast AI</h2>
            <p>I'm Enviro, your environmental intelligence assistant. Ask me about air quality, pollution, climate solutions, and environmental science.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat messages area
    if st.session_state.messages:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                display_message("user", message["content"], "👤")
            else:
                display_message("assistant", message["content"], "🌿")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End main-content
    
    # Chat input section
    st.markdown('<div class="chat-input-section">', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about environmental science, air quality, or climate solutions..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Rerun to display the user message and start the generation process
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # End chat-input-section
    st.markdown('</div>', unsafe_allow_html=True)  # End app-container

    # After a prompt has been submitted and the page is rerunning,
    # we check the last message to see if it's from the user and needs a response.
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        prompt = st.session_state.messages[-1]["content"]
        
        try:
            response = st.session_state.chat_session.send_message(prompt)
            full_response = stream_response(response.text)
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = f"⚠️ **Error:** {str(e)}<br><br>Please try again in a moment."
            display_message("assistant", error_message, "⚠️")

        # Rerun once more to show the complete response
        st.rerun()

if __name__ == "__main__":
    main()
