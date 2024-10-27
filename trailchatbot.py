import requests
import os
from openai import OpenAI
import streamlit as st

# Initialize OpenAI client
#"Remove this comment to enable" client =  OpenAI(api_key='')

# Text generation feature and role for system
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

# Download images from generation
def download_image(filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        st.error(f"Error downloading image from URL: {url}")

# Generates filename from user input
def filename_from_input(prompt):
    alphanum = "".join([char if char.isalnum() or char == " " else "" for char in prompt])
    words = alphanum.split()[:3]
    return "_".join(words)

# Create an image from a prompt in DALL-E-2
def get_image(prompt, model="dall-e-2"):
    n = 2  # Number of images to generate
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

# Streamlit App
st.title("Creekside Trail Explorer")
st.write("Get personalized creekside trail recommendations based on your preferences and location. Optionally, view generated images for a visual impression of the trails.")

# Sidebar for chat input and image generating
with st.sidebar:
    st.header("Trail Explorer Chat")
    messages = st.container()

# Sidebar history storafge
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # User input
    prompt = st.chat_input("Describe the type of trail (location, difficulty):")

    # Checkbox for image generation
    generate_images = st.checkbox("Generate personalized image based on prompt description?", value=True)

    if prompt:
        # Append user prompt to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Generate text response
        text_response = get_completion(prompt)

        # Save assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": text_response})

        # Display chat history in the sidebar
        with messages:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    messages.chat_message("user").write(message["content"])
                else:
                    messages.chat_message("assistant").write(message["content"])

        # Display generated images in main area if selected
        if generate_images:
            image_filenames = get_image(prompt) 
            st.subheader("Generated Trail Images:")
            if image_filenames:
                for i, display_filename in enumerate(image_filenames):
                    if os.path.exists(display_filename):
                        st.image(display_filename, caption=f"Image {i + 1} based on: {prompt}", use_column_width=True)
                    else:
                        st.warning(f"Image file {display_filename} not found.")

# Link to AllTrails website and display the AllTrails logo image
st.markdown("## For More Creekside Trail Recommendations")
st.write("For more detailed trail information, visit the AllTrails website:")
st.markdown("[Explore Creekside Trails on AllTrails](https://www.alltrails.com/?ref=header)", unsafe_allow_html=True)

# Display AllTrails logo image
image_path = "alltrail.png"
if os.path.exists(image_path):
    st.image(image_path, caption="AllTrails - Discover More Trails", use_column_width=True)
else:
    st.warning("The 'alltrail.png' image was not found in the directory.")

