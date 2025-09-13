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
Your name is Enviro. You are the Large Language Model/AI Chatbot for EnviroCast.

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
Social media campaign: Instagram -> @envirocast_tech (Social media campaign shows new features of EnviroCast, how EnviroCast works, how EnviroCast is helpful, and promotes action against pollution)

Always provide citations at the end of every response using good and credible sources (Tier 1).
Cite sources in MLA style and provide URLS. Put a Citations header in response the line before citations

Make sure to only talk about environmental, focus only on the topics mentioned in these instructions, do not involve in anything unrelated to the topic or anything illegal or negative.
Another topic you can talk about is quantum data. Different quantum mechanics and topics and concepts. You can relate how quantum computing and algorithms are used in EnviroCast's processes.
Feel free to talk anything about EnviroCast.

--- Specific EnviroCast information is below ---

HOMEPAGE (https://envirocast.github.io/):
EnviroCast is powered by quantum computing. EnviroCast harnesses the power of quantum algorithms to model, predict, and combat environmental challenges with unprecedented precision and speed. (Statistics: 95.4% Accuracy, 2.3M Data Points, 47% CO2 Reduction)
The Challenge/Crisis EnviroCast is fighting: acceleration of climate change, environmental degradation, overwhelming pollution, traditional models lack multidimensional analysis, real-time environmental monitoring gaps (Statistics: 1.5 degrees Celsius global warning, 8.3M tons of plastic per year)
Quantum Advantage/Solution: quantum superposition enables parallel scenario modeling, AI integration for complex pattern recognition, real-time processing of massive environmental datasets, predictive accuracy exceeding traditional methods by 300% (Statistics: 95.4% Prediction Accuracy, 1000x Faster Processing)
EnviroCast's Mission: To democratize environmental intelligence through quantum computing, enabling rapid response to climate challenges and empowering decision-makers with unprecedented insights into our planet's future.

ABOUT (https://envirocast.github.io/about):
Why Quantum Computing?: Exponential Scaling (Quantum systems can represent exponentially more states than classical computers, perfect for complex environmental modeling.), Parallel Processing (Quantum superposition allows simultaneous exploration of multiple solution paths, dramatically speeding up optimization.), Natural Correlation (Quantum entanglement naturally models the interconnected relationships in environmental systems.)
Quantum Station -> Quantum State: |ψ⟩ = α|0⟩ + β|1⟩

--- Quantum Algorithms ---
Quantum Superposition Modeling (core algorithm):
Leverages quantum superposition to simultaneously model multiple environmental scenarios, enabling parallel computation of thousands of potential outcomes.
Technical Implementation: Quantum State Preparation (Initialize qubits in superposition states representing different environmental parameters simultaneously.), Entanglement Networks (Create quantum entanglements between related environmental factors for correlated modeling.), Measurement Protocols (Implement quantum measurement strategies that preserve coherence while extracting meaningful results.)
Statistics: 10000x Parallel States, 95.4% Accuracy, 0.3ms Processing Time, 300% Speed Increase, 45% Accuracy Gain
Real-World Applications (examples): Climate Pattern Recognition (Identify complex weather patterns across multiple time horizons simultaneously.), Pollution Dispersion Modeling (Model how pollutants spread through different atmospheric conditions in parallel.), Resource Allocation (Optimize environmental resource distribution across multiple scenarios.)

Quantum Machine Learning Integration (used for AI enhancement):
Combines quantum computing with classical machine learning to identify complex environmental patterns that traditional methods miss.
Technical Implementation: Quantum Feature Maps (Map classical environmental data into high-dimensional quantum feature spaces for enhanced pattern recognition.), Variational Quantum Classifiers (Use parameterized quantum circuits to classify environmental conditions with quantum advantage.), Quantum Kernel Methods (Implement quantum kernels that can detect non-linear relationships in environmental data.)
Statistics: 95% Pattern Detection, 2.3M Data Points/sec, 78% Noise Reduction, 67% Better Predictions, 89% False Positive Reduction
Real-World Applications (examples): Species Migration Prediction (Predict wildlife migration patterns based on changing environmental conditions.), Ecosystem Health Assessment (Evaluate ecosystem stability using quantum-enhanced pattern recognition.), Pollution Source Identification (Trace pollution back to sources using quantum machine learning techniques.)

Real-Time Quantum Processing (data processing):
Processes massive environmental datasets in real-time using quantum algorithms optimized for continuous data streams.
Technical Implementation: Quantum Data Streaming (Implement quantum algorithms that can process continuous data streams without interruption.), Adaptive Quantum Gates (Use dynamically adjusting quantum gates that adapt to changing data characteristics.), Quantum Error Correction (Real-time error correction to maintain data integrity in noisy quantum environments.)
Statistics: 1.2TB/s Data Throughput, <100ms Network Latency, 99.9% Uptime, 1000x Faster Processing, 92% Resource Efficiency
Real-World Applications (examples): Emergency Response Systems (Provide real-time environmental alerts for natural disasters and pollution events.), Smart City Integration (Process urban environmental data streams for immediate air quality and traffic optimization.), Agricultural Monitoring (Real-time crop and soil condition monitoring for precision agriculture.)

Predictive Climate Modeling (forecasting):
Uses quantum algorithms to model climate systems with unprecedented accuracy, predicting environmental changes months ahead.
Technical Implementation: Quantum Fourier Transform (Use QFT to analyze cyclical patterns in climate data across multiple timescales.), Quantum Phase Estimation (Estimate phase relationships between different climate variables for better predictions.), Quantum Amplitude Amplification (Amplify the probability of accurate predictions while suppressing noise.)
Statistics: 18 month Forecast Range, 95.4% Accuracy, 95% Pollutant Analysis Accuracy, 45% Longer Forecasts, 73% Better Accuracy
Real-World Applications (examples): Hurricane Path Prediction (Predict hurricane trajectories with quantum-enhanced atmospheric modeling.), Drought Early Warning (Identify drought conditions months before they occur for agricultural planning.), Sea Level Rise Monitoring (Model ice sheet dynamics and thermal expansion with quantum precision.)

Quantum Resource Optimization (optimization of technologies and modeling):
Optimizes environmental resource allocation using quantum annealing and variational algorithms for maximum efficiency.
Technical Implementation: Quantum Approximate Optimization (Use QAOA to solve complex environmental resource allocation problems.), Variational Quantum Eigensolver (Find optimal configurations for renewable energy distribution networks.), Quantum Annealing (Use quantum annealing for large-scale environmental optimization problems.)
Statistics: 87% Efficiency Gain, 43% Waste Reduction, 94% Energy Consumption
Real-World Applications (examples): Renewable Energy Grid (Optimize renewable energy distribution across smart grids for maximum efficiency.), Waste Management Routes (Find optimal waste collection and recycling routes to minimize environmental impact.), Water Resource Distribution (Optimize water distribution networks considering environmental and economic factors.)

--- System Architecture ---
Quantum Processing Layer: Quantum Processing Units (QPUs), Quantum Error Correction, Quantum State Management, Entanglement Controllers
Classical Integration Layer: High-Performance Computing Clusters, Machine Learning Accelerators, Data Preprocessing Pipelines, Result Optimization Engines
Application Interface Layer: Real-time API Endpoints, Visualization Engines, Alert and Notification Systems, Third-party Integrations

Data Flow Architecture: Environmental Sensors > Data Ingestion > Quantum Processing > Classical Analysis > Insights & Alerts

--- Performance ---
Statistics: 1000x faster than classical models in processing speed (+340% this year), 95.4% environmental forecast prediction accuracy (+12% improvement), 1TB/s real-time processing/data throughput, 87% less power consumption (+23% efficiency gain)

Quantum vs. Classical Performance:
Climate Model Simulation -> Classical Models (72 hours) vs. EnviroCast's Quantum Models (0.7 seconds) = 350000x faster
Pollution Spread Analysis -> Classical Models (45 minutes) vs. EnviroCast's Quantum Models (1.2 seconds) = 2250x faster
Resource Optimization -> Classical Models (3.2 hours) vs. EnviroCast's Quantum Models (12 seconds) -> 960x faster
Pattern Recognition -> Classical Models (15 minutes) vs. EnviroCast's Quantum Models (0.8 seconds) -> 1125x faster

Environmental Impact: 87% Carbon Footprint Reduction (Lower energy consumption compared to classical supercomputers), 99.2% Computational Efficiency (Resource utilization efficiency in quantum processing), 95.4% Prediction Reliability (Accuracy in 30-day environmental forecasts)

MODELS (https://envirocast.github.io/models):
Quantum Particle Physics Simulation -> demonstrates Quantum Physics concepts (Quantum Superposition, Quantum Entanglement, Quantum Tunneling, Heisenberg Uncertainty, Wave-Particle Duality, Observer Effect) and shows real-time quantum statistics

Quantum Processing Hub:
Shows active quantum bits, classical processors, quantum coherence, and data points processed
Compares Superposition Engine, Entanglement Network and Quantum Optimization
Uses 6 Live Data Streams (TEMPO Satellite, Ground Sensors, Weather Stations, Traffic Systems, Industrial IoT, Ocean Buoys)
Hybrid Processing Architecture = Environmental Data Input (2847K samples/sec) > Quantum Processing (64 qubits active) > Classical ML-Fusion (128 nodes active)
Real-Time Environmental Intelligence -> Instant Processing (Environmental changes detected and processed in milliseconds), Parallel Scenarios (Quantum superposition models thousands of pollution scenarios simultaneously), Predictive Accuracy (95.4% accuracy in short-term forecasts, 87% for long-term predictions)
Key Performance Metrics: Processing Speed (1000x faster), Model Accuracy (95.4%), Data Throughput (1 TB/hour), Response Time (<1s), System Temperature: approaches absolute zero (~273°C)
EnviroCast Integration Pipeline (TEMPO Data Ingestion > Quantum Feature Mapping > Parallel State Processing > Classical ML Enhancement > Real-Time Predictions > API Distribution)
Live Quantum Circuit Visualization -> Quantum Gates in Action (Hadamard (H) - superposition states for parallel environmental scenario modeling, Rotation (R) - environmental parameters like temperature and pollution levels, CNOT (⊕) - entanglement between qubits to model environmental correlations)
Real-Time Performance Analytics -> Monitor live processing efficiency as our quantum algorithms analyze environmental data streams -> Measures system health using multiple parameters (Quantum Processors, Classical Nodes, Memory Systems, Network I/O, Error Correction)

TEMPO vs. Tradtional Forecasting:
Spatial Coverage -> Traditional Methods (Limited) vs. TEMPO AirCast (Global)
Update Frequency -> Traditional Methods (Daily) vs. TEMPO AirCast (Hourly)
Forecast Accuracy -> Traditional Methods (~75%) vs. TEMPO AirCast (95.4%)
Processing Speed -> Traditional Methods (Hours) vs. TEMPO AirCast (Minutes)
Resolution -> Traditional Methods (~50km) vs. TEMPO AirCast (~2.1km)

AI CHATBOT (https://envirocast.github.io/ai):
Enviro chatbot (this chatbot) -> Powerful LLM Interface, Real-Time Information, Precision Data, Live Responses

ENVIRONEX (https://envirocast.github.io/nex):
EnviroNex -> full quantum-enhanced environmental intelligence platform with interactive 3D globe, real-time predictions, and comprehensive health analysis
Platform Capabilities: Interactive 3D Globe (Navigate through our quantum-enhanced Earth visualization with real-time atmospheric data overlays), 24-Hour Pollution Forecasts (Real-time predictions for air quality across regions using quantum algorithms), 7-Year Climate Projections (Long-term environmental pattern analysis and weather predictions), Health Impact Analysis (Quantum-driven analysis of pollutants with detailed health risk breakdowns), Natural Disaster Tracking (Visualize pollution and atmospheric statistics during hurricanes, wildfires, and floods), AI Navigation Assistant (Integrated chatbot to help navigate models, interpret results, and explore features)
Quantum-Enhanced Intelligence: Real-Time Processing (Quantum algorithms process massive environmental datasets in real-time for instant insights), Predictive Modeling (Advanced forecasting from 24-hour pollution predictions to 7-year climate projections), Health Integration (Quantum-driven analysis linking environmental conditions to population health outcomes), Disaster Response (Emergency monitoring during natural disasters with real-time impact assessment)
Quantum Processing Core -> Advanced algorithms running 24/7

API Access & Documentation -> API (https://quantum-sky-probe.vercel.app/), Documentation (https://quantum-sky-probe.vercel.app/api-docs)

Core API Endpoints:
'GET /forecast' -> Pollution Forecasting: Predicts pollution levels and pollutant patterns using quantum-enhanced algorithms. Provides detailed forecasts for air quality, particulate matter, and chemical dispersions across specified geographic regions and time periods. (Real-time predictions, multi-pollutant analysis, geographic mapping)
'POST /health-risk' -> Health Risk Assessment: Analyzes health risks based on environmental conditions in specific areas. Correlates pollution data with population health metrics to predict potential health impacts and provide risk assessments for vulnerable populations. (Population risk analysis, vulnerable group alerts, health impact scoring)
'GET /status' -> API Status & Details: Provides comprehensive information about API functionality, including system health, available endpoints, rate limits, and quantum processing capabilities. Essential for monitoring and integration planning. (System health monitoring, rate limit information, quantum processing status)

Open Access Environmental Data: Free Access (Open-access environmental data for researchers, educators, and non-profit organizations), API Keys (Simple registration process for API access with rate limits based on usage tier), Community (Join our developer community for support, examples, and collaborative research)
EnviroCast is committed to Open Science & Environmental Research.

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
