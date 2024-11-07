# main_page.py
import streamlit as st
import requests
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='')

st.title("🏞️ Creekside Trail Assistant")
st.write("Welcome to Creekside Trail Assistant! Get personalized trail recommendations, educational trail information, and explore visual previews of fauna and flora.")

# Sidebar for chat input and image generating
with st.sidebar:
    st.header("Quick Trail Chat")
    messages = st.container()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    prompt = st.chat_input("Ask a quick question about trails:")

    if prompt:
        # Add basic chat functionality on main page
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with messages:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    messages.chat_message("user").write(message["content"])

# Display feature overview
st.header("Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🤖 AI Trail Guide")
    st.write("Get personalized trail recommendations based on your preferences.")
    st.page_link("pages/1_trail_finder.py", label="Find Trails", icon="🔍")

with col2:
    st.subheader("📚 Trail Information")
    st.write("Access comprehensive hiking guides and safety information.")
    st.page_link("pages/2_trail_info.py", label="Learn More", icon="📖")

with col3:
    st.subheader("🌄 Visual Explorer")
    st.write("Generate and explore visual previews of different trail environments.")
    st.page_link("pages/3_trail_visualizer.py", label="Explore Visuals", icon="🎨")
