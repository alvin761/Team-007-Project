import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='Your-API-KEY')  # Replace with your API key

def get_trail_summary(trail_data):
    """Generate an AI summary of trail data using OpenAI."""
    try:
        trail_info = "\n".join([f"{key}: {value}" for key, value in trail_data.items()])
        
        prompt = f"""Analyze the following trail information and provide a concise summary including:
        - Trail highlights
        - Key features
        - Best times to visit
        - Any notable information
        
        Trail Data:
        {trail_info}"""
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable park ranger providing helpful trail information."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

# Main app code
st.title("🏞️ Santa Clara County Trail Parks")

# Load the data
try:
    df = pd.read_csv("/Users/carlos/Downloads/Santa_Clara_County_Parks_20241029.csv")
    
    # Print the first few rows of the dataframe for debugging
    st.sidebar.write("### Data Preview:")
    st.sidebar.write(df.head())
    
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    st.stop()

# Find the city column (assuming it might have different names)
city_column = None
possible_city_columns = ['City', 'CITY', 'city', 'Location', 'LOCATION', 'location']
for col in df.columns:
    if col in possible_city_columns:
        city_column = col
        break

if city_column is None:
    st.error("Could not find city column. Available columns:")
    st.write(df.columns.tolist())
    st.stop()

# Add filters
st.sidebar.header("Trail Filters")

# Get unique cities and sort them
cities = sorted(df[city_column].dropna().unique())

# Allow multiple city selection
selected_cities = st.sidebar.multiselect("Select Cities", cities)

# Filter dataframe by selected cities
if selected_cities:
    filtered_df = df[df[city_column].isin(selected_cities)]
else:
    filtered_df = df  # Show all data if no cities are selected

# Display filtered trails
st.subheader("Filtered Trails")
st.dataframe(filtered_df)

# Trail selector
if not filtered_df.empty:
    st.subheader("Trail Details")
    
    # Find a suitable column for trail names
    trail_name_column = None
    possible_trail_columns = ['Park_Name', 'PARK_NAME', 'Trail_Name', 'TRAIL_NAME', 'Name', 'NAME']
    for col in df.columns:
        if col in possible_trail_columns:
            trail_name_column = col
            break
    
    if trail_name_column is None:
        trail_name_column = df.columns[0]  # Use first column as fallback
    
    trail_names = sorted(filtered_df[trail_name_column].unique())
    selected_trail = st.selectbox("Select a trail for detailed information", trail_names)
    
    if selected_trail:
        # Get the selected trail data
        trail_data = filtered_df[filtered_df[trail_name_column] == selected_trail].iloc[0].to_dict()
        
        # Create columns for layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### Trail Information")
            # Display all available information
            for field, value in trail_data.items():
                st.write(f"**{field.replace('_', ' ').title()}:** {value}")
        
        # Generate and display AI summary
        with col2:
            st.write("### AI Trail Summary")
            if st.button("Generate Trail Summary"):
                with st.spinner("Generating summary..."):
                    summary = get_trail_summary(trail_data)
                    st.write(summary)

# Try to identify latitude and longitude columns
lat_col = None
lon_col = None
for col in df.columns:
    col_lower = col.lower()
    if 'lat' in col_lower:
        lat_col = col
    elif 'lon' in col_lower or 'long' in col_lower:
        lon_col = col

# Add map visualization if coordinates are available
if lat_col and lon_col and not filtered_df.empty:
    st.subheader("Trail Locations")
    map_data = filtered_df[[lat_col, lon_col]].rename(columns={lat_col: 'lat', lon_col: 'lon'})
    st.map(map_data)

# Trail statistics
if not filtered_df.empty:
    st.subheader("Trail Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        total_trails = len(filtered_df)
        st.metric("Total Trails", total_trails)
        
        if selected_cities:
            st.metric("Selected Cities", len(selected_cities))
    
    with col2:
        # Display additional statistics if numerical columns exist
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            selected_metric = st.selectbox("Select metric to analyze", numeric_cols)
            avg_value = filtered_df[selected_metric].mean()
            st.metric(f"Average {selected_metric}", f"{avg_value:,.2f}")