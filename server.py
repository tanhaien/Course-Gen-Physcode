import os
from openai import OpenAI
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import requests
from io import BytesIO

# Load biến môi trường từ file .env
load_dotenv()

# Khởi tạo client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Gọi API để tạo chat completion
def generate_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",  # Hoặc model khác tùy theo nhu cầu của bạn
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Sửa đổi hàm generate_image
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
        print(f"Đã xảy ra lỗi khi tạo hình ảnh: {e}")
        return None

# Hàm sinh nội dung khóa học
def generate_course_content(topic):
    prompt = f"""Bạn là chuyên gia tạo khóa học. Nhiệm vụ của bạn là tạo nội dung khóa học cụ thể và chuyên sâu về chủ đề '{topic}' bao gồm:
    1. Tiêu đề
    2. Mô tả
    3. Khung chương trình đầy đủ, chi tiết chuyên sâu về chủ đề '{topic}' (outline) với các section và lesson của nó
    """
    return generate_response(prompt)

import streamlit as st

# Giao diện Streamlit
st.title("Physcode-ChatGPT Assistant for Education")

task = st.selectbox("Chọn loại nội dung", ["Sinh văn bản", "Sinh hình ảnh", "Sinh nội dung khóa học"])

prompt = st.text_area("Nhập prompt của bạn ở đây")

if st.button("Tạo"):
    if task == "Sinh văn bản":
        result = generate_response(prompt)
        st.text_area("Kết quả:", value=result, height=300)
    elif task == "Sinh hình ảnh":
        image_url = generate_image(prompt)
        if image_url:
            # Tải hình ảnh từ URL
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            # Hiển thị hình ảnh
            st.image(image, caption="Hình ảnh được tạo", use_column_width=True)
        else:
            st.error("Không thể tạo hình ảnh. Vui lòng thử lại.")
    elif task == "Sinh nội dung khóa học":
        result = generate_course_content(prompt)
        st.text_area("Kết quả:", value=result, height=300)