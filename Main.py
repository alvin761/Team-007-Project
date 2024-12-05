import streamlit as st
import requests
import os
import openai

# Initialize OpenAI client
openai.api_key = os.environ["OPENAI_API_KEY"]

# Configure Streamlit theme
st.set_page_config(
    page_title="Creekside Trail Explorer",
    page_icon="🏞️",
    layout="wide",
    initial_sidebar_state="expanded"
)
#Alvin Liu UI
# Custom CSS for enhanced styling (keeping existing styles but removing button styles)
st.markdown("""
    <style>
        /* Main content styling */
        .stApp {
            background-color: #f5f7f9;
        }
        
        /* Header styling */
        .main-header {
            color: #2c3e50;
            font-family: 'Helvetica Neue', sans-serif;
            padding: 1.5rem 0;
            text-align: center;
            background: linear-gradient(90deg, #a8e6cf 0%, #dcedc1 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        /* Card styling */
        .css-1r6slb0 {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        .css-1r6slb0:hover {
            transform: translateY(-5px);
        }
        
        /* Chat container styling */
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Main header with enhanced styling
st.markdown("""
    <div class="main-header">
        <h1>🏞️ Creekside Trail Explorer</h1>
        <p style='font-size: 1.2em; color: #34495e;'>
            Discover the perfect trail for your next adventure
        </p>
    </div>
""", unsafe_allow_html=True)

# Welcome message with better formatting
st.markdown("""
    <div style='background-color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h3 style='color: #2c3e50;'>Welcome to Your Trail Companion! 🌲</h3>
        <p style='color: #34495e; font-size: 1.1em;'>
            Get personalized trail recommendations, essential safety information, and explore the 
            diverse flora and fauna of our local creek trails.
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Enhancement
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h2 style='color: #FFFFFF;'>💭 Trail Chat Assistant</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat container
    messages = st.container()
    with messages:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
    
    # Chat input with styling
    prompt = st.chat_input("Ask about trails...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

# Feature cards with enhanced styling
st.markdown("<h2 style='color: black;'>🎯 Explore Our Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
##############################
# [Previous imports and setup code remains the same...]

# In the button sections, update the paths like this:
with col1:
    st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; height: 100%;'>
            <h3 style='color: #2c3e50;'>🔍 AI Trail Finder</h3>
            <p style='color: #34495e; min-height: 80px;'>
                Get personalized trail recommendations based on your preferences, skill level, and desired experience.
            </p>
        </div>
    """, unsafe_allow_html=True)
    # Updated path to match your project structure
    if st.button("Find Your Trail", key="trail_finder", 
                 use_container_width=True,
                 type="primary"):
        st.switch_page("/workspaces/Team-007-Project/pages/1_trail_finder.py")  # Note the double .py extension

with col2:
    st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; height: 100%;'>
            <h3 style='color: #2c3e50;'>📖 Trail Guide</h3>
            <p style='color: #34495e; min-height: 80px;'>
                Access comprehensive hiking guides, safety tips, and essential information for a safe adventure.
            </p>
        </div>
    """, unsafe_allow_html=True)
    # Updated path for trail info
    if st.button("Learn More", key="trail_info", 
                 use_container_width=True,
                 type="primary"):
        st.switch_page("/workspaces/Team-007-Project/pages/2_trail_info.py")

with col3:
    st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; height: 100%;'>
            <h3 style='color: #2c3e50;'>🎨 Species Explorer</h3>
            <p style='color: #34495e; min-height: 80px;'>
                Generate and analyze visual previews of local flora and fauna along our creek trails.
            </p>
        </div>
    """, unsafe_allow_html=True)
    # Updated path for visualizer
    if st.button("Explore Nature", key="visualizer", 
                 use_container_width=True,
                 type="primary"):
        st.switch_page("/workspaces/Team-007-Project/pages/3_trail_visualizer.py")
#######################
# Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem; color: #7f8c8d;'>
        <p>Made with ❤️ for nature enthusiasts</p>
        <p style='font-size: 0.8em;'>© 2024 Creekside Trail Explorer</p>
    </div>
""", unsafe_allow_html=True)
