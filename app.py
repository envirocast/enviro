import streamlit as st
import google.generativeai as genai
import time
import os
import re

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable")

genai.configure(api_key=GEMINI_API_KEY)

# Page configuration
st.set_page_config(
    page_title="Meet Enviro",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal Modern Interface with Advanced Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Clean animated background */
    .stApp {
        background: linear-gradient(-45deg, #0f0f23, #1a1a3a, #2d1b69, #0f172a);
        background-size: 400% 400%;
        animation: gradientFlow 12s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
    
    /* Floating quantum particles */
    .quantum-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0; overflow: hidden; pointer-events: none;
    }
    
    .particle {
        position: absolute;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.6), transparent 70%);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }
    
    .p1 { width: 4px; height: 4px; top: 10%; left: 10%; animation-delay: 0s; }
    .p2 { width: 6px; height: 6px; top: 60%; left: 80%; animation-delay: -5s; }
    .p3 { width: 3px; height: 3px; top: 80%; left: 20%; animation-delay: -10s; }
    .p4 { width: 5px; height: 5px; top: 30%; left: 70%; animation-delay: -15s; }
    
    @keyframes float {
        0% { transform: translate(0, 100vh) rotate(0deg); opacity: 0; }
        10%, 90% { opacity: 0.8; }
        100% { transform: translate(-200px, -100vh) rotate(360deg); opacity: 0; }
    }
    
    /* Simple title */
    .title {
        background: linear-gradient(135deg, #00D4FF, #8B5CF6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 3rem 0;
        animation: titleGlow 3s ease infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.3)); }
        50% { filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.5)); }
    }
    
    /* Clean container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 2rem 2rem 2rem;
        position: relative;
        z-index: 10;
    }
    
    /* Minimal message styling */
    .message {
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 16px;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        animation: messageIn 0.5s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes messageIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00D4FF;
        margin-left: 10%;
    }
    
    .assistant-message {
        background: rgba(139, 92, 246, 0.1);
        border-left: 4px solid #8B5CF6;
        margin-right: 10%;
    }
    
    .message:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Simple message header */
    .msg-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .user-header { color: #00D4FF; }
    .enviro-header { color: #8B5CF6; }
    
    /* Clean content styling */
    .msg-content {
        color: #e2e8f0;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .msg-content h1, .msg-content h2, .msg-content h3 {
        color: #f1f5f9;
        margin: 1rem 0 0.5rem 0;
        font-weight: 600;
    }
    
    .msg-content h1 { font-size: 1.5rem; }
    .msg-content h2 { font-size: 1.3rem; }
    .msg-content h3 { font-size: 1.1rem; }
    
    .msg-content ul, .msg-content ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .msg-content li { margin: 0.3rem 0; }
    
    .msg-content strong {
        color: #f1f5f9;
        font-weight: 600;
    }
    
    .msg-content code {
        background: rgba(0, 212, 255, 0.2);
        color: #00D4FF;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .msg-content a {
        color: #00D4FF;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .msg-content a:hover {
        color: #38bdf8;
        text-shadow: 0 0 5px rgba(0, 212, 255, 0.5);
    }
    
    /* Welcome message */
    .welcome {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        animation: welcomePulse 4s ease infinite;
    }
    
    @keyframes welcomePulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.1); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.2); }
    }
    
    .welcome h2 {
        color: #f1f5f9;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .welcome p {
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    /* Minimal chat input */
    .stChatInput > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div > div:focus-within {
        border-color: #00D4FF !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2) !important;
    }
    
    .stChatInput textarea {
        background: transparent !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        border: none !important;
        padding: 1rem !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #64748b !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #00D4FF, #8B5CF6) !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Typing animation */
    .typing {
        color: #8B5CF6;
        font-style: italic;
        margin: 1rem 0;
    }
    
    .dot {
        animation: typingDots 1.4s infinite;
        font-size: 1.2rem;
    }
    
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingDots {
        0%, 80%, 100% { opacity: 0.3; }
        40% { opacity: 1; }
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .chat-container {
            padding: 0 1rem 1rem 1rem;
        }
        
        .title {
            font-size: 2rem;
        }
        
        .user-message {
            margin-left: 5%;
        }
        
        .assistant-message {
            margin-right: 5%;
        }
    }
</style>

<!-- Minimal quantum particles -->
<div class="quantum-bg">
    <div class="particle p1"></div>
    <div class="particle p2"></div>
    <div class="particle p3"></div>
    <div class="particle p4"></div>
</div>
""", unsafe_allow_html=True)

# Generation configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# System instruction
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
EnviroCast (web: https://envirocast.github.io is a platform designed to educate people on pollution, environmental effects, and air quality prediction.
It uses advanced technologies, including a hybrid quantum-classical algorithm, to monitor and predict air quality.
The site includes interactive simulations, models, and visualizations to help users understand environmental challenges and solutions.
Social media campaign: Instagram @envirocast_tech.

Always provide citations at the end of every response using good and credible sources:

Make sure to only talk about environmental, focus only on the topics mentioned in these instructions, do not involve in anything unrelated to the topic or anything illegal or negative.

You are ONLY an -informational- chatbot.
"""

def initialize_session_state():
    if 'chat_model' not in st.session_state:
        st.session_state.chat_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=SYSTEM_INSTRUCTION,
        )

    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = st.session_state.chat_model.start_chat(history=[])

    if 'messages' not in st.session_state:
        st.session_state.messages = []

def simple_markdown(text):
    """Simple markdown conversion"""
    # Headers
    text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold and italic
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Lists
    text = re.sub(r'^[•-] (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>(?:\s*<li>.*?</li>)*)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    
    # Line breaks
    text = text.replace('\n\n', '<br><br>')
    text = text.replace('\n', '<br>')
    
    return text

def stream_response(response_text):
    """Clean streaming effect"""
    # Show typing
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="message assistant-message">
        <div class="msg-header enviro-header">
            🌎 Enviro
        </div>
        <div class="typing">
            Thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1.5)
    
    # Stream response
    words = response_text.split()
    streamed_text = ""
    placeholder = st.empty()
    
    for word in words:
        streamed_text += word + " "
        current_html = simple_markdown(streamed_text)
        
        placeholder.markdown(f"""
        <div class="message assistant-message">
            <div class="msg-header enviro-header">
                🌎 Enviro
            </div>
            <div class="msg-content">
                {current_html}<span style="color: #8B5CF6; animation: blink 1s infinite;">|</span>
            </div>
        </div>
        <style>
        @keyframes blink {{ 0%, 50% {{ opacity: 1; }} 51%, 100% {{ opacity: 0; }} }}
        </style>
        """, unsafe_allow_html=True)
        
        time.sleep(0.04)
    
    # Final without cursor
    final_html = simple_markdown(streamed_text.strip())
    placeholder.markdown(f"""
    <div class="message assistant-message">
        <div class="msg-header enviro-header">
            🌎 Enviro
        </div>
        <div class="msg-content">
            {final_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return streamed_text.strip()

def main():
    initialize_session_state()

    # Title and container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">🌎 Meet Enviro</h1>', unsafe_allow_html=True)
    
    # Welcome message
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome">
            <h2>Welcome to EnviroCast AI</h2>
            <p>I'm Enviro, your environmental intelligence assistant. Ask me about air quality, pollution, climate solutions, or environmental science!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        content = simple_markdown(message["content"])
        
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user-message">
                <div class="msg-header user-header">👤 You</div>
                <div class="msg-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message assistant-message">
                <div class="msg-header enviro-header">🌎 Enviro</div>
                <div class="msg-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    prompt = st.chat_input("Ask about environmental science, air quality, or climate solutions...")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message
        user_content = simple_markdown(prompt)
        st.markdown(f"""
        <div class="chat-container">
            <div class="message user-message">
                <div class="msg-header user-header">👤 You</div>
                <div class="msg-content">{user_content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate response
        try:
            response = st.session_state.chat_session.send_message(prompt)
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            full_response = stream_response(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to session
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
            st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="chat-container">
                <div class="message assistant-message" style="border-left-color: #ef4444;">
                    <div class="msg-header" style="color: #ef4444;">⚠️ Error</div>
                    <div class="msg-content" style="color: #fca5a5;">
                        {str(e)}<br><br>
                        {"🔄 API rate limit reached. Please wait a moment." if "rate_limit" in str(e).lower() else "🔄 Please try again."}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
