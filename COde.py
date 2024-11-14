# main_page.py
import streamlit as st
import requests
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='')

st.title("🏞️ Creekside Trail Explorer")
st.write("Welcome to Creekside Trail Explorer! Get personalized trail recommendations, safety information, and explore visual previews of trails.")

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
    st.subheader("AI Trail Finder")
    st.write("Get personalized trail recommendations based on your preferences.")
    st.page_link("/Users/alvinliu/BUS4-118I/118i-tutorial/118i-Project/pages/Trail_Finder.py", label="Find Trails", icon="🔍")

with col2:
    st.subheader("Trail Information")
    st.write("Access comprehensive hiking guides and safety information.")
    st.page_link("/Users/alvinliu/BUS4-118I/118i-tutorial/118i-Project/pages/2_trail_info.py", label="Learn More", icon="📖")

with col3:
    st.subheader("Animal and Plant Visulaizer/Analyzer")
    st.write("Generate and explore visual previews of local flora and fauna.")
    st.page_link("/Users/alvinliu/BUS4-118I/118i-tutorial/118i-Project/pages/Visualizer.py", label="Explore Visuals", icon="🎨")
