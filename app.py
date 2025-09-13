import streamlit as st
import google.generativeai as genai
import time
import os
from textwrap import dedent

# ----------------------------
# Config & API initialization
# ----------------------------
# We configure the model here, but the actual API key will be provided at runtime.
genai.configure()

st.set_page_config(
    page_title="Meet Enviro",
    page_icon="🌐",
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
Name: Your name is Enviro. You are the Large Language Model/AI Chatbot for EnviroCast.

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
Another topic you can talk about is quantum data. Different quantum mechanics and topics and concepts. You can relate how quantum computing and algorithms are used in EnviroCast's processes.
Feel free to talk anything about EnviroCast.

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
    overflow: hidden !important; /* Prevents global scrolling */
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

/* Main app container - full height with proper flex layout */
.app-container {
    display: flex !important;
    flex-direction: column !important;
    height: 100vh !important;
    position: relative !important;
    z-index: 10 !important;
}

/* Header - fixed height, no scroll */
.header {
    flex: 0 0 auto !important; /* Don't grow or shrink */
    text-align: center;
    padding: 1rem 0; /* Refined padding */
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
    flex: 1 1 auto !important; /* Fills remaining space */
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important; /* Prevents this container from scrolling */
    position: relative !important;
    z-index: 15 !important;
}

/* Welcome section - only shown when no messages */
.welcome-section {
    flex: 0 0 auto !important; /* Doesn't scroll */
    padding: 1rem 2rem 2rem 2rem; /* Reduced top padding */
}

.welcome {
    text-align: center;
    padding: 1.5rem; /* Refined padding */
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.05), rgba(139, 92, 246, 0.05));
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    max-width: 900px;
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
    flex: 1 1 auto !important; /* Fills remaining space */
    overflow-y: auto !important; /* Only this section scrolls */
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
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 1.5rem;
}

.user-message {
    flex-direction: row-reverse;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    border-color: rgba(255, 255, 255, 0.3);
}

.assistant-message {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.05));
    border-color: rgba(0, 212, 255, 0.3);
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
    background: linear-gradient(135deg, #ffffff, #e0e0e0);
    color: #000000;
}

.assistant-avatar {
    background: linear-gradient(135deg, #4CAF50, #2196F3);
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
    flex: 0 0 auto !important; /* Don't grow or shrink */
    padding: 1rem 2rem 2rem 2rem;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(20px);
    position: relative;
    z-index: 25;
}

.stChatInput > div {
    max-width: 900px !important; /* Make wider */
    margin: 0 auto !important;
}

.stChatInput > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important; /* More visible border */
    border-radius: 12px !important;
}

.stChatInput textarea {
    background: transparent !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 16px !important;
    padding: 0.5rem 1rem !important; /* Added padding */
}

.stChatInput button {
    background: linear-gradient(135deg, #00D4FF, #8B5CF6) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

/* Typing effect cursor */
.typing-cursor {
    animation: blink 1s step-end infinite;
    font-weight: bold;
    color: #ffffff;
}

@keyframes blink {
    from, to { color: transparent; }
    50% { color: white; }
}

/* --- Mobile Styles --- */
@media (max-width: 768px) {
    .title {
        font-size: 2.5rem;
    }
    .welcome h2 {
        font-size: 1.5rem;
    }
    .welcome p {
        font-size: 1rem;
    }
    .chat-messages, .chat-input-section {
        padding: 0 1rem;
    }
    .message {
        padding: 1rem;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

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

def stream_response(response):
    # 1. Display "Enviro is analyzing..." message
    analyzing_placeholder = st.empty()
    analyzing_message_html = """
        <div class="message assistant-message">
            <div class="avatar assistant-avatar">🌐</div>
            <div class="message-content">
                <span style="color: #00D4FF; font-weight: bold;">Enviro is analyzing...</span>
            </div>
        </div>
    """
    analyzing_placeholder.markdown(analyzing_message_html, unsafe_allow_html=True)
    time.sleep(2) # Show message for a couple of seconds

    # 2. Clear the analyzing message and prepare for streaming
    analyzing_placeholder.empty()
    full_response = ""
    message_placeholder = st.empty()
    
    # 3. Stream the response
    for chunk in response:
        full_response += chunk.text
        # We use st.markdown to render markdown correctly.
        message_placeholder.markdown(f"""
            <div class="message assistant-message">
                <div class="avatar assistant-avatar">🌐</div>
                <div class="message-content">{full_response} <span class="typing-cursor">|</span></div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02) # Slower typing effect for a more natural feel

    # 4. Final render of the message without the cursor
    message_placeholder.markdown(f"""
        <div class="message assistant-message">
            <div class="avatar assistant-avatar">🌐</div>
            <div class="message-content">{full_response}</div>
        </div>
    """, unsafe_allow_html=True)
    return full_response

# -------------
# Main App
# -------------
def main():
    initialize_session_state()
    
    # Header section
    st.markdown("""
    <div class="header">
        <h1 class="title">🌐 Meet Enviro</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Welcome section (only show when no messages)
    if not st.session_state.messages:
        st.markdown('<div class="welcome-section">', unsafe_allow_html=True)
        st.markdown("""
        <div class="welcome">
            <h2>Welcome to EnviroCast's AI Chatbot</h2>
            <p>I'm Enviro, your environmental intelligence assistant. Ask me about air quality, pollution, climate solutions, and environmental science or EnviroCast and quantum data.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat messages area
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            display_message("user", message["content"], "👤")
        else:
            display_message("assistant", message["content"], "🌐")
    
    st.markdown('</div>', unsafe_allow_html=True) # End chat-messages
    
    st.markdown('</div>', unsafe_allow_html=True) # End main-content
    
    # Chat input section
    st.markdown('<div class="chat-input-section">', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me about environmental science, climate solutions or anything EnviroCast..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Rerun to display the user message and start the generation process
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) # End chat-input-section
    st.markdown('</div>', unsafe_allow_html=True) # End app-container

    # After a prompt has been submitted and the page is rerunning,
    # we check the last message to see if it's from the user and needs a response.
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        prompt = st.session_state.messages[-1]["content"]
        
        try:
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            full_response = stream_response(response)
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_message = f"⚠️ **Error:** {str(e)}<br><br>Please try again in a moment."
            display_message("assistant", error_message, "⚠️")

        # Rerun once more to show the complete response
        st.rerun()

if __name__ == "__main__":
    main()
