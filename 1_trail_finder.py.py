# pages/1_trail_finder.py
import streamlit as st
import requests
import os
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize OpenAI client
client = OpenAI(api_key='')

def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "As an expert in nature trails, provide recommendations for creekside trails based on location, difficulty level, and visitor preferences."},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating trail recommendation: {e}")
        return None

st.title("🔍 Trail Finder")
st.write("Get personalized trail recommendations based on your preferences.")


#webapp practice

st.title("Trail Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())
    
    st.subheader("Trail Data Summary")
    st.write(df.describe())

    st.subheader("Filter Trail Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select Value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if st.button("Generate Plot"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])
else:
    st.write("Waiting on file to upload")
###### Code done make sure to use later for coding - Carlos

#Code to plot a map - Carlos
map_data = pd.DataFrame(
    np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
    columns=['lat', 'lon'])

####### CODE PLOT ^

#### AI CHATBOT - CArlos
st.title("Trail ChatBot")
client = OpenAI(api_key='Your-API-Key')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Chat history

if "messages" not in st.session_state:
    st.session_state = []

# Display chat message history

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("How is it going")
if prompt:
    #display messages
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role" : m["role"], "content": m["content"]}
            for m in st.session_state.messages
            
        ],
        stream = True,
    ):
        full_response += response.choices[0].delta.get("content","")
        message_placeholder.markdown(full_response + " ")
    message_placeholder.markdown(full_response)
st.session_state.messages.append({"role": "assistant", "content": full_response})
                                 
                







with st.sidebar:
    st.header("Trail Explorer Chat")
    messages = st.container()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    #Changed it to st.text_area to show a bigger box - Carlos 
    prompt = st.text_area("Describe the type of trail (location, difficulty):")

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        text_response = get_completion(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": text_response})

        with messages:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    messages.chat_message("user").write(message["content"])
                else:
                    messages.chat_message("assistant").write(message["content"])

####### AI CHAT BOT NOT WORKING ^ -CARLOS


#Imports the pandas data base in section 1 -Carlos 
df = pd.read_csv("/Users/carlos/Downloads/Santa_Clara_County_Parks_20241029.csv")




st.title ("Santa Clara Couintry Trail Parks")
st.write(df)

# AllTrails Section
st.markdown("## For More Trail Recommendations")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    image_path = "alltrail.png"
    if os.path.exists(image_path):
        st.image(image_path, caption="AllTrails - Discover More Trails", use_column_width=True)
    else:
        st.warning("The 'alltrail.png' image was not found in the directory.")
    
    st.markdown(
        """
        <div style='text-align: center'>
            <a href='https://www.alltrails.com/?ref=header' target='_blank'>
                <button style='
                    background-color: #2E7D32;
                    color: white;
                    padding: 10px 24px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                    margin: 10px 0;
                    width: 100%;
                '>
                    Explore Creekside Trails on AllTrails
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

#Button 2 (Santa Clara County Parks Website)
    with col2:
        image_path = "Santa Clara County Parks.png"
        if os.path.exists(image_path):
            st.image(image_path, caption="Santa Clara County Parks", use_column_width=True)
        else:
            st.warning("The 'Santa Clara County Parks.png' image was not found in the directory.")
        
        st.markdown(
            """
            <div style='text-align: center'>
                <a href='https://data.sccgov.org/Environment/Santa-Clara-County-Parks/4uyd-siq9' target='_blank'>
                    <button style='
                        background-color: white;
                        color: black;
                        padding: 10px 24px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 16px;
                        margin: 10px 0;
                        width: 100%;
                    '>
                        Explore Creekside Trails on SCC Open Data
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

