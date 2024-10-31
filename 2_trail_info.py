# pages/2_trail_info.py
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='')

def get_hiking_info(category, model="gpt-3.5-turbo"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert on hiking safety and trail information. Provide detailed, practical advice about hiking concerns and safety measures."},
                {"role": "user", "content": f"Provide comprehensive information about {category} on hiking trails, including potential risks and safety tips."}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating information: {e}")
        return None

st.title("📚 Trail Information Guide")
st.write("Select a topic to learn more about common hiking concerns and safety measures.")

category = st.selectbox(
    "What would you like to know about?",
    options=[
        "Wildlife Encounters & Safety",
        "Plant Hazards & Identification",
        "Weather Safety & Preparation",
        "Navigation & Trail Markers",
        "First Aid & Emergency Response",
        "Gear & Equipment Essentials",
        "Water Safety & Hydration",
        "Trail Etiquette & Rules",
        "Seasonal Hiking Tips",
        "Physical Preparation & Fitness"
    ]
)

if category:
    st.write(f"### {category}")
    with st.spinner(f"Generating information about {category}..."):
        response = get_hiking_info(category)
        if response:
            st.markdown(response)
            st.info("💡 **Pro Tip**: Save this information for offline reference when hiking!")
