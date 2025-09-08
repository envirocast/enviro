import streamlit as st
import google.generativeai as genai
import time
import os

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

# EnviroCast Dark Theme Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background matching EnviroCast website */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #2d1b69 100%);
        padding: 0;
        margin: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #2d1b69 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        letter-spacing: -0.02em;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Message styling */
    .user-message {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-left: 4px solid #00D4FF;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #e2e8f0;
    }
    
    .assistant-message {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-left: 4px solid #8B5CF6;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #e2e8f0;
    }
    
    .message-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .user-header {
        color: #00D4FF;
    }
    
    .enviro-header {
        color: #8B5CF6;
    }
    
    .message-content {
        line-height: 1.6;
        color: #cbd5e1;
    }
    
    .message-content h1, .message-content h2, .message-content h3 {
        color: #f1f5f9;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .message-content ul, .message-content ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .message-content li {
        margin: 0.5rem 0;
    }
    
    .message-content strong {
        color: #f1f5f9;
    }
    
    .message-content a {
        color: #00D4FF;
        text-decoration: none;
    }
    
    .message-content a:hover {
        color: #38bdf8;
        text-decoration: underline;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > textarea {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    
    .stChatInput > div > div > textarea:focus {
        border-color: #00D4FF !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
        outline: none !important;
    }
    
    .stChatInput > div > div > textarea::placeholder {
        color: #64748b !important;
    }
    
    /* Send button */
    .stChatInput button {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Quantum particle animation */
    .quantum-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        pointer-events: none;
    }
    
    .quantum-particle {
        position: absolute;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.3) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    /* Scrollbar styling */
    .main::-webkit-scrollbar {
        width: 8px;
    }
    
    .main::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    .main::-webkit-scrollbar-thumb {
        background: rgba(0, 212, 255, 0.3);
        border-radius: 4px;
    }
    
    .main::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 212, 255, 0.5);
    }
    
    /* Welcome message special styling */
    .welcome-message {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .welcome-message h2 {
        background: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .welcome-message p {
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.6;
    }
</style>

<!-- Quantum particle background -->
<div class="quantum-bg">
    <div class="quantum-particle" style="left: 10%; width: 4px; height: 4px; animation-delay: 0s; animation-duration: 25s;"></div>
    <div class="quantum-particle" style="left: 20%; width: 6px; height: 6px; animation-delay: 5s; animation-duration: 20s;"></div>
    <div class="quantum-particle" style="left: 30%; width: 3px; height: 3px; animation-delay: 10s; animation-duration: 30s;"></div>
    <div class="quantum-particle" style="left: 40%; width: 5px; height: 5px; animation-delay: 15s; animation-duration: 22s;"></div>
    <div class="quantum-particle" style="left: 50%; width: 4px; height: 4px; animation-delay: 20s; animation-duration: 28s;"></div>
    <div class="quantum-particle" style="left: 60%; width: 7px; height: 7px; animation-delay: 25s; animation-duration: 18s;"></div>
    <div class="quantum-particle" style="left: 70%; width: 3px; height: 3px; animation-delay: 30s; animation-duration: 26s;"></div>
    <div class="quantum-particle" style="left: 80%; width: 5px; height: 5px; animation-delay: 35s; animation-duration: 24s;"></div>
    <div class="quantum-particle" style="left: 90%; width: 4px; height: 4px; animation-delay: 40s; animation-duration: 20s;"></div>
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

def stream_response(response_text):
    """Stream response with typing effect"""
    words = response_text.split()
    streamed_text = ""
    placeholder = st.empty()
    
    for i, word in enumerate(words):
        streamed_text += word + " "
        # Show cursor while typing
        display_text = streamed_text + "▌"
        placeholder.markdown(f"""
        <div class="assistant-message">
            <div class="message-header enviro-header">
                🌎 Enviro
            </div>
            <div class="message-content">
                {display_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.03)  # Adjust typing speed
    
    # Final display without cursor
    placeholder.markdown(f"""
    <div class="assistant-message">
        <div class="message-header enviro-header">
            🌎 Enviro
        </div>
        <div class="message-content">
            {streamed_text.strip()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return streamed_text.strip()

def main():
    initialize_session_state()

    # Title with EnviroCast styling
    st.markdown("""
    <div class="chat-container">
        <h1 class="main-title">🌎 Meet Enviro</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message if it's the first load
    if not st.session_state.messages:
        st.markdown("""
        <div class="chat-container">
            <div class="welcome-message">
                <h2>Welcome to EnviroCast AI</h2>
                <p>I'm Enviro, your quantum-enhanced environmental intelligence assistant. I specialize in air quality forecasting, pollution analysis, and environmental science. Ask me anything about environmental challenges, air quality prediction, or climate solutions!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="message-header user-header">
                    You
                </div>
                <div class="message-content">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="message-header enviro-header">
                    🌎 Enviro
                </div>
                <div class="message-content">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    prompt = st.chat_input("What would you like to learn about environmental science?")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        st.markdown(f"""
        <div class="chat-container">
            <div class="user-message">
                <div class="message-header user-header">
                    You
                </div>
                <div class="message-content">
                    {prompt}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate and display assistant response
        try:
            with st.spinner('🧠 Enviro is thinking...'):
                response = st.session_state.chat_session.send_message(prompt)
            
            # Stream the response with EnviroCast styling
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
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
            st.error(f"⚠️ An error occurred: {str(e)}")
            if "rate_limit" in str(e).lower():
                st.warning("🔄 The API rate limit has been reached. Please wait a moment before trying again.")
            else:
                st.warning("🔄 Please try again in a moment.")

if __name__ == "__main__":
    main()
