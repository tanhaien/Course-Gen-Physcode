import os
import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import requests
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Initialize client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Call API to create chat completion
def generate_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",  # Or another model based on your needs
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to generate image
def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"An error occurred while generating the image: {e}")
        return None

# Function to generate course content
def generate_course_content(topic):
    prompt = f"""You are a course creation expert. Your task is to create specific and in-depth course content on the topic '{topic}' including:
    1. Title
    2. Description
    3. Detailed, in-depth course outline on the topic '{topic}' with its sections and lessons
    """
    return generate_response(prompt)

# Streamlit interface
st.title("Physcode-GPT Assistant for Education")

task = st.selectbox("Select content type", ["Generate Text", "Generate Image", "Generate Course Content"])

prompt = st.text_area("Enter your topic here")

if st.button("Generate"):
    with st.spinner("Processing... Please wait."):
        if task == "Generate Text":
            result = generate_response(prompt)
            st.text_area("Result:", value=result, height=300)
        elif task == "Generate Image":
            image_url = generate_image(prompt)
            if image_url:
                # Download image from URL
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                # Display image
                st.image(image, caption="Generated Image", use_column_width=True)
            else:
                st.error("Unable to generate image. Please try again.")
        elif task == "Generate Course Content":
            result = generate_course_content(prompt)
            st.text_area("Result:", value=result, height=300)

    st.success("Generation completed!")