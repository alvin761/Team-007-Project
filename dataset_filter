import os
import openai
import streamlit as st
import pandas as pd

# Echo API Key (Safety)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the CSV file with parks data (Make sure it uses the path "Parks.csv")
df = pd.read_csv("Parks.csv")

# Display the full dataset title and dropdown prompt
st.title("📊 Explore Parks")
st.write("Find Trails in Santa Clara County")

# Dropdown to select filter type
filter_type = st.selectbox("Choose how you want to find trails", ["Zip Code", "City", "Status"])

# User input based on selected filter type
filter_value = st.text_input(f"Enter the {filter_type} you are looking for:")

if filter_value:
    user_query = f"Find parks with {filter_type} = {filter_value}."

    with st.spinner("Processing your query with OpenAI..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that helps users explore a dataset of parks. The dataset includes columns such as Zip Code, City, and Status."},
                {"role": "user", "content": user_query}
            ]
        )
        
    # Filter the dataset locally based on filter type
    if filter_type == "Zip Code":
        filtered_df = df[df['Zip Code'].astype(str) == filter_value]  # Adjust column name here
    elif filter_type == "City":
        filtered_df = df[df['City'].str.contains(filter_value, case=False, na=False)]
    elif filter_type == "Status":
        filtered_df = df[df['Status'].str.contains(filter_value, case=False, na=False)]

    # Display the filtered DataFrame if any results match
    if not filtered_df.empty:
        st.write("### Filtered Parks Data")
        st.dataframe(filtered_df)
    else:
        st.write("No parks found with the specified filter.")
