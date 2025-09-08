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
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stTitle {
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    
    .chat-message.user {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2E8B57;
    }
    
    .chat-message.assistant {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    
    .enviro-name {
        font-weight: bold;
        color: #2E8B57;
        font-size: 1.1em;
        margin-bottom: 0.5rem;
    }
    
    .user-name {
        font-weight: bold;
        color: #333;
        font-size: 1.1em;
        margin-bottom: 0.5rem;
    }
</style>
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
        initial_message = """Welcome to the EnviroCast Informational LLM Platform. What would you like to learn about?"""
        st.session_state.messages = [
            {"role": "assistant", "content": initial_message}
        ]

def stream_response(response_text):
    """Stream response with typing effect"""
    words = response_text.split()
    streamed_text = ""
    placeholder = st.empty()
    
    for word in words:
        streamed_text += word + " "
        placeholder.markdown(streamed_text + "▌")
        time.sleep(0.05)
    
    placeholder.markdown(streamed_text)
    return streamed_text.strip()

def main():
    initialize_session_state()

    # Title
    st.title("🌎 Meet Enviro")
    st.markdown("---")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-message user">
                    <div class="user-name">You:</div>
                    {message["content"]}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-message assistant">
                    <div class="enviro-name">🌎 Enviro:</div>
                    {message["content"]}
                </div>
                """, 
                unsafe_allow_html=True
            )

    # Chat input
    prompt = st.chat_input("What would you like to learn about?")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        st.markdown(
            f"""
            <div class="chat-message user">
                <div class="user-name">You:</div>
                {prompt}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Generate and display assistant response
        try:
            response = st.session_state.chat_session.send_message(prompt)
            
            # Create container for Enviro's response
            st.markdown(
                """
                <div class="chat-message assistant">
                    <div class="enviro-name">🌎 Enviro:</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Stream the response
            full_response = stream_response(response.text)
            
            # Add to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
            # Rerun to show the complete conversation
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if "rate_limit" in str(e).lower():
                st.warning("The API rate limit has been reached. Please wait a moment before trying again.")

if __name__ == "__main__":
    main()
