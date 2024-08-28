from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field
from openai import OpenAI
import requests
from io import BytesIO
import base64
from dotenv import load_dotenv
import os
import logging

# Tải biến môi trường
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo FastAPI app
app = FastAPI()

# Khởi tạo Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Khởi tạo OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Định nghĩa các model dữ liệu
class TextRequest(BaseModel):
    prompt: str
    output_language: str

class ImageRequest(BaseModel):
    prompt: str

class CourseRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=100)
    output_language: str = Field(..., min_length=2, max_length=50)
    audience: str = Field(..., min_length=3, max_length=100)
    tone: str = Field(..., min_length=3, max_length=50)
    style: str = Field(..., min_length=3, max_length=50)

# Định nghĩa thêm các model dữ liệu mới
class PromptRequest(BaseModel):
    prompt: str

class ImagePromptRequest(BaseModel):
    prompt: str

class CoursePromptRequest(BaseModel):
    topic: str
    output_language: str
    audience: str
    tone: str
    style: str

# Thêm các model dữ liệu mới
class CustomTextRequest(BaseModel):
    custom_prompt: str

class CustomImageRequest(BaseModel):
    custom_prompt: str

class CustomCourseRequest(BaseModel):
    custom_prompt: str

# Cập nhật hàm generate_response
def generate_response(prompt, output_language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant. Always respond in {output_language}.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        response = chat_completion.choices[0].message.content
        logging.info(f"Generating response for prompt: {prompt}")
        return {"prompt": prompt, "response": response}
    except Exception as e:
        logging.error(f"Error in generate_response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
        return {"prompt": prompt, "image_url": image_url}
    except Exception as e:
        logging.error(f"An error occurred while generating the image: {e}")
        return None

def generate_course_content(topic, output_language, audience, tone, style):
    prompt = f"""You are a course creation expert. Your task is to create specific and in-depth course content on the topic '{topic}' including:
    1. Title
    2. Description
    3. Detailed, in-depth course outline on the topic '{topic}' with its sections and lessons

    Please consider the following parameters:
    - Audience: {audience}
    - Tone: {tone}
    - Style: {style}

    Tailor the content to match the specified audience, use the appropriate tone, and follow the given style.

    Please provide the entire response in {output_language}.
    """
    result = generate_response(prompt, output_language)
    if result:
        return {"topic": topic, "audience": audience, "tone": tone, "style": style, "output_language": output_language, "content": result["response"]}
    return None

# API endpoints mới để lấy và chỉnh sửa prompt
@app.post("/get_text_prompt")
async def get_text_prompt(request: TextRequest):
    return {"prompt": request.prompt, "output_language": request.output_language}

@app.post("/get_image_prompt")
async def get_image_prompt(request: ImageRequest):
    return {"prompt": request.prompt}

@app.post("/get_course_prompt")
async def get_course_prompt(request: CourseRequest):
    prompt = f"""You are a course creation expert. Your task is to create specific and in-depth course content on the topic '{request.topic}' including:
    1. Title
    2. Description
    3. Detailed, in-depth course outline on the topic '{request.topic}' with its sections and lessons
    Please provide the entire response in {request.output_language}.
    """
    return {"prompt": prompt, "topic": request.topic, "output_language": request.output_language}

# Cập nhật API endpoints để nhận prompt đã chỉnh sửa
@app.post("/generate_text")
@limiter.limit("10/minute")
async def api_generate_text(request: Request, text_request: TextRequest):
    result = generate_response(text_request.prompt, text_request.output_language)
    if result:
        return result
    raise HTTPException(status_code=500, detail="Không thể tạo văn bản")

@app.post("/generate_image")
@limiter.limit("5/minute")
async def api_generate_image(request: Request, image_request: ImageRequest):
    result = generate_image(image_request.prompt)
    if result:
        response = requests.get(result["image_url"])
        image = BytesIO(response.content)
        return {
            "prompt": result["prompt"],
            "image": base64.b64encode(image.getvalue()).decode()
        }
    raise HTTPException(status_code=500, detail="Không thể tạo hình ảnh")

@app.post("/generate_course")
@limiter.limit("2/minute")
async def api_generate_course(request: Request, course_request: CourseRequest):
    result = generate_course_content(
        course_request.topic,
        course_request.output_language,
        course_request.audience,
        course_request.tone,
        course_request.style
    )
    if result:
        return result
    raise HTTPException(status_code=500, detail="Không thể tạo nội dung khóa học")

# Thêm các endpoint mới
@app.post("/generate_custom_text")
async def api_generate_custom_text(request: CustomTextRequest):
    result = generate_response(request.custom_prompt, "")  # Để trống output_language
    if result:
        return result
    raise HTTPException(status_code=500, detail="Không thể tạo văn bản tùy chỉnh")

@app.post("/generate_custom_image")
async def api_generate_custom_image(request: CustomImageRequest):
    result = generate_image(request.custom_prompt)
    if result:
        response = requests.get(result["image_url"])
        image = BytesIO(response.content)
        return {
            "prompt": result["prompt"],
            "image": base64.b64encode(image.getvalue()).decode()
        }
    raise HTTPException(status_code=500, detail="Không thể tạo hình ảnh tùy chỉnh")

@app.post("/generate_custom_course")
async def api_generate_custom_course(request: CustomCourseRequest):
    result = generate_response(request.custom_prompt, "")  # Empty output_language
    if result:
        return {"prompt": request.custom_prompt, "content": result["response"]}
    raise HTTPException(status_code=500, detail="Không thể tạo nội dung khóa học tùy chỉnh")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)