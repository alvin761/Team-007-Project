# pages/3_trail_visualizer.py
import streamlit as st
import requests
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='')

def download_image(filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        st.error(f"Error downloading image from URL: {url}")

def filename_from_input(prompt):
    alphanum = "".join([char if char.isalnum() or char == " " else "" for char in prompt])
    words = alphanum.split()[:3]
    return "_".join(words)

def get_image(prompt, model="dall-e-2"):
    n = 2
    trail_prompt = f"creekside trail environment based on {prompt}"
    try:
        images = client.images.generate(
            prompt=trail_prompt,
            model=model,
            n=n,
            size="1024x1024"
        )
        filenames = []
        for i in range(n):
            filename = f"{filename_from_input(trail_prompt)}_{i + 1}.png"
            download_image(filename, images.data[i].url)
            filenames.append(filename)  
        return filenames 
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

st.title("🎨 Trail Visualizer")
st.write("Generate visual previews of different trail environments using AI.")

# User input for visualization
trail_description = st.text_input("Describe the trail environment you'd like to visualize:")
generate_button = st.button("Generate Trail Preview")

if generate_button and trail_description:
    with st.spinner("Generating trail previews..."):
        image_filenames = get_image(trail_description)
        if image_filenames:
            st.subheader("Generated Trail Previews:")
            for i, display_filename in enumerate(image_filenames):
                if os.path.exists(display_filename):
                    st.image(display_filename, 
                            caption=f"Preview {i + 1}: {trail_description}", 
                            use_column_width=True)
                else:
                    st.warning(f"Preview {i + 1} could not be generated.")
