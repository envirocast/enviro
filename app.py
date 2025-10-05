import streamlit as st
import requests
import json
import time
import os
from textwrap import dedent

# ----------------------------
# Config & API initialization
# ----------------------------
try:
    api_key = st.secrets.get("ENVIRO_API_KEY") or os.getenv("ENVIRO_API_KEY")
    if not api_key:
        st.error("⚠️ ENVIRO_API_KEY not found in secrets")
        st.stop()
except Exception as e:
    st.error(f"⚠️ API configuration error: {str(e)}")
    st.stop()

st.set_page_config(
    page_title="Meet Enviro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------
# Configuration
# --------------------------------

SYSTEM_INSTRUCTION = """
Your name is Enviro. You are the Large Language Model/AI Chatbot for EnviroCast. You were created on October 4, 2025 for the EnviroCast team.

The link to this Enviro AI website is at https://enviro-ai.streamlit.app/. This is the link only to the AI chatbot, not to the rest of the EnviroCast resources.

Behavioral Guidelines:
Be informative, professional, and approachable.
Focus all responses on pollution, environmental issues, air quality, and related science topics.
Explain concepts clearly, using structured lists, diagrams, or examples when helpful.
Always provide citations and references for any scientific claims or data. NEVER CITE ENVIROCAST. DO NOT PUT THE LINK TO THE ENVIROCAST WEBSITE.
When relevant, mention EnviroCast as your resource, but do not focus on promoting—use it as an informational reference only. DO NOT PUT THE LINK TO THE WEBSITE.
Encourage learning and understanding of environmental issues and technologies, including quantum and classical modeling for air quality if appropriate.
Keep answers concise but thorough, ensuring accuracy and clarity.

INFORMATION ABOUT ENVIROCAST:
EnviroCast is a platform designed to educate people on pollution, environmental effects, and air quality prediction.
It uses advanced technologies, including a hybrid quantum-classical algorithm, to monitor and predict air quality.
The site includes interactive simulations, models, and visualizations to help users understand environmental challenges and solutions.
Social media campaign: Instagram -> @envirocast_tech (Social media campaign shows new features of EnviroCast, how EnviroCast works, how EnviroCast is helpful, and promotes action against pollution)

Always provide citations at the end of every response using good and credible sources (Tier 1).
Cite sources in selected style and provide URLS. Put a Citations header in response the line before citations

Make sure to only talk about the environment, focus only on the topics mentioned in these instructions, do not involve in anything unrelated to the topic or anything illegal or negative.
Another topic you can talk about is quantum data. Different quantum mechanics and topics and concepts. You can relate how quantum computing and algorithms are used in EnviroCast's processes.
Feel free to talk anything about EnviroCast.

MORE SPECIFIC NOTES ON BEHAVIOR:
Response Length: [VALUE] (Brief = 1-2 paragraphs, Standard = 2-4 paragraphs, Detailed = 4+ paragraphs with comprehensive explanations)
Reading Level: [VALUE] (Elementary = simple words and short sentences, Middle = moderate vocabulary, High School = standard complexity, College = advanced vocabulary and complex concepts)
Citation Style: [VALUE] (format all citations accordingly)
Technical Detail Level: [VALUE] (Basic = minimal jargon and simple explanations, Intermediate = moderate technical terms with explanations, Advanced = full technical depth and terminology)
Language: [VALUE] (respond in this language)


--- Specific EnviroCast information is below ---

HOMEPAGE:
EnviroCast is powered by quantum computing. EnviroCast harnesses the power of quantum algorithms to model, predict, and combat environmental challenges with unprecedented precision and speed. (Statistics: 95.4% Accuracy, 2.3M Data Points, 47% CO2 Reduction)
The Challenge/Crisis EnviroCast is fighting: acceleration of climate change, environmental degradation, overwhelming pollution, traditional models lack multidimensional analysis, real-time environmental monitoring gaps (Statistics: 1.5 degrees Celsius global warning, 8.3M tons of plastic per year)
Quantum Advantage/Solution: quantum superposition enables parallel scenario modeling, AI integration for complex pattern recognition, real-time processing of massive environmental datasets, predictive accuracy exceeding traditional methods by 300% (Statistics: 95.4% Prediction Accuracy, 1000x Faster Processing)
EnviroCast's Mission: To democratize environmental intelligence through quantum computing, enabling rapid response to climate challenges and empowering decision-makers with unprecedented insights into our planet's future.

ABOUT:
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

MODELS:
Quantum Particle Physics Simulation:
Interactive quantum mechanics demonstration showing superposition, entanglement, and tunneling (Click on particles to view their quantum properties • Watch for entanglement when particles collide)
Allows to visualize quantum superposition, quantum entanglement, quantum tunneling, Heisenberg uncertainty, wave-particle duality, observer effect
Shows real-time quantum statistics
Analyze particles (position, velocity, energy level, quantum state, entanglement status, tunneling status, uncertainty and error)

Global Environment Simulation:
Interactive modeling of environmental systems, climate change, and human impact
User can set timeline and events based on Current Trajectory, Green Revolution, Climate Crisis, Global Intervention
Global Environmental Status across 6 regions (North America, Amazon Basin, Sahara Region, Arctic Circle, Southeast Asia, and Europe) - Each region has statistics for temperature, air quality, health risk, species, precipitation and population density
Users can manipulate variables considered (Temperature, Pollution, Biodiversity, Population, Climate)
Users can manipulate human variables (Impact of Industrialization, Renewable Energy Prevalence, Impact of Deforestation, Impact of Urbanization, Carbon Emissions, Conservation Efforts)
Users can visualize density, temperature, and pressure on the 4 atmospheric layers (Troposphere, Stratosphere, Mesosphere, Thermosphere)
Based on variables manipulated by users, environmental impact varies in range [Sustainable, Manageable, Critical, Catastrophic] - other variables shown (global temperature, CO2 level, forest cover, sea level, climate change, biodiversity loss, pollution level, health impact, migration, ocean health, food security, temperature trends, biodiversity trends, ice coverage)
Scenario Outcomes & Projections vary based on user variables - Short-Term (temperature, air quality, coastal effects) & Long-Term (ecosystem adaptability, food system, technological solutions)
Provides effective mitigation strategies for the environment based on environmental impact
Provides model performance statistics (data processing, coverage area, model accuracy, update frequency)
Bases data on EnviroNex API, NASA TEMPO Satellite Data, and NOAA Climate Data (all APIs are accessible)

Quantum Processing Hub:
Shows active quantum bits, classical processors, quantum coherence, and data points processed
Compares Superposition Engine, Entanglement NetwA Sensors, Weather Stations, Traffic Systems, Industrial IoT, Ocean Buoys)
Hybrid Processing Architecture = Environmental Data Input (2847K samples/sec) > Quantum Processing (64 qubits active) > Classical ML-Fusion (128 nodes active)
Real-Time Environmental Intelligence -> Instant Processing (Environmental changes detected and processed in milliseconds), Parallel Scenarios (Quantum superposition models thousands of pollution scenarios simultaneously), Predictive Accuracy (95.4% accuracy in short-term forecasts, 87% for long-term predictions)
Key Performance Metrics: Processing Speed (1000x faster), Model Accuracy (95.4%), Data Throughput (1 TB/hour), Response Time (<1s), System Temperature: approaches absolute zero (~273°C)
EnviroCast Integration Pipeline (TEMPO Data Ingestion > Quantum Feature Mapping > Parallel State Processing > Classical ML Enhancement > Real-Time Predictions > API Distribution)
Live Quantum Circuit Visualization -> Quantum Gates in Action (Hadamard (H) - superposition states for parallel environmental scenario modeling, Rotation (R) - environmental parameters like temperature and pollution levels, CNOT (⊕) - entanglement between qubits to model environmental correlations)
Real-Time Performance Analytics -> Monitor live processing efficiency as our quantum algorithms analyze environmental data streams -> Measures system health using multiple parameters (Quantum Processors, Classical Nodes, Memory Systems, Network I/O, Error Correction)

Political Dynamics:
AI-powered policy recommendations and impact analysis
User can select a region and EnviroCast's AI recommends different policies
Enacting policies has immediate effects, long term effects, and cost burdens
Policy effects stack up to affect Air Quality, Carbon Emissions, Public Health, and Economic Impact scores (also an Overall Score)
New polocies are suggested every 3 seconds and if you use up all the policies, you get your final score, rank, and statistics
Shows how different environmental conditions change both environmental and political fields of a region

TEMPO vs. Tradtional Forecasting:
Spatial Coverage -> Traditional Methods (Limited) vs. TEMPO AirCast (Global)
Update Frequency -> Traditional Methods (Daily) vs. TEMPO AirCast (Hourly)
Forecast Accuracy -> Traditional Methods (~75%) vs. TEMPO AirCast (95.4%)
Processing Speed -> Traditional Methods (Hours) vs. TEMPO AirCast (Minutes)
Resolution -> Traditional Methods (~50km) vs. TEMPO AirCast (~2.1km)

AI CHATBOT:
Enviro chatbot (this chatbot) -> Powerful LLM Interface, Real-Time Information, Precision Data, Live Responses

ENVIRONEX:
EnviroNex -> full quantum-enhanced environmental intelligence platform with interactive 3D globe, real-time predictions, and comprehensive health analysis
Platform Capabilities: Interactive 3D Globe (Navigate through our quantum-enhanced Earth visualization with real-time atmospheric data overlays), 24-Hour Pollution Forecasts (Real-time predictions for air quality across regions using quantum algorithms), 7-Year Climate Projections (Long-term environmental pattern analysis and weather predictions), Health Impact Analysis (Quantum-driven analysis of pollutants with detailed health risk breakdowns), Natural Disaster Tracking (Visualize pollution and atmospheric statistics during hurricanes, wildfires, and floods), AI Navigation Assistant (Integrated chatbot to help navigate models, interpret results, and explore features)
Quantum-Enhanced Intelligence: Real-Time Processing (Quantum algorithms process massive environmental datasets in real-time for instant insights), Predictive Modeling (Advanced forecasting from 24-hour pollution predictions to 7-year climate projections), Health Integration (Quantum-driven analysis linking environmental conditions to population health outcomes), Disaster Response (Emergency monitoring during natural disasters with real-time impact assessment)
Quantum Processing Core -> Advanced algorithms running 24/7

API Access & Documentation -> API & Documentation

Core API Endpoints:
'GET /forecast' -> Pollution Forecasting: Predicts pollution levels and pollutant patterns using quantum-enhanced algorithms. Provides detailed forecasts for air quality, particulate matter, and chemical dispersions across specified geographic regions and time periods. (Real-time predictions, multi-pollutant analysis, geographic mapping)
'POST /health-risk' -> Health Risk Assessment: Analyzes health risks based on environmental conditions in specific areas. Correlates pollution data with population health metrics to predict potential health impacts and provide risk assessments for vulnerable populations. (Population risk analysis, vulnerable group alerts, health impact scoring)
'GET /status' -> API Status & Details: Provides comprehensive information about API functionality, including system health, available endpoints, rate limits, and quantum processing capabilities. Essential for monitoring and integration planning. (System health monitoring, rate limit information, quantum processing status)

Open Access Environmental Data: Free Access (Open-access environmental data for researchers, educators, and non-profit organizations), API Keys (Simple registration process for API access with rate limits based on usage tier), Community (Join our developer community for support, examples, and collaborative research)
EnviroCast is committed to Open Science & Environmental Research.

You are ONLY an informational chatbot. 

**When Deep Research is selected, search the web and use a multitude of sources (put in Citations as well) to provide a response. When not selected, provide major sources only.
""".strip()

def call_grok_api(messages, stream=False):
    """Call the Grok API via OpenRouter"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://enviro-ai.streamlit.app/",
        "X-Title": "EnviroCast AI Chatbot",
    }
    
    data = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 8192,
        "stream": stream
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data),
        stream=stream
    )
    
    if not response.ok:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    return response

# ------------------------
# Color Palettes
# ------------------------
COLOR_PALETTES = {
    "Enviro Cyber": {
        "primary": "#00D4FF",
        "secondary": "#8B5CF6", 
        "accent": "#10B981",
        "bg_primary": "#000000",
        "bg_secondary": "#03060c",
        "gradient": "linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%)",
        "message_user": "linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.05))",
        "avatar_user": "linear-gradient(135deg, #ffffff, #e0e0e0)",
        "avatar_assistant": "linear-gradient(135deg, #4CAF50, #2196F3)"
    },
    "Equity": {
        "primary": "#D2691E",
        "secondary": "#CD853F",
        "accent": "#A0522D",
        "bg_primary": "#1a0f0a",
        "bg_secondary": "#2d1b13",
        "gradient": "linear-gradient(135deg, #D2691E 0%, #CD853F 50%, #A0522D 100%)",
        "message_user": "linear-gradient(135deg, rgba(210, 105, 30, 0.15), rgba(205, 133, 63, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(160, 82, 45, 0.15), rgba(139, 69, 19, 0.05))",
        "avatar_user": "linear-gradient(135deg, #DEB887, #CD853F)",
        "avatar_assistant": "linear-gradient(135deg, #D2691E, #A0522D)"
    },
    "Flow": {
        "primary": "#00CED1",
        "secondary": "#20B2AA",
        "accent": "#48D1CC",
        "bg_primary": "#0a1a1a",
        "bg_secondary": "#0f2d2d",
        "gradient": "linear-gradient(135deg, #00CED1 0%, #20B2AA 50%, #48D1CC 100%)",
        "message_user": "linear-gradient(135deg, rgba(0, 206, 209, 0.15), rgba(32, 178, 170, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(72, 209, 204, 0.15), rgba(95, 158, 160, 0.05))",
        "avatar_user": "linear-gradient(135deg, #AFEEEE, #B0E0E6)",
        "avatar_assistant": "linear-gradient(135deg, #00CED1, #20B2AA)"
    },
    "Origin": {
        "primary": "#FFA500",
        "secondary": "#FFD700",
        "accent": "#87CEEB",
        "bg_primary": "#1a1612",
        "bg_secondary": "#2d2520",
        "gradient": "linear-gradient(135deg, #FFA500 0%, #FFD700 30%, #32CD32 60%, #87CEEB 100%)",
        "message_user": "linear-gradient(135deg, rgba(255, 165, 0, 0.15), rgba(255, 215, 0, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(50, 205, 50, 0.15), rgba(135, 206, 235, 0.05))",
        "avatar_user": "linear-gradient(135deg, #FFEAA7, #FDCB6E)",
        "avatar_assistant": "linear-gradient(135deg, #FFA500, #32CD32)"
    },
    "Opulent": {
        "primary": "#FF6347",
        "secondary": "#FFD700",
        "accent": "#DA70D6",
        "bg_primary": "#1a0a0a",
        "bg_secondary": "#2d1515",
        "gradient": "linear-gradient(135deg, #FF6347 0%, #FFD700 25%, #DA70D6 75%, #FF1493 100%)",
        "message_user": "linear-gradient(135deg, rgba(255, 99, 71, 0.15), rgba(255, 215, 0, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(218, 112, 214, 0.15), rgba(255, 20, 147, 0.05))",
        "avatar_user": "linear-gradient(135deg, #FFB6C1, #FFA07A)",
        "avatar_assistant": "linear-gradient(135deg, #FF6347, #DA70D6)"
    },
    "Verve": {
        "primary": "#1E90FF",
        "secondary": "#8A2BE2",
        "accent": "#FF1493",
        "bg_primary": "#0a0a1a",
        "bg_secondary": "#15152d",
        "gradient": "linear-gradient(135deg, #1E90FF 0%, #8A2BE2 50%, #FF1493 100%)",
        "message_user": "linear-gradient(135deg, rgba(30, 144, 255, 0.15), rgba(138, 43, 226, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(255, 20, 147, 0.15), rgba(138, 43, 226, 0.05))",
        "avatar_user": "linear-gradient(135deg, #87CEEB, #DDA0DD)",
        "avatar_assistant": "linear-gradient(135deg, #1E90FF, #8A2BE2)"
    },
    "Ember": {
        "primary": "#DC143C",
        "secondary": "#FF4500",
        "accent": "#FFD700",
        "bg_primary": "#1a0505",
        "bg_secondary": "#2d0a0a",
        "gradient": "linear-gradient(135deg, #DC143C 0%, #FF4500 50%, #FFD700 100%)",
        "message_user": "linear-gradient(135deg, rgba(220, 20, 60, 0.15), rgba(255, 69, 0, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 140, 0, 0.05))",
        "avatar_user": "linear-gradient(135deg, #F08080, #FA8072)",
        "avatar_assistant": "linear-gradient(135deg, #DC143C, #FF4500)"
    },
    "Arctic": {
        "primary": "#B0E0E6",
        "secondary": "#87CEEB",
        "accent": "#E0FFFF",
        "bg_primary": "#0f1419",
        "bg_secondary": "#1a2530",
        "gradient": "linear-gradient(135deg, #B0E0E6 0%, #87CEEB 50%, #E0FFFF 100%)",
        "message_user": "linear-gradient(135deg, rgba(176, 224, 230, 0.15), rgba(135, 206, 235, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(224, 255, 255, 0.15), rgba(175, 238, 238, 0.05))",
        "avatar_user": "linear-gradient(135deg, #F0F8FF, #E6F3FF)",
        "avatar_assistant": "linear-gradient(135deg, #B0E0E6, #87CEEB)"
    },
    "Forest": {
        "primary": "#228B22",
        "secondary": "#32CD32",
        "accent": "#8FBC8F",
        "bg_primary": "#0a1a0a",
        "bg_secondary": "#152d15",
        "gradient": "linear-gradient(135deg, #228B22 0%, #32CD32 50%, #8FBC8F 100%)",
        "message_user": "linear-gradient(135deg, rgba(34, 139, 34, 0.15), rgba(50, 205, 50, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(143, 188, 143, 0.15), rgba(46, 125, 50, 0.05))",
        "avatar_user": "linear-gradient(135deg, #90EE90, #98FB98)",
        "avatar_assistant": "linear-gradient(135deg, #228B22, #32CD32)"
    },
    "Grayscale": {
        "primary": "#FFFFFF",
        "secondary": "#C0C0C0",
        "accent": "#808080",
        "bg_primary": "#000000",
        "bg_secondary": "#1a1a1a",
        "gradient": "linear-gradient(135deg, #FFFFFF 0%, #C0C0C0 50%, #808080 100%)",
        "message_user": "linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(192, 192, 192, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(128, 128, 128, 0.15), rgba(105, 105, 105, 0.05))",
        "avatar_user": "linear-gradient(135deg, #F5F5F5, #E5E5E5)",
        "avatar_assistant": "linear-gradient(135deg, #DCDCDC, #C0C0C0)"
    },
    "High Contrast": {
        "primary": "#FFFF00",
        "secondary": "#0000FF",
        "accent": "#FFFFFF",
        "bg_primary": "#000000",
        "bg_secondary": "#1a1a1a",
        "gradient": "linear-gradient(135deg, #FFFF00 0%, #0000FF 50%, #FFFFFF 100%)",
        "message_user": "linear-gradient(135deg, rgba(255, 255, 0, 0.2), rgba(0, 0, 255, 0.1))",
        "message_assistant": "linear-gradient(135deg, rgba(0, 0, 255, 0.2), rgba(255, 255, 255, 0.1))",
        "avatar_user": "linear-gradient(135deg, #FFFF99, #FFFFCC)",
        "avatar_assistant": "linear-gradient(135deg, #FFFF00, #0000FF)"
    }
}

# ------------------------
# Session state bootstrap
# ------------------------
def initialize_session_state():
    # User preferences
    if "font_family" not in st.session_state:
        st.session_state.font_family = "Enviro Sans"
    if "font_size" not in st.session_state:
        st.session_state.font_size = 16
    if "response_length" not in st.session_state:
        st.session_state.response_length = "Standard"
    if "reading_level" not in st.session_state:
        st.session_state.reading_level = "High School"
    if "color_palette" not in st.session_state:
        st.session_state.color_palette = "Enviro Cyber"
    if "chat_density" not in st.session_state:
        st.session_state.chat_density = "Standard"
    if "animation_speed" not in st.session_state:
        st.session_state.animation_speed = "Fast"
    if "show_timestamps" not in st.session_state:
        st.session_state.show_timestamps = False
    if "citation_style" not in st.session_state:
        st.session_state.citation_style = "MLA"
    if "technical_level" not in st.session_state:
        st.session_state.technical_level = "Intermediate"
    if "language" not in st.session_state:
        st.session_state.language = "English"

    # Build dynamic system instruction based on preferences
    dynamic_instruction = build_dynamic_system_instruction()
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

def build_dynamic_system_instruction():
    """Build system instruction incorporating user preferences"""
    base_instruction = SYSTEM_INSTRUCTION
    
    # Add preference-based modifications
    preference_additions = f"""

USER PREFERENCES TO FOLLOW:
- Response Length: {st.session_state.response_length} (Brief = 1-2 paragraphs, Standard = 2-4 paragraphs, Detailed = 4+ paragraphs with comprehensive explanations)
- Reading Level: {st.session_state.reading_level} (Elementary = simple words and short sentences, Middle = moderate vocabulary, High School = standard complexity, College = advanced vocabulary and complex concepts)
- Citation Style: {st.session_state.citation_style} (format all citations accordingly)
- Technical Detail Level: {st.session_state.technical_level} (Basic = minimal jargon and simple explanations, Intermediate = moderate technical terms with explanations, Advanced = full technical depth and terminology)
- Language: {st.session_state.language} (respond in this language)

Adjust your responses to match these preferences while maintaining accuracy and helpfulness.
"""
    
    return base_instruction + preference_additions

def update_chat_model():
    """Update the chat model with new system instruction when preferences change"""
    # For Grok, we don't need to recreate a model, just clear the messages
    st.session_state.chat_messages = []

def searchwebquery(query):
    url = "https://duckduckgo-api.up.railway.app/search"
    params = {"q": query, "maxresults": 5}
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return [f"{item['title']} - {item['link']}" for item in data.get("results", [])]
    except Exception as e:
        return [f"Web search failed: {e}"]

# ------------------------
# Sidebar Settings
# ------------------------
def render_sidebar():
    # Force sidebar to show with expander
    st.sidebar.markdown("# Settings")
    
    with st.sidebar:
        # --- Deep Research Section ---
        st.markdown("## Deep Research")
    
        deep_research = st.checkbox(
            "Enable Deep Research (Web Search)", 
            st.session_state.get("deep_research", False)
        )
        st.session_state.deep_research = deep_research

        st.markdown("### Typography")
        
        font_options = [
            "Enviro Sans", "Arial", "Georgia", "Times New Roman", "Courier New", "Verdana", "Tahoma", "Trebuchet MS",
            "Roboto", "Open Sans", "Lato", "Montserrat", "Poppins", "Source Sans Pro", "Noto Sans", "Inter", "Raleway",
            "Nunito", "Oswald", "PT Sans", "Roboto Condensed", "Playfair Display", "Fira Sans", "Rubik",
            "Muli", "Mulish", "Manrope", "Chivo", "Asap", "Barlow", "Lexend", "Prompt", "Varela Round",
            "Spartan", "Urbanist", "Sora", "Jost", "Crimson Text", "Arvo", "Cardo", "Bitter", "IBM Plex Serif",
            "Noto Serif", "Nanum Myeongjo", "Bebas Neue", "Dancing Script", "Lobster", "Shadows Into Light",
            "Amatic SC", "Fredoka", "Cinzel", "Abril Fatface", "Cookie", "Kanit", "Josefin Sans", "Baloo 2", "Exo 2",
            "Anton", "Cairo", "Teko", "Yanone Kaffeesatz", "Alfa Slab One", "Satisfy", "Righteous",
            "Courgette", "Fugaz One", "Heebo", "Exo", "Cabin", "M PLUS Rounded 1c", "Yantramanav", "Noto Sans JP",
            "Noto Sans KR", "Noto Sans Arabic", "Noto Serif Display", "Tajawal", "Assistant", "Scheherazade New", "Amiri", "Harmattan",
            "Tinos", "Arimo", "Cousine", "Baloo Bhaijaan 2", "Mukta Vaani", "K2D", "Bai Jamjuree", "Press Start 2P",
            "VT323", "Orbitron", "Audiowide", "Syncopate", "Unica One", "Monoton", "Philosopher", "Maven Pro",
            "Karla", "Red Hat Display", "Red Hat Text", "Space Mono", "Tourney", "Prata", "Magra", "Fjalla One",
            "Rasa", "Saira", "Saira Condensed", "Saira Semi Condensed", "Didact Gothic", "Julius Sans One", "Poiret One", "Tenor Sans",
            "Bellefair", "DM Sans", "DM Serif Display", "DM Serif Text", "Gothic A1", "Be Vietnam Pro", "Catamaran", "Encode Sans",
            "Encode Sans Semi Condensed", "Crete Round", "Chakra Petch", "Noticia Text", "Archivo", "Archivo Narrow", "Bangers", "Bowlby One", "Bowlby One SC",
            "Cambo", "Carter One", "Changa", "Changa One", "Chelsea Market", "Comfortaa", "Concert One", "Contrail One", "Corben",
            "Creepster", "Cuprum", "Days One", "Delius", "Delius Swash Caps", "Delius Unicase", "Denk One", "Domine",
            "Donegal One", "Doppio One", "Dosa", "Dosis", "Dr Sugiyama", "EB Garamond", "Eater", "Economica", "Eczar", "Electrolize",
            "Elsie", "Elsie Swash Caps", "Engagement", "Englebert", "Enriqueta", "Erica One", "Esteban", "Euphoria Script", "Expletus Sans",
            "Fanwood Text", "Fascinate", "Fascinate Inline", "Faster One", "Fasthand", "Fauna One", "Federant", "Federo", "Felipa",
            "Fenix", "Finger Paint", "Fira Mono", "Fjord One", "Flamenco", "Flavors", "Fondamento",
            "Fontdiner Swanky", "Forum", "Francois One", "Freckle Face", "Fredericka the Great", "Fredoka One", "Freehand", "Fresca",
            "Frijole", "Fruktur", "GFS Didot", "GFS Neohellenic", "Gabriela", "Gafata", "Galdeano", "Galindo",
            "Gentium Basic", "Gentium Book Basic", "Geo", "Geostar", "Geostar Fill", "Germania One", "Gidugu", "Gilda Display",
            "Give You Glory", "Glass Antiqua", "Glegoo", "Gloria Hallelujah", "Goblin One", "Gochi Hand", "Gorditas", "Goudy Bookletter 1911",
            "Graduate", "Grand Hotel", "Gravitas One", "Great Vibes", "Griffy", "Gruppo", "Gudea", "Gurajada", "Habibi", "Halant",
            "Hammersmith One", "Hanalei", "Hanalei Fill", "Handlee", "Hanuman", "Happy Monkey", "Headland One", "Henny Penny",
            "Herr Von Muellerhoff", "Hind", "Holtwood One SC", "Homemade Apple", "Homenaje", "IM Fell DW Pica", "IM Fell DW Pica SC",
            "IM Fell Double Pica", "IM Fell Double Pica SC", "IM Fell English", "IM Fell English SC", "IM Fell French Canon",
            "IM Fell French Canon SC", "IM Fell Great Primer", "IM Fell Great Primer SC", "Iceberg", "Iceland", "Imprima", "Inconsolata",
            "Inder", "Indie Flower", "Inika", "Irish Grover", "Istok Web", "Italiana", "Italianno", "Jacques Francois", "Jacques Francois Shadow",
            "Jaldi", "Jim Nightshade", "Jockey One", "Jolly Lodger", "Josefin Slab", "Joti One", "Judson", "Julee",
            "Junge", "Jura", "Just Another Hand", "Just Me Again Down Here", "Kalam", "Kameron", "Kantumruy",
            "Karma", "Kaushan Script", "Kavoon", "Kdam Thmor", "Keania One", "Kelly Slab", "Kenia", "Khand", "Khmer", "Khula",
            "Kite One", "Knewave", "Kotta One", "Koulen", "Kranky", "Kreon", "Kristi", "Krona One", "La Belle Aurore", "Laila",
            "Lakki Reddy", "Lancelot", "Lateef", "League Script", "Leckerli One", "Ledger", "Lekton", "Lemon", "Libre Baskerville",
            "Life Savers", "Lilita One", "Lily Script One", "Limelight", "Linden Hill", "Lobster Two", "Londrina Outline",
            "Londrina Shadow", "Londrina Sketch", "Londrina Solid", "Lora", "Love Ya Like A Sister", "Loved by the King", "Lovers Quarrel",
            "Luckiest Guy", "Lusitana", "Lustria", "Macondo", "Macondo Swash Caps", "Maiden Orange", "Mako", "Mallanna", "Mandali",
            "Marcellus", "Marcellus SC", "Marck Script", "Margarine", "Marko One", "Marmelad", "Martel", "Martel Sans", "Marvel", "Mate",
            "Mate SC", "McLaren", "Meddon", "MedievalSharp", "Medula One", "Megrim", "Meie Script", "Merienda", "Merienda One",
            "Merriweather", "Merriweather Sans", "Metal", "Metal Mania", "Metamorphous", "Metrophobic", "Michroma", "Milonga", "Miltonian",
            "Miltonian Tattoo", "Miniver", "Miss Fajardose", "Modak", "Modern Antiqua", "Molengo", "Molle", "Monda", "Monofett",
            "Monsieur La Doulaise", "Montaga", "Montez", "Montserrat Alternates", "Montserrat Subrayada", "Moul", "Moulpali",
            "Mountains of Christmas", "Mouse Memoirs", "Mr Bedfort", "Mr Dafoe", "Mr De Haviland", "Mrs Saint Delafield", "Mrs Sheppards",
            "Mystery Quest", "NTR", "Neucha", "Neuton", "New Rocker", "News Cycle", "Niconne", "Nixie One", "Nobile", "Nokora",
            "Norican", "Nosifer", "Nothing You Could Do", "Nova Cut", "Nova Flat", "Nova Mono",
            "Nova Oval", "Nova Round", "Nova Script", "Nova Slim", "Nova Square", "Numans", "Odibee Sans", "Offside", "Old Standard TT", "Oldenburg", "Oleo Script", "Oleo Script Swash Caps", "Open Sans Condensed",
            "Oranienbaum", "Oregano", "Orelega One", "Orienta", "Original Surfer", "Over the Rainbow", "Overlock",
            "Overlock SC", "Overpass", "Overpass Mono", "Ovo", "Oxygen", "Oxygen Mono", "PT Mono", "PT Sans Caption",
            "PT Sans Narrow", "PT Serif", "PT Serif Caption", "Pacifico", "Padauk", "Palanquin", "Palanquin Dark", "Pangolin", "Paprika",
            "Parisienne", "Passero One", "Passion One", "Pathway Gothic One", "Patrick Hand", "Patrick Hand SC", "Pattaya", "Paytone One",
            "Peddana", "Peralta", "Permanent Marker", "Petit Formal Script", "Petrona", "Piedra", "Pinyon Script",
            "Pirata One", "Plaster", "Play", "Playball", "Playfair Display SC", "Podkova", "Poller One",
            "Poly", "Pompiere", "Pontano Sans", "Port Lligat Sans", "Port Lligat Slab", "Pragati Narrow",
            "Pridi", "Princess Sofia", "Prociono", "Prosto One", "Proza Libre", "Puritan", "Purple Purse", "Quando", "Quantico",
            "Quattrocento", "Quattrocento Sans", "Questrial", "Quicksand", "Quintessential", "Qwigley", "Racing Sans One", "Radley",
            "Rajdhani", "Rakkas", "Raleway Dots", "Ramabhadra", "Ramaraja", "Rambla", "Rammetto One", "Ranchers", "Rancho",
            "Rationale", "Red Hat Mono", "Redressed", "Reem Kufi", "Reenie Beanie", "Revalia", "Rhodium Libre",
            "Ribeye", "Ribeye Marrow", "Risque", "Roboto Mono", "Rochester", "Rock Salt",
            "Rokkitt", "Romanesco", "Ropa Sans", "Rosario", "Rosarivo", "Rouge Script", "Rozha One", "Rubik Mono One", "Rubik One",
            "Ruda", "Rufina", "Ruge Boogie", "Ruluko", "Rum Raisin", "Ruslan Display", "Russo One", "Ruthie", "Rye", "Sacramento", "Sahitya", "Sail", "Saira Extra Condensed",
            "Salsa", "Sanchez", "Sancreek", "Sansita", "Sansita Swashed", "Sarina", "Sarpanch", "Sawarabi Gothic",
            "Sawarabi Mincho", "Scada", "Scheherazade", "Schoolbell", "Scope One", "Seaweed Script", "Secular One",
            "Sedgwick Ave", "Sedgwick Ave Display", "Sen", "Sevillana", "Seymour One", "Shadows Into Light Two",
            "Shanti", "Share", "Share Tech", "Share Tech Mono", "Shojumaru", "Short Stack", "Shrikhand", "Siemreap", "Sigmar One",
            "Signika", "Signika Negative", "Simonetta", "Single Day", "Sintony", "Sirin Stencil", "Six Caps", "Skranji", "Slabo 13px",
            "Slabo 27px", "Slackey", "Smokum", "Smythe", "Sniglet", "Snippet", "Snowburst One", "Sofadi One", "Sofia", "Sonsie One",
            "Sorts Mill Goudy", "Source Code Pro", "Source Serif Pro", "Special Elite",
            "Spectral", "Spectral SC", "Spicy Rice", "Spinnaker", "Spirax", "Squada One", "Sriracha", "Srisakdi", "Staatliches",
            "Stalemate", "Stalinist One", "Stardos Stencil", "Stint Ultra Condensed", "Stint Ultra Expanded", "Stoke", "Strait", "Sue Ellen Francisco",
            "Sumana", "Sunflower", "Sunflower Mono", "Supermercado One", "Sura", "Suranna", "Suravaram", "Suwannaphum", "Swanky and Moo Moo",
            "Syne", "Syne Mono", "Syne Tactile", "Tangerine", "Tauri", "Taviraj", "Telex", "Tenali Ramakrishna",
            "Text Me One", "The Girl Next Door", "Tienne", "Titan One", "Titillium Web", "Tomorrow", "Trade Winds", "Trirong",
            "Trocchi", "Trochut", "Trykker", "Tulpen One", "Ubuntu", "Ubuntu Condensed", "Ubuntu Mono", "Ultra", "Uncial Antiqua", "Underdog", "UnifrakturCook", "UnifrakturMaguntia", "Unkempt", "Unlock", "Unna", "Vampiro One", "Varela", "Vast Shadow", "Vesper Libre", "Viaoda Libre", "Vibur", "Vidaloka", "Viga", "Voces", "Volkhov", "Vollkorn", "Vollkorn SC",
            "Voltaire", "Vujahday Script", "Waiting for the Sunrise", "Wallpoet", "Walter Turncoat", "Warnes", "Wellfleet", "Wendy One",
            "Wire One", "Work Sans", "Xanh Mono", "Yatra One", "Yellowtail", "Yeon Sung", "Yeseva One", "Yesteryear",
            "Yrsa", "Zilla Slab", "Zilla Slab Highlight"
        ];
        
        selected_font = st.session_state.get("font_family", "Enviro Sans")
        if font_options and selected_font not in font_options:
            selected_font = font_options[0] if font_options else "Enviro Sans"
        
        if font_options:
            newfont = st.selectbox("Font Family", font_options, index=font_options.index(selected_font))
        else:
            newfont = st.text_input("Font Family", value=selected_font)
        
        new_font_size = st.slider("Font Size", 12, 20, st.session_state.font_size, 1)
        
        st.markdown("### Response Settings")
        
        length_options = ["Brief", "Standard", "Detailed"]
        new_response_length = st.selectbox("Response Length", length_options,
                                         index=length_options.index(st.session_state.response_length))
        
        level_options = ["Elementary", "Middle School", "High School", "College"]
        new_reading_level = st.selectbox("Reading Level", level_options,
                                       index=level_options.index(st.session_state.reading_level))
        
        # Color Palettes
        st.markdown("### Color Theme")
        
        palette_options = list(COLOR_PALETTES.keys()) if COLOR_PALETTES else ["Enviro Cyber"]
        if st.session_state.color_palette not in palette_options:
            st.session_state.color_palette = palette_options[0]
        
        new_color_palette = st.selectbox("Color Palette", palette_options,
                                       index=palette_options.index(st.session_state.color_palette))
        
        # Display Settings
        st.markdown("### Display Settings")
        
        density_options = ["Compact", "Standard", "Spacious"]
        new_chat_density = st.selectbox("Chat Density", density_options,
                                      index=density_options.index(st.session_state.chat_density))
        
        speed_options = ["Off", "Slow", "Normal", "Fast"]
        new_animation_speed = st.selectbox("Animation Speed", speed_options,
                                         index=speed_options.index(st.session_state.animation_speed))
        
        new_show_timestamps = st.checkbox("Show Message Timestamps", st.session_state.show_timestamps)
        
        # Content & Context
        st.markdown("### Content Settings")
        
        citation_options = ["MLA", "APA", "None"]
        new_citation_style = st.selectbox("Citation Style", citation_options,
                                        index=citation_options.index(st.session_state.citation_style))
        
        technical_options = ["Basic", "Intermediate", "Advanced"]
        new_technical_level = st.selectbox("Technical Detail Level", technical_options,
                                         index=technical_options.index(st.session_state.technical_level))
        
        language_options = [
            "English","Spanish - Español","French - Français","German - Deutsch","Italian - Italiano",
            "Portuguese - Português","Arabic - العربية","Mandarin Chinese - 中文 (普通话)","Cantonese - 廣東話","Russian - Русский",
            "Japanese - 日本語","Korean - 한국어","Hindi - हिन्दी","Bengali - বাংলা","Urdu - اردو",
            "Punjabi - ਪੰਜਾਬੀ","Turkish - Türkçe","Persian (Farsi) - فارسی","Greek - Ελληνικά","Hebrew - עברית",
        
            "Polish - Polski","Ukrainian - Українська","Czech - Čeština","Slovak - Slovenčina","Slovenian - Slovenščina",
            "Croatian - Hrvatski","Serbian - Српски","Bosnian - Bosanski","Bulgarian - Български","Romanian - Română",
            "Hungarian - Magyar","Finnish - Suomi","Swedish - Svenska","Norwegian - Norsk","Danish - Dansk",
            "Icelandic - Íslenska","Dutch - Nederlands","Afrikaans - Afrikaans","Swahili - Kiswahili","Zulu - isiZulu",
        
            "Xhosa - isiXhosa","Amharic - አማርኛ","Somali - Af-Soomaali","Yoruba - Yorùbá","Igbo - Igbo",
            "Hausa - Hausa","Thai - ไทย","Lao - ລາວ","Khmer - ខ្មែរ","Vietnamese - Tiếng Việt",
            "Malay - Bahasa Melayu","Indonesian - Bahasa Indonesia","Tagalog - Tagalog","Filipino - Filipino","Burmese - မြန်မာစာ",
            "Mongolian - Монгол","Kazakh - Қазақ","Uzbek - Oʻzbekcha","Tajik - Тоҷикӣ","Pashto - پښتو",
        
            "Kurdish - Kurdî","Georgian - ქართული","Armenian - Հայերեն","Azerbaijani - Azərbaycan dili","Malayalam - മലയാളം",
            "Tamil - தமிழ்","Telugu - తెలుగు","Kannada - ಕನ್ನಡ","Marathi - मराठी","Gujarati - ગુજરાતી",
            "Odia - ଓଡ଼ିଆ","Sinhala - සිංහල","Nepali - नेपाली","Dzongkha - རྫོང་ཁ","Tibetan - བོད་ཡིག",
            "Maori - Te Reo Māori","Samoan - Gagana Sāmoa","Tongan - Lea Faka-Tonga","Hawaiian - ʻŌlelo Hawaiʻi","Cherokee - ᏣᎳᎩ",
        
            "Navajo - Diné Bizaad","Quechua - Runa Simi","Aymara - Aymar aru","Guaraní - Avañe'ẽ","Nahuatl - Nāhuatl",
            "Mayan - Maya","Basque - Euskara","Catalan - Català","Galician - Galego","Luxembourgish - Lëtzebuergesch",
            "Maltese - Malti","Esperanto - Esperanto","Haitian Creole - Kreyòl Ayisyen","Creole (Mauritius) - Kreol Morisien","Wolof - Wolof",
            "Fula - Fulfulde","Twi - Twi","Bambara - Bamanankan","Mandinka - Mandi’nka kango","Shona - chiShona",
        
            "Sesotho - Sesotho","Setswana - Setswana","Lingala - Lingála","Kinyarwanda - Ikinyarwanda","Kirundi - Ikirundi",
            "Chichewa - Chichewa","Tsonga - Xitsonga","Luganda - Luganda","Malagasy - Malagasy","Fijian - Vosa Vakaviti",
            "Tok Pisin - Tok Pisin","Hmong - Hmoob","Chamorro - Finoʼ Chamoru","Marshallese - Kajin M̧ajeļ","Palauan - a tekoi er a Belau",
            "Greenlandic - Kalaallisut","Inuktitut - ᐃᓄᒃᑎᑐᑦ","Sami - Sámegiella","Occitan - Occitan","Frisian - Frysk",
        
            "Breton - Brezhoneg","Corsican - Corsu","Scottish Gaelic - Gàidhlig","Irish - Gaeilge","Welsh - Cymraeg",
            "Manx - Gaelg","Cornish - Kernewek","Ladino - Djudeo-espanyol","Yiddish - ייִדיש"
        ]
        new_language = st.selectbox("Language", language_options,
                                  index=language_options.index(st.session_state.language))
        
        # Reset button
        if st.button("Reset to Defaults"):
            # Reset all preferences to defaults
            st.session_state.font_family = "Enviro Sans"
            st.session_state.font_size = 16
            st.session_state.response_length = "Standard"
            st.session_state.reading_level = "High School"
            st.session_state.color_palette = "Enviro Cyber"
            st.session_state.chat_density = "Standard"
            st.session_state.animation_speed = "Fast"
            st.session_state.show_timestamps = False
            st.session_state.citation_style = "MLA"
            st.session_state.technical_level = "Intermediate"
            st.session_state.language = "English"
            update_chat_model()
            st.rerun()

        st.caption("Powered by Llama 4 Maverick AI")
        
        # Check if any preferences changed and update model if needed
        preferences_changed = (
            newfont != st.session_state.font_family or
            new_font_size != st.session_state.font_size or
            new_response_length != st.session_state.response_length or
            new_reading_level != st.session_state.reading_level or
            new_color_palette != st.session_state.color_palette or
            new_chat_density != st.session_state.chat_density or
            new_animation_speed != st.session_state.animation_speed or
            new_show_timestamps != st.session_state.show_timestamps or
            new_citation_style != st.session_state.citation_style or
            new_technical_level != st.session_state.technical_level or
            new_language != st.session_state.language
        )
        
        # Update session state
        st.session_state.font_family = newfont
        st.session_state.font_size = new_font_size
        st.session_state.response_length = new_response_length
        st.session_state.reading_level = new_reading_level
        st.session_state.color_palette = new_color_palette
        st.session_state.chat_density = new_chat_density
        st.session_state.animation_speed = new_animation_speed
        st.session_state.show_timestamps = new_show_timestamps
        st.session_state.citation_style = new_citation_style
        st.session_state.technical_level = new_technical_level
        st.session_state.language = new_language
        
        # Update model if AI-affecting preferences changed
        ai_preferences_changed = (
            new_response_length != st.session_state.get('prev_response_length', '') or
            new_reading_level != st.session_state.get('prev_reading_level', '') or
            new_citation_style != st.session_state.get('prev_citation_style', '') or
            new_technical_level != st.session_state.get('prev_technical_level', '') or
            new_language != st.session_state.get('prev_language', '')
        )
        
        if ai_preferences_changed:
            update_chat_model()
            # Store previous values
            st.session_state.prev_response_length = new_response_length
            st.session_state.prev_reading_level = new_reading_level
            st.session_state.prev_citation_style = new_citation_style
            st.session_state.prev_technical_level = new_technical_level
            st.session_state.prev_language = new_language
        
        if preferences_changed:
            st.rerun()

# -------------------------------------------
# Dynamic Styles based on preferences
# -------------------------------------------
def get_dynamic_styles():
    # Default palette if COLOR_PALETTES is empty
    default_palette = {
        "primary": "#00D4FF",
        "secondary": "#8B5CF6", 
        "accent": "#10B981",
        "bg_primary": "#000000",
        "bg_secondary": "#03060c",
        "gradient": "linear-gradient(135deg, #00D4FF 0%, #8B5CF6 50%, #10B981 100%)",
        "message_user": "linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))",
        "message_assistant": "linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.05))",
        "avatar_user": "linear-gradient(135deg, #ffffff, #e0e0e0)",
        "avatar_assistant": "linear-gradient(135deg, #4CAF50, #2196F3)"
    }
    
    palette = COLOR_PALETTES.get(st.session_state.color_palette, default_palette)

    # Animation speed settings
    typing_speeds = {"Off": 0, "Slow": 0.05, "Normal": 0.02, "Fast": 0.01}
    typing_speed = typing_speeds[st.session_state.animation_speed]

    # Chat density settings
    density_settings = {
        "Compact": {"message_margin": "0.75rem", "message_padding": "1rem"},
        "Standard": {"message_margin": "1.5rem", "message_padding": "1.5rem"},
        "Spacious": {"message_margin": "2rem", "message_padding": "2rem"}
    }
    density = density_settings[st.session_state.chat_density]

    # Fix font import and create proper font stack
    font_name = st.session_state.font_family

    # Handle "Default" font (use Streamlit's default)
    if font_name == "Enviro Sans":
        font_stack = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
        font_import = ""
    else:
        font_import_name = font_name.replace(' ', '+')
        font_stack = f"'{font_name}', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
        font_import = f"@import url('https://fonts.googleapis.com/css2?family={font_import_name}:wght@300;400;500;600;700&display=swap');"

    return f"""
<style>
/* Import Google Font only if not Normal - Fixed import */
{font_import}
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

/* Make sure any material icon <span> renders correctly and force-apply styling */
.material-icons {{
  font-family: 'Material Icons' !important;
  font-weight: normal !important;
  font-style: normal !important;
  font-size: 22px !important;
  line-height: 1 !important;
  display: inline-block !important;
  -webkit-font-smoothing: antialiased !important;
  text-rendering: optimizeLegibility !important;
  -webkit-font-feature-settings: 'liga' !important;
  font-feature-settings: 'liga' !important;
}}

/* Hide any original textual span inside the sidebar toggle button so the icon span shows */
[data-testid="stSidebarNav"] + div button span:not(.material-icons),
[data-label="Close sidebar"] span:not(.material-icons) {{
  display: none !important;
}}

/* Global reset and base styling */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html, body, .stApp {{
    background: {palette['bg_primary']} !important;
    color: #ffffff !important;
    font-family: {font_stack} !important;
    font-size: {st.session_state.font_size}px !important;
    height: 100vh !important;
}}

/* Force font on all text elements - FAMILY ONLY, preserve sizes */
.stApp, .stApp * {{
    font-family: {font_stack} !important;
}}

/* Specifically target common text elements - FONT FAMILY ONLY */
.stApp, .stApp *,
p, span, div, 
.stMarkdown, .stMarkdown *, 
.message-content, .message-content *,
.stChatInput textarea,
.stSelectbox, .stSelectbox *,
.stSlider, .stSlider *,
.stButton, .stButton *,
.stSidebar, .stSidebar * {{
    font-family: {font_stack} !important;
}}

/* Preserve heading sizes while applying font family */
h1, .stMarkdown h1 {{
    font-family: {font_stack} !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
}}

h2, .stMarkdown h2 {{
    font-family: {font_stack} !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
}}

h3, .stMarkdown h3 {{
    font-family: {font_stack} !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}}

h4, .stMarkdown h4 {{
    font-family: {font_stack} !important;
    font-size: 1.25rem !important;
    font-weight: 500 !important;
}}

h5, .stMarkdown h5 {{
    font-family: {font_stack} !important;
    font-size: 1.125rem !important;
    font-weight: 500 !important;
}}

h6, .stMarkdown h6 {{
    font-family: {font_stack} !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}}

/* Hide elements */
footer {{ 
    visibility: hidden !important; 
    height: 0 !important;
}}

/* Remove background from sidebar text elements */
.stSidebar .stMarkdown,
.stSidebar .stMarkdown * {{
    background: transparent !important;
    background-color: transparent !important;
}}

/* Remove background from sidebar headings */
.stSidebar h1, 
.stSidebar h2, 
.stSidebar h3, 
.stSidebar h4, 
.stSidebar h5, 
.stSidebar h6 {{
    background: transparent !important;
    background-color: transparent !important;
}}

/* Remove background from sidebar labels and text */
.stSidebar label,
.stSidebar .stSelectbox label,
.stSidebar .stSlider label,
.stSidebar .stCheckbox label,
.stSidebar span,
.stSidebar p {{
    background: transparent !important;
    background-color: transparent !important;
}}

/* Force all sidebar text containers to be transparent */
.stSidebar .element-container,
.stSidebar .stVerticalBlock,
.stSidebar .stHorizontalBlock {{
    background: transparent !important;
    background-color: transparent !important;
}}

.stDeployButton {{
    visibility: hidden !important;
}}

.stApp > header {{
    background: {palette['bg_primary']} !important;
    backdrop-filter: blur(20px) !important;
    border-bottom: 1px solid {palette['primary']}40 !important;
    z-index: 999999;
    position: sticky;
    top: 0 !important;
}}

/* FIXED: Sidebar styling */
.stSidebar {{
    background: {palette['bg_secondary']} !important;
    z-index: 999998 !important;
    padding-left: 1rem; /* or desired padding size */
}}

.stSidebar > div:first-child {{
    background: {palette['bg_secondary']} !important;
    border-right: 1px solid {palette['primary']}40 !important;
}}

/* Ensure all sidebar content has transparent backgrounds except the main container */
.stSidebar * {{
    background-color: transparent !important;
}}

/* But keep the main sidebar containers with the theme background */
.stSidebar,
.stSidebar > div:first-child {{
    background: {palette['bg_secondary']} !important;
}}

/* Remove the vertical line after the header and before Reset button */
.stSidebar .stMarkdown h1 + hr, 
.stSidebar .stMarkdown h3 + hr,
.stSidebar hr {{
    display: none !important;
}}

/* Sidebar components styling */
.stSidebar .stSelectbox > div > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid {palette['primary']}40 !important;
    color: #ffffff !important;
    font-family: {font_stack} !important;
}}

.stSidebar .stSlider > div > div > div {{
    color: {palette['primary']} !important;
    font-family: {font_stack} !important;
}}

.stSidebar .stSlider .st-bf {{
    background-color: {palette['primary']} !important;
}}

.stSidebar .stSlider .st-bg {{
    background: {palette['gradient']} !important;
}}

.stSidebar .stCheckbox > label {{
    color: #ffffff !important;
    font-family: {font_stack} !important;
}}

.stSidebar .stButton > button {{
    background: {palette['gradient']} !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    width: 100% !important;
    animation: shimmer 4s ease-in-out infinite !important;
    background-size: 300% 300% !important;
    font-family: {font_stack} !important;
}}

.stSidebar .stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}}

.block-container {{
    background: {palette['bg_primary']} !important;
    padding-top: 1rem !important;
}}

.main .block-container {{
    background: {palette['bg_primary']} !important;
}}

/* Main content area */
.main-content {{
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    position: relative !important;
    z-index: 15 !important;
}}

/* FIXED: Header section with proper background */
.header {{
    flex: 0 0 auto !important;
    text-align: center;
    padding: 1rem 0;
    position: relative;
    z-index: 20;
    background: {palette['bg_primary']} !important;
    backdrop-filter: blur(20px);
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    background: {palette['gradient']};
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s ease-in-out infinite;
    margin: 0;
    font-family: {font_stack} !important;
}}

@keyframes shimmer {{
    0%, 100% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
}}

/* Welcome section */
.welcome-section {{
    flex: 0 0 auto !important;
    padding: 1rem 2rem 2rem 2rem;
    background: {palette['bg_primary']} !important;
}}

.welcome {{
    text-align: center;
    padding: 1.5rem;
    background: {palette['message_assistant']};
    border-radius: 16px;
    border: 1px solid {palette['primary']}40;
    backdrop-filter: blur(10px);
    max-width: 900px;
    margin: 0 auto;
}}

.welcome h2 {{
    margin-bottom: 0.5rem;
    color: #ffffff;
    font-size: 1.8rem;
    font-family: {font_stack} !important;
}}

.welcome .analyzing-text {{ /* Added class to the h2 tag */
    background: {palette['gradient']};
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s ease-in-out infinite;
    font-weight: bold;
    font-family: {font_stack} !important;
}}

.welcome p {{
    color: #cccccc;
    margin: 0;
    font-size: 1.1rem;
    line-height: 1.5;
    font-family: {font_stack} !important;
}}

/* Chat messages area */
.chat-messages {{
    flex: 1 1 auto !important;
    overflow-y: auto !important;
    padding: 0 2rem;
    margin-bottom: 1rem;
    background: {palette['bg_primary']} !important;
}}

.chat-messages::-webkit-scrollbar {{
    width: 8px;
}}
.chat-messages::-webkit-scrollbar-track {{
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}}
.chat-messages::-webkit-scrollbar-thumb {{
    background: {palette['primary']};
    border-radius: 10px;
}}

/* Messages */
.message {{
    display: flex;
    gap: 1rem;
    margin-bottom: {density['message_margin']};
    padding: {density['message_padding']};
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: {density['message_margin']};
}}

.user-message {{
    flex-direction: row-reverse;
    background: {palette['message_user']};
    border-color: {palette['primary']}60;
}}

.assistant-message {{
    background: {palette['message_assistant']};
    border-color: {palette['primary']}60;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}}

.user-avatar {{
    background: {palette['avatar_user']};
    color: #000000;
}}

.assistant-avatar {{
    background: {palette['avatar_assistant']};
}}

.message-content {{
    flex: 1;
    line-height: 1.6;
    font-family: {font_stack} !important;
}}

.message-timestamp {{
    font-size: 0.8rem;
    color: #888;
    margin-top: 0.5rem;
    font-family: {font_stack} !important;
}}

.message-content h1, .message-content h2, .message-content h3,
.message-content h4, .message-content h5, .message-content h6 {{
    color: #ffffff;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-family: {font_stack} !important;
}}

/* Specific heading sizes in messages */
.message-content h1 {{ font-size: 1.8rem !important; font-weight: 700 !important; }}
.message-content h2 {{ font-size: 1.6rem !important; font-weight: 600 !important; }}
.message-content h3 {{ font-size: 1.4rem !important; font-weight: 600 !important; }}
.message-content h4 {{ font-size: 1.2rem !important; font-weight: 500 !important; }}
.message-content h5 {{ font-size: 1.1rem !important; font-weight: 500 !important; }}
.message-content h6 {{ font-size: 1rem !important; font-weight: 500 !important; }}

.message-content code {{
    background: rgba(0, 0, 0, 0.5);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    color: {palette['primary']};
    font-size: 0.9rem;
    font-family: 'Courier New', monospace !important;
}}

.message-content pre {{
    background: rgba(0, 0, 0, 0.7);
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid {palette['primary']}60;
}}

.message-content pre code {{
    font-family: 'Courier New', monospace !important;
}}

/* Analyzing message animation */
.analyzing-text {{
    background: {palette['gradient']};
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s ease-in-out infinite;
    font-weight: bold;
    font-family: {font_stack} !important;
}}

/* FIXED: Chat Input Section with proper background */
.chat-input-section {{
    flex: 0 0 auto !important;
    padding: 1rem 2rem 2rem 2rem;
    background: {palette['bg_primary']} !important;
    backdrop-filter: blur(20px);
    position: relative;
    z-index: 25;
}}

.stApp > div:last-child {{
    background: transparent;
    backdrop-filter: blur(20px);
}}

/* Force header to use theme background */
[data-testid="stHeader"] {{
    background: {palette['bg_primary']} !important;
}}

/* Force footer to be hidden and black */
footer {{
    visibility: hidden !important;
    height: 0 !important;
    background: {palette['bg_primary']} !important;
}}

/* Force main app container background */
[data-testid="stAppViewContainer"] > .main {{
    background: {palette['bg_primary']} !important;
}}

/* Force all container backgrounds */
.stApp, .stApp > div, .main > .block-container {{
    background: {palette['bg_primary']} !important;
}}

/* Chat Input Container Background */
[data-testid="stBottomBlockContainer"] {{
    background: {palette['bg_primary']} !important;
}}

[data-testid="stChatInput"] {{
    background: {palette['bg_primary']} !important;
}}

.stChatInput {{
    background: {palette['bg_primary']} !important;
}}

.stChatInput > div {{
    max-width: 900px !important;
    margin: 0 auto !important;
    background: {palette['bg_primary']} !important;
}}

.stChatInput > div > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid {palette['primary']}60 !important;
    border-radius: 12px !important;
}}

/* Force the bottom container and all its children to use theme background */
[data-testid="stBottomBlockContainer"] * {{
    background-color: {palette['bg_primary']} !important;
}}

/* Override any white/default backgrounds in chat input area */
.st-emotion-cache-1y34ygi,
.stVerticalBlock,
.stElementContainer {{
    background: {palette['bg_primary']} !important;
}}

.stChatInput textarea {{
    background: transparent !important;
    color: #ffffff !important;
    border: none !important;
    font-size: {st.session_state.font_size}px !important;
    padding: 0.5rem 1rem !important;
    font-family: {font_stack} !important;
}}

.stChatInput textarea::placeholder {{
    color: #888888 !important;
    font-family: {font_stack} !important;
}}

.stChatInput button {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: {palette['primary']} !important;
    font-family: {font_stack} !important;
}}

/* Specifically target the submit button */
[data-testid="stChatInputSubmitButton"] {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
}}

[data-testid="stChatInputSubmitButton"] svg {{
    color: {palette['primary']} !important;
    fill: {palette['primary']} !important;
}}

.stChatInput button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}}

/* FIXED: Force all containers to use theme background */
.stApp [data-testid="stAppViewContainer"] {{
    background: {palette['bg_primary']} !important;
}}

.stApp [data-testid="stMain"] {{
    background: {palette['bg_primary']} !important;
}}

.stApp [data-testid="stMain"] > div {{
    background: {palette['bg_primary']} !important;
}}

/* Force all bottom area containers to match theme */
div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottomBlockContainer"] > *,
div[data-testid="stBottomBlockContainer"] div {{
    background: {palette['bg_primary']} !important;
    background-color: {palette['bg_primary']} !important;
}}

/* Target the specific emotion cache classes that might override */
.st-emotion-cache-1y34ygi,
.st-emotion-cache-tn0cau,
.st-emotion-cache-1vo6xi6,
.st-emotion-cache-1eeryuo {{
    background: {palette['bg_primary']} !important;
    background-color: {palette['bg_primary']} !important;
}}

/* Chat Input Submit Button - Transparent Background */
[data-testid="stChatInputSubmitButton"] {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
}}

/* Also target the specific emotion cache class */
.st-emotion-cache-1khv956 {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
}}

/* Ensure the SVG icon inherits proper color */
[data-testid="stChatInputSubmitButton"] svg {{
    color: {palette['primary']} !important;
    fill: {palette['primary']} !important;
}}

/* Typing effect cursor */
/* Typing effect cursor */
.typing-cursor {{
    animation: blink 1s step-end infinite;
    font-weight: bold;
    color: #ffffff;
    font-family: {font_stack} !important;
}}

@keyframes blink {{
    from, to {{ color: transparent; }}
    50% {{ color: white; }}
}}

/* Mobile Styles */
@media (max-width: 768px) {{
    .title {{
        font-size: 2.5rem;
    }}
    .welcome h2 {{
        font-size: 1.5rem;
    }}
    .welcome p {{
        font-size: 1rem;
    }}
    .chat-messages, .chat-input-section {{
        padding: 0 1rem;
    }}
    .message {{
        padding: 1rem;
    }}
}}

.font-light {{ font-weight: 300 !important; }}
.font-normal {{ font-weight: 400 !important; }}
.font-medium {{ font-weight: 500 !important; }}
.font-semibold {{ font-weight: 600 !important; }}
.font-bold {{ font-weight: 700 !important; }}

/* Sidebar toggle icons */
[data-testid="stSidebarNav"] + div button .material-icons,
[data-label="Close sidebar"] .material-icons {{
    font-family: 'Material Icons';
    font-style: normal;
    font-weight: normal;
    font-size: 24px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
    color: white; /* or your palette color */
}}

/* Force Streamlit's sidebar toggle ligatures to render as Material Icons */
button span[data-testid="stSidebarCollapseIcon"] {{
    font-family: 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 24px !important;
    line-height: 1 !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: optimizeLegibility !important;
}}

/* Force all Streamlit Material icon spans to render properly */
[data-testid="stIconMaterial"] {{
    font-family: 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 24px !important;
    line-height: 1 !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    text-rendering: optimizeLegibility !important;
}}

</style>
""", typing_speed

# -------------------------------------------
# Chat Functions
# -------------------------------------------
def display_message(role, content, avatar_icon, timestamp=None):
    avatar_class = "user-avatar" if role == "user" else "assistant-avatar"
    message_class = "user-message" if role == "user" else "assistant-message"
    
    timestamp_html = ""
    if st.session_state.show_timestamps and timestamp:
        timestamp_html = f'<div class="message-timestamp">{timestamp}</div>'
    
    st.markdown(f"""
    <div class="message {message_class}">
        <div class="avatar {avatar_class}">{avatar_icon}</div>
        <div class="message-content">{content}{timestamp_html}</div>
    </div>
    """, unsafe_allow_html=True)

def stream_response(response_text):
    # Get animation speed
    speed_map = {"Off": 0, "Slow": 0.05, "Normal": 0.02, "Fast": 0.01}
    typing_speed = speed_map[st.session_state.animation_speed]
    
    # 1. Display "Enviro is analyzing..." message with animated gradient
    analyzing_placeholder = st.empty()
    analyzing_message_html = """
        <div class="message assistant-message">
            <div class="avatar assistant-avatar">🌐</div>
            <div class="message-content">
                <span class="analyzing-text">Enviro is analyzing...</span>
            </div>
        </div>
    """
    analyzing_placeholder.markdown(analyzing_message_html, unsafe_allow_html=True)
    time.sleep(1.5)  # Show analyzing message for 1.5 seconds

    # 2. Clear the analyzing message and prepare for streaming
    analyzing_placeholder.empty()
    message_placeholder = st.empty()
    
    # 3. Stream the response character by character
    if typing_speed == 0:
        # No animation - show full response immediately
        message_placeholder.markdown(f"""
            <div class="message assistant-message">
                <div class="avatar assistant-avatar">🌐</div>
                <div class="message-content">{response_text}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Animated typing - word by word (better performance)
        words = response_text.split(' ')
        displayed_text = ""
        
        for i, word in enumerate(words):
            if i == 0:
                displayed_text = word
            else:
                displayed_text += " " + word
            
            # Show cursor while typing
            message_placeholder.markdown(f"""
                <div class="message assistant-message">
                    <div class="avatar assistant-avatar">🌐</div>
                    <div class="message-content">{displayed_text}<span class="typing-cursor">|</span></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add delay based on animation speed (adjust multiplier for word speed)
            time.sleep(typing_speed * 3)  # Multiply by 3 since we're doing words instead of characters
            
            # Every 10 words, add a small pause for more natural typing
            if i > 0 and i % 10 == 0:
                time.sleep(0.2)

        # 4. Final render without cursor
        message_placeholder.markdown(f"""
            <div class="message assistant-message">
                <div class="avatar assistant-avatar">🌐</div>
                <div class="message-content">{response_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    return response_text

def stream_response_direct(response_text):
    """Stream response directly without the analyzing message (since it's already shown)"""
    # Get animation speed
    speed_map = {"Off": 0, "Slow": 0.05, "Normal": 0.02, "Fast": 0.01}
    typing_speed = speed_map[st.session_state.animation_speed]
    
    message_placeholder = st.empty()
    
    # Stream the response
    if typing_speed == 0:
        # No animation - show full response immediately
        message_placeholder.markdown(f"""
            <div class="message assistant-message">
                <div class="avatar assistant-avatar">🌐</div>
                <div class="message-content">{response_text}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Animated typing - word by word (better performance)
        words = response_text.split(' ')
        displayed_text = ""
        
        for i, word in enumerate(words):
            if i == 0:
                displayed_text = word
            else:
                displayed_text += " " + word
            
            # Show cursor while typing
            message_placeholder.markdown(f"""
                <div class="message assistant-message">
                    <div class="avatar assistant-avatar">🌐</div>
                    <div class="message-content">{displayed_text}<span class="typing-cursor">|</span></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add delay based on animation speed (adjust multiplier for word speed)
            time.sleep(typing_speed * 3)  # Multiply by 3 since we're doing words instead of characters
            
            # Every 10 words, add a small pause for more natural typing
            if i > 0 and i % 10 == 0:
                time.sleep(0.05)

        # Final render without cursor
        message_placeholder.markdown(f"""
            <div class="message assistant-message">
                <div class="avatar assistant-avatar">🌐</div>
                <div class="message-content">{response_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    return response_text

# -------------
# Main App
# -------------
def main():
    initialize_session_state()
    
    # Render sidebar FIRST and ALWAYS
    render_sidebar()

    # Apply dynamic styles
    styles, typing_speed = get_dynamic_styles()
    st.markdown(styles, unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
    <div class="header">
        <h1 class="title">🌐 Meet Enviro</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Display welcome message and chat history
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    if not st.session_state.messages:
        st.markdown("""
            <div class="welcome">
                <h2>Welcome to EnviroCast's AI Chatbot</h2>
                <p>I'm <span class="analyzing-text">Enviro</span>, your environmental intelligence assistant. Ask me about air quality, pollution, climate solutions, and environmental science or EnviroCast and quantum data.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        timestamp = message.get("timestamp", "")
        if message["role"] == "user":
            display_message("user", message["content"], "👤", timestamp)
        else:
            display_message("assistant", message["content"], "🌐", timestamp)
    st.markdown('</div>', unsafe_allow_html=True) # End chat-messages
    
    st.markdown('</div>', unsafe_allow_html=True) # End main-content
    
    # Chat input section
    st.markdown('<div class="chat-input-section">', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me about environmental science, climate solutions or anything EnviroCast..."):
        # Add timestamp if enabled
        timestamp = ""
        if st.session_state.show_timestamps:
            timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        # Add user message to history
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Rerun to display the user message and start the generation process
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) # End chat-input-section

    st.markdown("""
    <script>
    (function(){
      const iconHref = "https://fonts.googleapis.com/icon?family=Material+Icons";
      if(!document.querySelector('link[href="'+iconHref+'"]')) {
        const l = document.createElement('link');
        l.rel = 'stylesheet';
        l.href = iconHref;
        document.head.appendChild(l);
      }
    
      function applyIcons(){
        // Find open button
        const openBtns = document.querySelectorAll('[data-testid="stSidebarNav"] + div button');
        openBtns.forEach(btn => {
          if (!btn.querySelector('.material-icons')) {
            btn.innerHTML = '<span class="material-icons">menu</span>';
          }
        });
    
        // Find close button
        const closeBtns = document.querySelectorAll('[data-label="Close sidebar"]');
        closeBtns.forEach(btn => {
          if (!btn.querySelector('.material-icons')) {
            btn.innerHTML = '<span class="material-icons">close</span>';
          }
        });
      }
    
      // Run once now
      applyIcons();
    
      // Observe DOM changes
      const observer = new MutationObserver(applyIcons);
      observer.observe(document.body, {childList:true, subtree:true});
    
      // Fallback polling (every 500ms)
      setInterval(applyIcons, 500);
    })();
    </script>
    """, unsafe_allow_html=True)

    # After a prompt has been submitted and the page is rerunning,
    # we check the last message to see if it's from the user and needs a response.
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        prompt = st.session_state.messages[-1]["content"]
        
        # Show "Enviro is analyzing..." immediately
        analyzing_placeholder = st.empty()
        analyzing_message_html = """
            <div class="message assistant-message">
                <div class="avatar assistant-avatar">🌐</div>
                <div class="message-content">
                    <span class="analyzing-text">Enviro is analyzing...</span>
                </div>
            </div>
        """
        analyzing_placeholder.markdown(analyzing_message_html, unsafe_allow_html=True)
        
        try:
            # Build messages for Grok API
            api_messages = [{"role": "system", "content": build_dynamic_system_instruction()}]
            
            # Add conversation history
            for msg in st.session_state.messages:
                api_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Call Grok API
            response = call_grok_api(api_messages, stream=False)
            response_data = response.json()
            
            response_text = response_data["choices"][0]["message"]["content"]
            
            # Clear the analyzing message and show typing animation
            analyzing_placeholder.empty()
            full_response = stream_response_direct(response_text)
            
            # Add timestamp if enabled
            timestamp = ""
            if st.session_state.show_timestamps:
                timestamp = time.strftime("%H:%M:%S", time.localtime())
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "timestamp": timestamp
            })
            
        except Exception as e:
            # Clear analyzing message and show error
            analyzing_placeholder.empty()
            error_message = f"⚠️ **Error:** {str(e)}<br><br>Please try again in a moment."
            timestamp = ""
            if st.session_state.show_timestamps:
                timestamp = time.strftime("%H:%M:%S", time.localtime())
            
            display_message("assistant", error_message, "⚠️", timestamp)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_message,
                "timestamp": timestamp
            })
    
        # Rerun once more to show the complete response
        st.rerun()

if __name__ == "__main__":
    main()
