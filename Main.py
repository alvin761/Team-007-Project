import os
import openai
import streamlit as st
from typing import List, Optional

# Configuration and Setup
def setup_page_config():
    st.set_page_config(
        page_title="Creekside Trail Explorer",
        page_icon="🏞️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    st.markdown("""
        <style>
            .stApp {
                background-color: #f5f7f9;
            }
            
            .main-header {
                color: #2c3e50;
                font-family: 'Helvetica Neue', sans-serif;
                padding: 1.5rem 0;
                text-align: center;
                background: linear-gradient(90deg, #a8e6cf 0%, #dcedc1 100%);
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            
            .feature-card {
                background-color: white;
                padding: 1.5rem;
                border-radius: 10px;
                height: 100%;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
            }
            
            .chat-container {
                background-color: white;
                border-radius: 10px;
                padding: 1rem;
                margin-top: 1rem;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .welcome-section {
                background-color: white;
                padding: 1.5rem;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

def display_logo():
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        st.markdown('<div style="max-width: 80%; margin: auto;">', unsafe_allow_html=True)
        st.image("logo.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def display_header():
    st.markdown("""
        <div class="main-header">
            <h1>🏞️ Creekside Trail Explorer</h1>
            <p style='font-size: 1.2em; color: #34495e;'>
                Discover the perfect trail for your next adventure
            </p>
        </div>
    """, unsafe_allow_html=True)

def display_welcome_message():
    st.markdown("""
        <div class="welcome-section">
            <h3 style='color: #2c3e50;'>Welcome to Your Trail Companion! 🌲</h3>
            <p style='color: #34495e; font-size: 1.1em;'>
                Get personalized trail recommendations, essential safety information, and explore the 
                diverse flora and fauna of our local creek trails.
            </p>
        </div>
    """, unsafe_allow_html=True)

def setup_chat_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h2 style='color: #FFFFFF;'>💭 Trail Chat Assistant</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        messages = st.container()
        with messages:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
        
        prompt = st.chat_input("Ask about trails...")
        if prompt:
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })

def create_feature_card(title: str, description: str, button_text: str, page_path: str, key: str):
    st.markdown(f"""
        <div class='feature-card'>
            <h3 style='color: #2c3e50;'>{title}</h3>
            <p style='color: #34495e; min-height: 80px;'>
                {description}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(button_text, key=key, use_container_width=True, type="primary"):
        st.switch_page(f"pages/{page_path}")

def display_feature_cards():
    st.markdown("<h2 style='color: black;'>🎯 Explore Our Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_feature_card(
            "🔍 AI Trail Finder",
            "Get personalized trail recommendations based on your preferences, skill level, and desired experience.",
            "Find Your Trail",
            "trailfinder.py",
            "trail_finder"
        )
    
    with col2:
        create_feature_card(
            "📖 Trail Guide",
            "Access comprehensive hiking guides, safety tips, and essential information for a safe adventure.",
            "Learn More",
            "2_trail_info.py",
            "trail_info"
        )
    
    with col3:
        create_feature_card(
            "🎨 Species Explorer",
            "Generate and analyze visual previews of local flora and fauna along our creek trails.",
            "Explore Nature",
            "3_trail_visualizer.py",
            "visualizer"
        )

def main():
    # Initialize OpenAI client
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    # Setup and configuration
    setup_page_config()
    load_custom_css()
    
    # Display components
    display_logo()
    display_header()
    display_welcome_message()
    setup_chat_sidebar()
    display_feature_cards()

if __name__ == "__main__":
    main()
