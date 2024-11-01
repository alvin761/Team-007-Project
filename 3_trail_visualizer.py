# pages/3_trail_visualizer.py
import streamlit as st
import requests
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='OPEN_AI_KEY')

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

def get_image(prompt, category, model="dall-e-2"):
    n = 1  # Generate one image at a time
    
    # Create a more specific prompt based on the category
    if category == "Plant":
        base_prompt = "Detailed botanical illustration of"
    else:  # Animal
        base_prompt = "Detailed wildlife illustration of"
        
    full_prompt = f"{base_prompt} {prompt} in its natural habitat, photorealistic style"
    
    try:
        images = client.images.generate(
            prompt=full_prompt,
            model=model,
            n=n,
            size="1024x1024"
        )
        filenames = []
        for i in range(n):
            filename = f"{filename_from_input(prompt)}_{i + 1}.png"
            download_image(filename, images.data[i].url)
            filenames.append(filename)  
        return filenames 
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Page layout
st.title("Plant and Animal Visualizer")
st.write("Generate detailed visual illustrations of plants and animals using AI.")

# Add instructions
st.markdown("""
### How to use:
1. Select whether you want to visualize a plant or animal
2. Enter the name or description of the species
3. Click 'Generate' to create a detailed illustration
""")

# User input section
col1, col2 = st.columns([1, 2])

with col1:
    category = st.selectbox(
        "Choose category",
        ["Plant", "Animal"],
        help="Select whether you want to generate a plant or animal illustration"
    )

with col2:
    if category == "Plant":
        placeholder_text = "e.g., California Poppy"
    else:
        placeholder_text = "e.g., Red-Tailed Hawk"
        
    species_description = st.text_input(
        f"Describe the {category.lower()} you want to visualize",
        placeholder=placeholder_text
    )

generate_button = st.button("Generate Illustration", type="primary")

# Create a container for the image display
image_container = st.container()

if generate_button and species_description:
    with st.spinner(f"Generating {category.lower()} illustration..."):
        image_filenames = get_image(species_description, category)
        
        if image_filenames:
            with image_container:
                st.subheader(f"Generated {category} Illustration:")
                for i, display_filename in enumerate(image_filenames):
                    if os.path.exists(display_filename):
                        st.image(
                            display_filename, 
                            caption=f"{species_description}", 
                            use_column_width=True
                        )
                    else:
                        st.warning("Illustration could not be generated.")
                
                # Add information about the generated image
                st.markdown(f"""
                *This is an AI-generated illustration of {species_description}. 
                Please note that while the image aims to be accurate, it may not perfectly represent the actual species.*
                """)
