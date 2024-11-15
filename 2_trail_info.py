import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='API-KEY')

# Sidebar Enhancement
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h2 style='color: #ffffff;'>💭 Trail Chat Assistant</h2>
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


# Apply the same nature-themed styling with black text
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
        
        h1, h2, h3, h4 {
            color: black !important;
            font-family: 'Helvetica Neue', sans-serif;
            margin-bottom: 1rem;
        }
        
        .stButton>button {
            border-radius: 20px;
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            transition: background-color 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #2980b9;
        }
        
        .stSelectbox {
            color: black;
        }
        
        .info-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            color: black !important;
        }
        
        .info-card p, .info-card li, .info-card h1, .info-card h2, .info-card h3, .info-card h4 {
            color: black !important;
        }
        
        .pro-tip {
            background-color: rgba(168, 230, 207, 0.2);
            border: 1px solid #a8e6cf;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
            color: black;
        }
        
        .topic-description {
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 2rem;
        }

        /* Ensure all markdown text is black */
        .stMarkdown, .stMarkdown p, .stMarkdown li {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

def get_hiking_info(category, model="gpt-4o-2024-08-06") -> str:
    """
    Generate hiking information using OpenAI's GPT-4.
    
    Args:
        category (str): The hiking topic to get information about
        model (str): The GPT model to use
        
    Returns:
        str: Generated information about the hiking topic
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert on hiking safety and trail information. Provide detailed, practical advice about hiking concerns and safety measures. Format your response using Markdown with appropriate headers, bullet points, and emphasis where needed."
                },
                {
                    "role": "user",
                    "content": f"Provide comprehensive information about {category} on hiking trails, including potential risks and safety tips. Include specific examples and actionable advice."
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating information: {e}")
        return None

# Main header
st.markdown("""
    <div class="main-header">
        <h1>📚 Trail Information Guide</h1>
        <p style='font-size: 1.2em; color: #34495e;'>
            Your comprehensive resource for hiking safety and trail knowledge
        </p>
    </div>
""", unsafe_allow_html=True)

# Topic selection
st.markdown("""
    <p class="topic-description">
        Select a topic to learn more about common hiking concerns and safety measures. 
        Each guide includes expert advice and practical tips for your trail adventures.
    </p>
""", unsafe_allow_html=True)

category = st.selectbox(
    "Choose your topic of interest",
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
    st.markdown(f"<h3 style='color: #2c3e50;'>{category}</h3>", unsafe_allow_html=True)
    
    with st.spinner(f"Gathering expert information about {category}..."):
        response = get_hiking_info(category)
        if response:
            st.markdown("""
                <style>
                    /* Additional style to ensure response text is black */
                    .generated-content {
                        color: black !important;
                    }
                    .generated-content * {
                        color: black !important;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="info-card">
                    <div class="generated-content">
                        {response}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="pro-tip">
                    <strong>💡 Pro Tips:</strong>
                    <ul>
                        <li>Save this information offline before your hike</li>
                        <li>Share these safety tips with your hiking companions</li>
                        <li>Review this guide during your pre-hike preparation</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# Nature-themed footer
st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem; color: black;'>
        <p>Stay safe and enjoy the trails! 🌲</p>
        <p style='font-size: 0.8em;'>© 2024 Creekside Trail Explorer | Preserving and celebrating our natural heritage</p>
    </div>
""", unsafe_allow_html=True)