import streamlit as st
import requests
import openai
import os
import pandas as pd
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import st_folium
import googlemaps
import logging 

# Configure OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Configure page
st.set_page_config(
    page_title="Trail Finder - Creekside Trail Explorer",
    page_icon="🏝️",
    layout="wide"
)

# Custom CSS matching main page theme
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
        
        .trail-info {
            color: black !important;
            margin-bottom: 0.5rem;
        }
        
        .stButton>button {
            border-radius: 20px;
            background-color: #3498db;
            color: white;
        }
        
        .stButton>button:hover {
            background-color: #2980b9;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Google Maps client
gmaps = googlemaps.Client(key='key') # Echoing the Google Maps API key like OpenAI API key # Replace with your Google Maps API key

def format_summary(text):
    """
    Format the summary text with spaces between topics.
    """
    # Split the text into sections
    sections = text.split('- ')
    formatted_parts = []
    
    for section in sections:
        if not section.strip():
            continue
            
        # Split section into title and content
        parts = section.split(':', 1)
        if len(parts) == 2:
            title, content = parts
            # Format each section with a newline between topics
            formatted_parts.append(f"{title.strip()}: {content.strip()}")
    
    # Join with double newlines to create space between topics
    return '\n\n'.join(formatted_parts)

def get_trail_summary(trail_data):
    try:
        # Initialize the client
        client = openai()
        
        # Format trail info
        trail_info = "\n".join([f"{key}: {value}" for key, value in trail_data.items()])
        
        # System message to set the context
        system_msg = "You are a knowledgeable park ranger. Provide a concise summary of the trail information."
        
        # User message with the trail data and request
        user_msg = f"""Analyze the following trail information and provide a structured summary with these sections:
        - Trail Highlights
        - Key Features
        - Best Times to Visit
        - Notable Information
        
        Present each section's content without bullet points or dashes.
        
        Trail Data:
        {trail_info}"""

        try:
            # Make the API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Get and format the response
            raw_summary = str(response.choices[0].message.content)
            formatted_summary = format_summary(raw_summary)
            
            return formatted_summary
                
        except Exception as api_error:
            return f"API Error: {str(api_error)}"
            
    except Exception as e:
        return f"Error in get_trail_summary: {str(e)}"

# Main header
st.markdown("""
    <div class="main-header">
        <h1>🏝️ Santa Clara County Trail Parks</h1>
        <p style='font-size: 1.2em; color: #34495e;'>
            Discover and explore local trails in Santa Clara County
        </p>
    </div>
""", unsafe_allow_html=True)

# Load data
try:
    df = pd.read_csv("Parks.csv")
    
    # Ensure consistent column naming
    df.columns = df.columns.str.strip().str.lower()
    
    st.subheader("Data Preview")
    st.dataframe(df.head(), height=200)
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

# Sidebar styling
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h2 style='color: black;'>🔍 Trail Filters</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Find city column
    city_column = next((col for col in df.columns if col.lower() in ['city', 'location']), None)
    if city_column:
        cities = sorted(df[city_column].dropna().unique())
        selected_cities = st.multiselect("Select Cities", cities)
    
    st.markdown("<h3 style='color: black;'>Data Preview:</h3>", unsafe_allow_html=True)
    st.dataframe(df.head(), height=200)

# Filter dataframe
filtered_df = df[df[city_column].isin(selected_cities)] if selected_cities else df

# Main content
st.markdown("<h3 style='color: black;'>Filtered Trails</h3>", unsafe_allow_html=True)
st.dataframe(filtered_df)

if not filtered_df.empty:
    st.markdown("<h3 style='color: black;'>Trail Details</h3>", unsafe_allow_html=True)
    
    # Trail selector
    trail_name_column = next((col for col in df.columns 
                            if col.lower() in ['park_name', 'trail_name', 'name']), df.columns[0])
    trail_names = sorted(filtered_df[trail_name_column].unique())
    selected_trail = st.selectbox("Select a trail for detailed information", trail_names)
    
    if selected_trail:
        trail_data = filtered_df[filtered_df[trail_name_column] == selected_trail].iloc[0].to_dict()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("<h4 style='color: black;'>Trail Information</h4>", unsafe_allow_html=True)
            for field, value in trail_data.items():
                st.markdown(f"""
                    <div class="trail-info">
                        <strong>{field.replace('_', ' ').title()}:</strong> {value}
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h4 style='color: black;'>AI Trail Summary</h4>", unsafe_allow_html=True)
            if st.button("Generate Trail Summary"):
                with st.spinner("Generating summary..."):
                    summary = get_trail_summary(trail_data)
                    st.markdown(f'<div class="trail-info">{summary}</div>', unsafe_allow_html=True)

    # Map visualization using Google Maps API
    if 'address' in trail_data and 'zip code' in trail_data:
        selected_address = f"{trail_data['address']}, {trail_data['city']}, {trail_data['zip code']}"
        geocode_result = gmaps.geocode(selected_address)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
        else:
            st.warning(f"Could not geocode address: {selected_address}")
            lat, lng = 37.7749, -122.4194  # Default to San Francisco coordinates
    else:
        st.warning("Selected trail does not have a valid address or zip code.")
        lat, lng = 37.7749, -122.4194  # Default to San Francisco coordinates

    # Create Folium map with hardcoded coordinates or geocoded coordinates
    m = folium.Map(location=[lat, lng], zoom_start=15, 
                   tiles="OpenStreetMap", 
                   attr="Map tiles by OpenStreetMap contributors.")
    folium.Marker([lat, lng], popup="Test Location").add_to(m)

    # Display the map in Streamlit
    st_folium(m, width="100%", height=500)

# Trail statistics
st.markdown("<h3 style='color: black;'>Trail Statistics</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='color: black;'>
            <h4 style='color: black;'>Overview</h4>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div style='color: black; font-size: 1.1em;'>
            <p><strong>Total Trails:</strong> {len(filtered_df)}</p>
            {f"<p><strong>Selected Cities:</strong> {len(selected_cities)}</p>" if selected_cities else ""}
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='color: black;'>Analytics</h4>", unsafe_allow_html=True)
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        selected_metric = st.selectbox("Select metric to analyze", numeric_cols, 
            key="metric_selector")
        avg_value = filtered_df[selected_metric].mean()
        st.markdown(f"""
            <div style='color: black; font-size: 1.1em;'>
                <p><strong>Average {selected_metric.replace('_', ' ').title()}:</strong> {avg_value:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)
