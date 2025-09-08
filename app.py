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

# Advanced EnviroCast Interface with Background Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif !important;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Full screen animated background matching EnviroCast */
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
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
    
    /* Advanced quantum background with moving elements */
    .quantum-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 1; overflow: hidden; pointer-events: none;
    }
    
    /* Floating geometric shapes */
    .shape {
        position: absolute;
        opacity: 0.1;
        border-radius: 50%;
        background: linear-gradient(135deg, #00D4FF, #8B5CF6);
        animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .shape1 {
        width: 200px; height: 200px;
        top: 10%; left: -100px;
        animation: drift1 25s infinite linear;
    }
    
    .shape2 {
        width: 150px; height: 150px;
        top: 50%; right: -75px;
        animation: drift2 30s infinite linear;
    }
    
    .shape3 {
        width: 100px; height: 100px;
        bottom: 20%; left: 20%;
        animation: drift3 20s infinite linear;
    }
    
    .shape4 {
        width: 80px; height: 80px;
        top: 70%; right: 30%;
        animation: drift4 35s infinite linear;
    }
    
    @keyframes drift1 {
        0% { transform: translateX(-200px) translateY(0) rotate(0deg); }
        100% { transform: translateX(calc(100vw + 200px)) translateY(-100px) rotate(360deg); }
    }
    
    @keyframes drift2 {
        0% { transform: translateX(200px) translateY(0) rotate(0deg); }
        100% { transform: translateX(calc(-100vw - 200px)) translateY(150px) rotate(-360deg); }
    }
    
    @keyframes drift3 {
        0% { transform: translateY(100px) rotate(0deg) scale(1); }
        50% { transform: translateY(-50px) rotate(180deg) scale(1.2); }
        100% { transform: translateY(100px) rotate(360deg) scale(1); }
    }
    
    @keyframes drift4 {
        0% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(100px, -100px) rotate(90deg); }
        50% { transform: translate(0, -200px) rotate(180deg); }
        75% { transform: translate(-100px, -100px) rotate(270deg); }
        100% { transform: translate(0, 0) rotate(360deg); }
    }
    
    /* Quantum particles with better movement */
    .particle {
        position: absolute;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.8), rgba(139, 92, 246, 0.4), transparent);
        border-radius: 50%;
        filter: blur(1px);
    }
    
    .p1 { width: 3px; height: 3px; top: 20%; left: 15%; animation: float1 18s infinite ease-in-out; }
    .p2 { width: 5px; height: 5px; top: 60%; left: 70%; animation: float2 22s infinite ease-in-out; }
    .p3 { width: 4px; height: 4px; top: 80%; left: 30%; animation: float3 16s infinite ease-in-out; }
    .p4 { width: 2px; height: 2px; top: 40%; left: 80%; animation: float4 24s infinite ease-in-out; }
    .p5 { width: 6px; height: 6px; top: 10%; left: 60%; animation: float5 20s infinite ease-in-out; }
    .p6 { width: 3px; height: 3px; top: 70%; left: 10%; animation: float6 26s infinite ease-in-out; }
    
    @keyframes float1 {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.4; }
        25% { transform: translate(150px, -100px) scale(1.5); opacity: 1; }
        50% { transform: translate(-50px, -200px) scale(0.8); opacity: 0.6; }
        75% { transform: translate(-100px, 50px) scale(1.2); opacity: 0.8; }
    }
    
    @keyframes float2 {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
        33% { transform: translate(-200px, -150px) scale(1.3); opacity: 1; }
        66% { transform: translate(100px, -100px) scale(0.7); opacity: 0.7; }
    }
    
    @keyframes float3 {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
        50% { transform: translate(200px, -300px) scale(1.4); opacity: 1; }
    }
    
    @keyframes float4 {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
        25% { transform: translate(-100px, 150px) scale(1.8); opacity: 0.9; }
        50% { transform: translate(-250px, -100px) scale(0.5); opacity: 0.5; }
        75% { transform: translate(50px, 200px) scale(1.1); opacity: 0.7; }
    }
    
    @keyframes float5 {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.4; }
        40% { transform: translate(-150px, 200px) scale(0.8); opacity: 1; }
        80% { transform: translate(100px, -150px) scale(1.6); opacity: 0.6; }
    }
    
    @keyframes float6 {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
        30% { transform: translate(300px, -50px) scale(1.2); opacity: 1; }
        60% { transform: translate(-100px, -250px) scale(0.9); opacity: 0.7; }
    }
    
    /* Enhanced header */
    .header {
        position: relative;
        z-index: 10;
        text-align: center;
        padding: 2rem 0;
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 212, 255, 0.1);
    }
    
    .title {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        animation: titleShimmer 4s ease infinite, titleFloat 6s ease-in-out infinite;
        text-shadow: 0 0 50px rgba(0, 212, 255, 0.3);
    }
    
    @keyframes titleShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Clean container with better contrast */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
        position: relative;
        z-index: 10;
        min-height: calc(100vh - 200px);
    }
    
    /* Enhanced message styling with better contrast */
    .message {
        margin-bottom: 1.5rem;
        padding: 1.8rem;
        border-radius: 20px;
        backdrop-filter: blur(25px);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        animation: messageSlide 0.6s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes messageSlide {
        from { opacity: 0; transform: translateY(30px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 212, 255, 0.05) 100%);
        border-left: 4px solid #00D4FF;
        margin-left: 8%;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-left: 4px solid #8B5CF6;
        margin-right: 8%;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.1);
    }
    
    .message:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
    }
    
    /* Better contrast message headers */
    .msg-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: -0.01em;
    }
    
    .user-header { 
        color: #38bdf8; 
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }
    .enviro-header { 
        color: #a78bfa; 
        text-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
    }
    
    /* Enhanced content with better readability */
    .msg-content {
        color: #f1f5f9;
        line-height: 1.8;
        font-size: 1.05rem;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .msg-content h1, .msg-content h2, .msg-content h3 {
        color: #ffffff;
        margin: 1.5rem 0 1rem 0;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .msg-content h1 { 
        font-size: 1.8rem; 
        background: linear-gradient(135deg, #00D4FF, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .msg-content h2 { 
        font-size: 1.5rem; 
        background: linear-gradient(135deg, #8B5CF6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .msg-content h3 { 
        font-size: 1.25rem; 
        background: linear-gradient(135deg, #10B981, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .msg-content ul, .msg-content ol {
        margin: 1.2rem 0;
        padding-left: 2rem;
    }
    
    .msg-content li { 
        margin: 0.8rem 0; 
        color: #e2e8f0;
        line-height: 1.7;
    }
    
    .msg-content strong {
        color: #ffffff;
        font-weight: 600;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.1));
        padding: 0.2em 0.4em;
        border-radius: 6px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
    }
    
    .msg-content em {
        color: #cbd5e1;
        font-style: italic;
        font-weight: 500;
    }
    
    .msg-content code {
        background: rgba(0, 0, 0, 0.6);
        color: #00D4FF;
        padding: 0.3rem 0.6rem;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        font-weight: 500;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.1);
    }
    
    .msg-content pre {
        background: rgba(0, 0, 0, 0.8);
        color: #f1f5f9;
        padding: 1.5rem;
        border-radius: 12px;
        overflow-x: auto;
        margin: 1.5rem 0;
        border: 1px solid rgba(139, 92, 246, 0.2);
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .msg-content a {
        color: #38bdf8;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        border-bottom: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    .msg-content a:hover {
        color: #0ea5e9;
        text-shadow: 0 0 15px rgba(14, 165, 233, 0.5);
        border-bottom-color: #0ea5e9;
    }
    
    .msg-content p {
        margin: 1rem 0;
        line-height: 1.8;
    }
    
    /* Welcome message with animation */
    .welcome {
        background: linear-gradient(135deg, 
            rgba(0, 212, 255, 0.1) 0%, 
            rgba(139, 92, 246, 0.1) 50%, 
            rgba(16, 185, 129, 0.1) 100%);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(30px);
    }
    
    .welcome::before {
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        background: linear-gradient(45deg, #00D4FF, #8B5CF6, #10B981, #00D4FF);
        background-size: 400% 400%;
        border-radius: 24px;
        z-index: -1;
        animation: borderFlow 6s linear infinite;
    }
    
    @keyframes borderFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .welcome h2 {
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }
    
    .welcome p {
        color: #e2e8f0;
        line-height: 1.7;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* No highlight chat input */
    .stChatInput > div {
        background: transparent !important;
    }
    
    .stChatInput > div > div {
        background: linear-gradient(135deg, 
            rgba(15, 23, 42, 0.9) 0%, 
            rgba(30, 41, 59, 0.8) 100%) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div > div:focus-within {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        outline: none !important;
    }
    
    .stChatInput textarea {
        background: transparent !important;
        color: #f1f5f9 !important;
        font-size: 1.05rem !important;
        border: none !important;
        padding: 1.2rem 1.5rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        resize: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stChatInput textarea:focus {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
        opacity: 0.8 !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        box-shadow: 0 4px 16px rgba(0, 212, 255, 0.3) !important;
        outline: none !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stChatInput button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4) !important;
        background: linear-gradient(135deg, #38bdf8 0%, #a78bfa 100%) !important;
    }
    
    .stChatInput button:focus {
        outline: none !important;
        box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4) !important;
    }
    
    /* Typing animation with better visibility */
    .typing {
        color: #a78bfa;
        font-style: italic;
        margin: 1rem 0;
        font-weight: 500;
        text-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
    }
    
    .dot {
        animation: typingPulse 1.6s infinite;
        font-size: 1.5rem;
        color: #8B5CF6;
    }
    
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingPulse {
        0%, 80%, 100% { opacity: 0.3; transform: scale(1); }
        40% { opacity: 1; transform: scale(1.2); }
    }
    
    /* Mobile improvements */
    @media (max-width: 768px) {
        .chat-container {
            padding: 1rem;
        }
        
        .title {
            font-size: 2.5rem;
        }
        
        .user-message, .assistant-message {
            margin-left: 0;
            margin-right: 0;
            padding: 1.5rem;
        }
        
        .msg-content {
            font-size: 1rem;
        }
    }
</style>

<!-- Enhanced quantum background -->
<div class="quantum-bg">
    <!-- Floating geometric shapes -->
    <div class="shape shape1"></div>
    <div class="shape shape2"></div>
    <div class="shape shape3"></div>
    <div class="shape shape4"></div>
    
    <!-- Quantum particles -->
    <div class="particle p1"></div>
    <div class="particle p2"></div>
    <div class="particle p3"></div>
    <div class="particle p4"></div>
    <div class="particle p5"></div>
    <div class="particle p6"></div>
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

def advanced_markdown(text):
    """Enhanced markdown conversion with better line handling"""
    # Handle multiple line breaks properly
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Normalize multiple line breaks
    
    # Headers
    text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold and italic
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Code blocks
    text = re.sub(r'```(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
    
    # Lists - improved handling
    text = re.sub(r'^[•\-\*] (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^(\d+)\. (.*$)', r'<li>\2</li>', text, flags=re.MULTILINE)
    
    # Wrap consecutive list items in ul tags
    text = re.sub(r'(<li>.*?</li>)(\s*<li>.*?</li>)*', 
                  lambda m: '<ul>' + m.group(0) + '</ul>', text, flags=re.DOTALL)
    
    # Convert line breaks to paragraphs and br tags
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            # Don't wrap headers, lists, or code blocks in p tags
            if not (paragraph.startswith('<h') or paragraph.startswith('<ul') or 
                   paragraph.startswith('<pre') or paragraph.startswith('<li')):
                # Convert single line breaks to <br> within paragraphs
                paragraph = paragraph.replace('\n', '<br>')
                paragraph = f'<p>{paragraph}</p>'
            formatted_paragraphs.append(paragraph)
    
    return '\n'.join(formatted_paragraphs)

def stream_response(response_text):
    """Enhanced streaming with better animation"""
    # Show enhanced typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="message assistant-message">
        <div class="msg-header enviro-header">
            🌎 Enviro
        </div>
        <div class="typing">
            Analyzing environmental data<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(2)  # Longer thinking time for realism
    
    # Stream response with variable speed
    words = response_text.split()
    streamed_text = ""
    placeholder = st.empty()
    
    for i, word in enumerate(words):
        streamed_text += word + " "
        current_html = advanced_markdown(streamed_text)
        
        # Add blinking cursor
        placeholder.markdown(f"""
        <div class="message assistant-message">
            <div class="msg-header enviro-header">
                🌎 Enviro
            </div>
            <div class="msg-content">
                {current_html}<span style="color: #8B5CF6; animation: blink 1s infinite; font-weight: bold;">|</span>
            </div>
        </div>
        <style>
        @keyframes blink {{ 0%, 50% {{ opacity: 1; }} 51%, 100% {{ opacity: 0; }} }}
        </style>
        """, unsafe_allow_html=True)
        
        # Variable typing speed for natural feel
        if word.endswith('.') or word.endswith('!') or word.endswith('?'):
            time.sleep(0.12)  # Longer pause after sentences
        elif word.endswith(',') or word.endswith(':'):
            time.sleep(0.08)  # Medium pause after punctuation
        elif word in ['and', 'or', 'but', 'the', 'a', 'an']:
            time.sleep(0.02)  # Faster for common words
        else:
            time.sleep(0.05)  # Normal typing speed
    
    # Final display without cursor
    final_html = advanced_markdown(streamed_text.strip())
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

    # Enhanced header section
    st.markdown("""
    <div class="header">
        <h1 class="title">🌎 Meet Enviro</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Welcome message with enhanced styling
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome">
            <h2>Welcome to EnviroCast AI</h2>
            <p>I'm Enviro, your quantum-enhanced environmental intelligence assistant. I specialize in air quality forecasting, pollution analysis, and environmental science. Ask me anything about environmental challenges, air quality prediction, or climate solutions!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display messages with enhanced markdown support
    for message in st.session_state.messages:
        content = advanced_markdown(message["content"])
        
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
    
    # Markdown toolbar - Add above chat input
    st.markdown("""
    <div class="chat-container">
        <div style="margin-bottom: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center;">
            <button onclick="insertMarkdown('**', '**')" style="
                background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 212, 255, 0.1));
                border: 1px solid rgba(0, 212, 255, 0.3);
                color: #38bdf8;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            " onmouseover="this.style.background='linear-gradient(135deg, rgba(0, 212, 255, 0.3), rgba(0, 212, 255, 0.2))'" 
               onmouseout="this.style.background='linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 212, 255, 0.1))'">
                <strong>B</strong> Bold
            </button>
            
            <button onclick="insertMarkdown('*', '*')" style="
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1));
                border: 1px solid rgba(139, 92, 246, 0.3);
                color: #a78bfa;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            " onmouseover="this.style.background='linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(139, 92, 246, 0.2))'" 
               onmouseout="this.style.background='linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(139, 92, 246, 0.1))'">
                <em>I</em> Italic
            </button>
            
            <button onclick="insertMarkdown('`', '`')" style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
                border: 1px solid rgba(16, 185, 129, 0.3);
                color: #34d399;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                font-family: 'JetBrains Mono', monospace;
            " onmouseover="this.style.background='linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(16, 185, 129, 0.2))'" 
               onmouseout="this.style.background='linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1))'">
                &lt;/&gt; Code
            </button>
            
            <button onclick="insertMarkdown('- ', '')" style="
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
                border: 1px solid rgba(245, 158, 11, 0.3);
                color: #fbbf24;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            " onmouseover="this.style.background='linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(245, 158, 11, 0.2))'" 
               onmouseout="this.style.background='linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1))'">
                • List
            </button>
        </div>
    </div>
    
    <script>
    function insertMarkdown(before, after) {
        const textarea = document.querySelector('.stChatInput textarea');
        if (textarea) {
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const selectedText = textarea.value.substring(start, end);
            const beforeText = textarea.value.substring(0, start);
            const afterText = textarea.value.substring(end);
            
            textarea.value = beforeText + before + selectedText + after + afterText;
            textarea.focus();
            
            // Set cursor position
            const newPos = start + before.length + selectedText.length + after.length;
            textarea.setSelectionRange(newPos, newPos);
            
            // Trigger input event to update Streamlit
            const event = new Event('input', { bubbles: true });
            textarea.dispatchEvent(event);
        }
    }
    </script>
    """, unsafe_allow_html=True)

    # Enhanced chat input
    prompt = st.chat_input("Ask about environmental science, air quality, pollution analysis, or climate solutions...")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        user_content = advanced_markdown(prompt)
        st.markdown(f"""
        <div class="chat-container">
            <div class="message user-message">
                <div class="msg-header user-header">👤 You</div>
                <div class="msg-content">{user_content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate and display assistant response
        try:
            response = st.session_state.chat_session.send_message(prompt)
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            full_response = stream_response(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
            st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="chat-container">
                <div class="message assistant-message" style="border-left-color: #ef4444; background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));">
                    <div class="msg-header" style="color: #f87171; text-shadow: 0 0 10px rgba(248, 113, 113, 0.3);">⚠️ Error</div>
                    <div class="msg-content" style="color: #fca5a5;">
                        <strong>Error:</strong> {str(e)}<br><br>
                        {"🔄 <em>API rate limit reached. Please wait a moment before trying again.</em>" if "rate_limit" in str(e).lower() else "🔄 <em>Please try again in a moment.</em>"}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
