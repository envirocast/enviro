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

# Ultra Modern EnviroCast Interface with Animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Reset and Base Styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App Background with Animated Gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f0f23, #1a1a3a, #2d1b69, #1e1b4b, #0f172a);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden !important;
    }
    
    /* Quantum Background Particles */
    .quantum-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
    }
    
    .quantum-particle {
        position: absolute;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.4) 0%, rgba(139, 92, 246, 0.2) 50%, transparent 70%);
        border-radius: 50%;
        opacity: 0.8;
    }
    
    .particle-1 {
        width: 3px;
        height: 3px;
        top: 20%;
        left: 10%;
        animation: float1 20s infinite linear;
    }
    
    .particle-2 {
        width: 5px;
        height: 5px;
        top: 60%;
        left: 80%;
        animation: float2 25s infinite linear;
    }
    
    .particle-3 {
        width: 2px;
        height: 2px;
        top: 80%;
        left: 20%;
        animation: float3 30s infinite linear;
    }
    
    .particle-4 {
        width: 4px;
        height: 4px;
        top: 40%;
        left: 70%;
        animation: float4 18s infinite linear;
    }
    
    .particle-5 {
        width: 6px;
        height: 6px;
        top: 10%;
        left: 50%;
        animation: float5 22s infinite linear;
    }
    
    .particle-6 {
        width: 3px;
        height: 3px;
        top: 70%;
        left: 90%;
        animation: float6 28s infinite linear;
    }
    
    @keyframes float1 {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translate(-100px, -200px) rotate(180deg); }
        90% { opacity: 1; }
        100% { transform: translate(-200px, -400px) rotate(360deg); opacity: 0; }
    }
    
    @keyframes float2 {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translate(150px, -300px) rotate(-180deg); }
        90% { opacity: 1; }
        100% { transform: translate(300px, -600px) rotate(-360deg); opacity: 0; }
    }
    
    @keyframes float3 {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translate(-50px, -400px) rotate(270deg); }
        90% { opacity: 1; }
        100% { transform: translate(-100px, -800px) rotate(540deg); opacity: 0; }
    }
    
    @keyframes float4 {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translate(200px, -250px) rotate(-90deg); }
        90% { opacity: 1; }
        100% { transform: translate(400px, -500px) rotate(-180deg); opacity: 0; }
    }
    
    @keyframes float5 {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translate(-300px, -350px) rotate(450deg); }
        90% { opacity: 1; }
        100% { transform: translate(-600px, -700px) rotate(900deg); opacity: 0; }
    }
    
    @keyframes float6 {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        50% { transform: translate(100px, -450px) rotate(-270deg); }
        90% { opacity: 1; }
        100% { transform: translate(200px, -900px) rotate(-540deg); opacity: 0; }
    }
    
    /* Main Container with Glass Effect */
    .main-container {
        position: relative;
        z-index: 10;
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
        backdrop-filter: blur(20px);
        background: rgba(15, 23, 42, 0.1);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        min-height: 90vh;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.3),
            0 10px 10px -5px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    /* Animated Title */
    .enviro-title {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -0.05em;
        animation: shimmer 3s ease-in-out infinite;
        position: relative;
    }
    
    .enviro-title::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
        background-size: 200% 200%;
        animation: shimmer 3s ease-in-out infinite;
        opacity: 0.1;
        border-radius: 12px;
        filter: blur(20px);
        z-index: -1;
    }
    
    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Message Containers with Advanced Styling */
    .message-container {
        margin: 2rem 0;
        position: relative;
        animation: messageSlideIn 0.6s ease-out;
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1.5rem;
    }
    
    .assistant-message-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1.5rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 24px 24px 8px 24px;
        padding: 1.5rem 2rem;
        max-width: 70%;
        position: relative;
        box-shadow: 
            0 8px 32px rgba(0, 212, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .user-message:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(0, 212, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 24px 24px 24px 8px;
        padding: 1.5rem 2rem;
        max-width: 80%;
        position: relative;
        box-shadow: 
            0 8px 32px rgba(139, 92, 246, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .assistant-message:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 12px 40px rgba(139, 92, 246, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Message Headers with Icons */
    .message-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .user-header {
        color: #00D4FF;
    }
    
    .enviro-header {
        color: #8B5CF6;
    }
    
    .message-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        animation: pulse 2s infinite;
    }
    
    .user-icon {
        background: linear-gradient(135deg, #00D4FF, #38bdf8);
    }
    
    .enviro-icon {
        background: linear-gradient(135deg, #8B5CF6, #a855f7);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Enhanced Message Content Styling */
    .message-content {
        color: #e2e8f0;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    .message-content h1 {
        color: #f1f5f9;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        background: linear-gradient(135deg, #00D4FF, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .message-content h2 {
        color: #f1f5f9;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.25rem 0 0.75rem 0;
        background: linear-gradient(135deg, #8B5CF6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .message-content h3 {
        color: #f1f5f9;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        background: linear-gradient(135deg, #10B981, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .message-content ul, .message-content ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .message-content li {
        margin: 0.5rem 0;
        position: relative;
    }
    
    .message-content ul li::marker {
        color: #00D4FF;
    }
    
    .message-content ol li::marker {
        color: #8B5CF6;
        font-weight: 600;
    }
    
    .message-content strong {
        color: #f1f5f9;
        font-weight: 600;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.1));
        padding: 0.1em 0.3em;
        border-radius: 4px;
    }
    
    .message-content em {
        color: #cbd5e1;
        font-style: italic;
        background: rgba(139, 92, 246, 0.1);
        padding: 0.1em 0.3em;
        border-radius: 4px;
    }
    
    .message-content code {
        background: rgba(15, 23, 42, 0.8);
        color: #00D4FF;
        padding: 0.2em 0.5em;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9em;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    .message-content pre {
        background: rgba(15, 23, 42, 0.9);
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 12px;
        overflow-x: auto;
        margin: 1rem 0;
        border: 1px solid rgba(139, 92, 246, 0.2);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .message-content blockquote {
        border-left: 4px solid #8B5CF6;
        margin: 1rem 0;
        padding-left: 1rem;
        background: rgba(139, 92, 246, 0.05);
        border-radius: 0 8px 8px 0;
        font-style: italic;
    }
    
    .message-content a {
        color: #00D4FF;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .message-content a:hover {
        color: #38bdf8;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.4);
    }
    
    .message-content a::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -2px;
        left: 0;
        background: linear-gradient(135deg, #00D4FF, #8B5CF6);
        transition: width 0.3s ease;
    }
    
    .message-content a:hover::after {
        width: 100%;
    }
    
    /* Welcome Message Special Styling */
    .welcome-message {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(16, 185, 129, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 24px;
        padding: 3rem;
        margin: 3rem 0;
        text-align: center;
        position: relative;
        animation: welcomeGlow 4s ease-in-out infinite;
        overflow: hidden;
    }
    
    .welcome-message::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #00D4FF, #8B5CF6, #10B981, #00D4FF);
        background-size: 400% 400%;
        border-radius: 24px;
        z-index: -1;
        animation: borderGlow 3s linear infinite;
    }
    
    @keyframes welcomeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.3); }
    }
    
    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .welcome-title {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    /* Chat Input Styling */
    .stChatInput > div {
        background: transparent !important;
        border: none !important;
    }
    
    .stChatInput > div > div {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 20px !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div > div:focus-within {
        border-color: #00D4FF !important;
        box-shadow: 
            0 0 0 4px rgba(0, 212, 255, 0.1),
            0 12px 40px rgba(0, 212, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px) !important;
    }
    
    .stChatInput textarea {
        background: transparent !important;
        border: none !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.5 !important;
        resize: none !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #64748b !important;
        font-weight: 400 !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3) !important;
    }
    
    .stChatInput button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 20px rgba(0, 212, 255, 0.4) !important;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%) !important;
    }
    
    .stChatInput button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Typing Indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #8B5CF6;
        font-style: italic;
        margin: 1rem 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 0.25rem;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        background: #8B5CF6;
        border-radius: 50%;
        animation: typingBounce 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    .typing-dot:nth-child(3) { animation-delay: 0s; }
    
    @keyframes typingBounce {
        0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    /* Scrollbar Styling */
    .main-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .main-container::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.3);
        border-radius: 4px;
    }
    
    .main-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.5), rgba(139, 92, 246, 0.5));
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .main-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.7), rgba(139, 92, 246, 0.7));
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main-container {
            margin: 1rem;
            padding: 1rem;
            border-radius: 16px;
        }
        
        .enviro-title {
            font-size: 2.5rem;
        }
        
        .user-message, .assistant-message {
            max-width: 85%;
            padding: 1rem 1.5rem;
        }
        
        .welcome-message {
            padding: 2rem;
            margin: 2rem 0;
        }
    }
</style>

<!-- Quantum Background Particles -->
<div class="quantum-bg">
    <div class="quantum-particle particle-1"></div>
    <div class="quantum-particle particle-2"></div>
    <div class="quantum-particle particle-3"></div>
    <div class="quantum-particle particle-4"></div>
    <div class="quantum-particle particle-5"></div>
    <div class="quantum-particle particle-6"></div>
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

def markdown_to_html(text):
    """Convert markdown to HTML with proper styling"""
    # Convert headers
    text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Convert bold and italic
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Convert inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Convert code blocks
    text = re.sub(r'```(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)
    
    # Convert links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Convert line breaks
    text = text.replace('\n\n', '</p><p>')
    text = text.replace('\n', '<br>')
    
    # Wrap in paragraph tags if not already wrapped
    if not text.startswith('<'):
        text = f'<p>{text}</p>'
    
    # Convert bullet points
    text = re.sub(r'^- (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^• (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^(\d+)\. (.*$)', r'<li>\2</li>', text, flags=re.MULTILINE)
    
    # Wrap consecutive list items in ul tags
    text = re.sub(r'(<li>.*?</li>)(?:\s*<li>.*?</li>)*', r'<ul>\g<0></ul>', text, flags=re.DOTALL)
    
    return text

def stream_response(response_text):
    """Stream response with enhanced typing effect and proper markdown rendering"""
    
    # Show typing indicator first
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="assistant-message-container">
        <div class="assistant-message">
            <div class="message-header">
                <div class="message-icon enviro-icon">🌎</div>
                <span class="enviro-header">Enviro</span>
            </div>
            <div class="typing-indicator">
                <span>Enviro is thinking</span>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)  # Show typing indicator for 1 second
    
    # Convert markdown to HTML
    formatted_text = markdown_to_html(response_text)
    
    # Stream the response
    words = response_text.split()
    streamed_text = ""
    placeholder = st.empty()
    
    for i, word in enumerate(words):
        streamed_text += word + " "
        # Convert current streamed text to HTML
        current_html = markdown_to_html(streamed_text)
        
        # Show cursor while typing
        display_text = current_html + "<span style='color: #8B5CF6; animation: blink 1s infinite;'>▌</span>"
        
        placeholder.markdown(f"""
        <div class="assistant-message-container">
            <div class="assistant-message">
                <div class="message-header">
                    <div class="message-icon enviro-icon">🌎</div>
                    <span class="enviro-header">Enviro</span>
                </div>
                <div class="message-content">
                    {display_text}
                </div>
            </div>
        </div>
        <style>
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Variable typing speed for more natural feel
        if word.endswith('.') or word.endswith('!') or word.endswith('?'):
            time.sleep(0.08)  # Longer pause after sentences
        elif word.endswith(','):
            time.sleep(0.05)  # Medium pause after commas
        else:
            time.sleep(0.03)  # Normal typing speed
    
    # Final display without cursor
    placeholder.markdown(f"""
    <div class="assistant-message-container">
        <div class="assistant-message">
            <div class="message-header">
                <div class="message-icon enviro-icon">🌎</div>
                <span class="enviro-header">Enviro</span>
            </div>
            <div class="message-content">
                {formatted_text}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return streamed_text.strip()

def main():
    initialize_session_state()

    # Main container with glass effect
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Animated title
    st.markdown('<h1 class="enviro-title">🌎 Meet Enviro</h1>', unsafe_allow_html=True)
    
    # Welcome message if it's the first load
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-message">
            <h2 class="welcome-title">Welcome to EnviroCast AI</h2>
            <p class="welcome-subtitle">
                I'm Enviro, your quantum-enhanced environmental intelligence assistant. 
                I specialize in air quality forecasting, pollution analysis, and environmental science. 
                Ask me anything about environmental challenges, air quality prediction, or climate solutions!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages with enhanced styling
    for message in st.session_state.messages:
        if message["role"] == "user":
            # Convert user message markdown to HTML too
            user_content = markdown_to_html(message["content"])
            st.markdown(f"""
            <div class="user-message-container">
                <div class="user-message">
                    <div class="message-header">
                        <div class="message-icon user-icon">👤</div>
                        <span class="user-header">You</span>
                    </div>
                    <div class="message-content">
                        {user_content}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Convert assistant message markdown to HTML
            assistant_content = markdown_to_html(message["content"])
            st.markdown(f"""
            <div class="assistant-message-container">
                <div class="assistant-message">
                    <div class="message-header">
                        <div class="message-icon enviro-icon">🌎</div>
                        <span class="enviro-header">Enviro</span>
                    </div>
                    <div class="message-content">
                        {assistant_content}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main container

    # Enhanced chat input
    prompt = st.chat_input("Ask me about environmental science, air quality, or climate solutions...")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately with animation
        user_content = markdown_to_html(prompt)
        st.markdown(f"""
        <div class="main-container">
            <div class="message-container">
                <div class="user-message-container">
                    <div class="user-message">
                        <div class="message-header">
                            <div class="message-icon user-icon">👤</div>
                            <span class="user-header">You</span>
                        </div>
                        <div class="message-content">
                            {user_content}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate and display assistant response with enhanced streaming
        try:
            response = st.session_state.chat_session.send_message(prompt)
            
            # Create container for streamed response
            st.markdown('<div class="main-container">', unsafe_allow_html=True)
            full_response = stream_response(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
            # Rerun to show the complete conversation
            st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="main-container">
                <div class="assistant-message-container">
                    <div class="assistant-message" style="border-color: #ef4444;">
                        <div class="message-header">
                            <div class="message-icon" style="background: linear-gradient(135deg, #ef4444, #dc2626);">⚠️</div>
                            <span style="color: #ef4444;">Error</span>
                        </div>
                        <div class="message-content">
                            <p style="color: #fca5a5;">An error occurred: {str(e)}</p>
                            {"<p style='color: #fed7d7;'>🔄 The API rate limit has been reached. Please wait a moment before trying again.</p>" if "rate_limit" in str(e).lower() else "<p style='color: #fed7d7;'>🔄 Please try again in a moment.</p>"}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
