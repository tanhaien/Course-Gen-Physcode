import os
from openai import OpenAI
from flask import Flask, render_template, request
from PIL import Image
import io
import base64

# Khởi tạo client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)

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

# Hàm sinh hình ảnh
def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="512x512",
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        task = request.form['task']
        
        if task == 'text':
            result = generate_response(prompt)
        elif task == 'image':
            image_url = generate_image(prompt)
            result = f'<img src="{image_url}" alt="Generated Image">'
        elif task == 'course':
            result = generate_course_content(prompt)
        
        return render_template('index.html', result=result, show_result=True)
    
    return render_template('index.html', show_result=False)

if __name__ == '__main__':
    app.run(debug=True, port=5001)