import os
import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import requests
from io import BytesIO
import streamlit as st
     
api_key = st.secrets["OPENAI_API_KEY"]

# Initialize client
client = OpenAI(
    api_key=api_key
)

# Thêm danh sách ngôn ngữ đầu ra
output_languages = ["Tiếng Việt", "English", "Français", "Deutsch", "Español"]

# Call API to create chat completion
def generate_response(prompt, output_language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"Respond in {output_language}.",
                },
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
        enhanced_prompt = f"{prompt}. Do not include any text or words in the image."
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
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
def generate_course_content(topic, output_language):
    prompt = f"""You are a course creation expert. Your task is to create specific and in-depth course content on the topic '{topic}' including:
    1. Title
    2. Description
    3. Detailed, in-depth course outline on the topic '{topic}' with its sections and lessons
    """
    return generate_response(prompt, output_language)

# Streamlit interface
st.title("Physcode-GPT Assistant for Education")

task = st.selectbox("Select content type", ["Generate Text", "Generate Image", "Generate Course Content"])

prompt = st.text_area("Enter your topic here")

output_language = st.selectbox("Chọn ngôn ngữ đầu ra", output_languages)

num_variants = st.slider("Số lượng biến thể", min_value=1, max_value=5, value=1)

if st.button("Generate"):
    with st.spinner("Processing... Please wait."):
        if task == "Generate Text":
            for i in range(num_variants):
                result = generate_response(prompt, output_language)
                st.text_area(f"Kết quả {i+1}:", value=result, height=300)
        elif task == "Generate Image":
            for i in range(num_variants):
                image_url = generate_image(prompt)
                if image_url:
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption=f"Hình ảnh được tạo {i+1}", use_column_width=True)
                else:
                    st.error("Không thể tạo hình ảnh. Vui lòng thử lại.")
        elif task == "Generate Course Content":
            for i in range(num_variants):
                result = generate_course_content(prompt, output_language)
                st.text_area(f"Kết quả {i+1}:", value=result, height=300)

    st.success("Generation completed!")