# PhysCode GPT API Server

API server sử dụng FastAPI và OpenAI để tạo nội dung văn bản, hình ảnh và khóa học.

## Quy trình của api_server.py

1. Khởi tạo ứng dụng FastAPI và cấu hình logging
2. Thiết lập rate limiting để bảo vệ API
3. Định nghĩa các model dữ liệu cho các request
4. Cung cấp các endpoint để:
   - Lấy và chỉnh sửa prompt cho text, image, và course
   - Tạo text, image, và course content dựa trên prompt
   - Tạo nội dung tùy chỉnh cho text, image, và course
5. Xử lý các request, gọi API OpenAI, và trả về kết quả
6. Xử lý lỗi và giới hạn tốc độ request

## Hướng dẫn sử dụng Docker image

Để chạy server sử dụng Docker, thực hiện lệnh sau:


docker run -p 8000:8000 -e OPENAI_API_KEY=your_api_key physcode-gpt


Thay thế `your_api_key` bằng API key OpenAI của bạn.

## Sử dụng API

1. Truy cập API documentation: 
   ```
   http://localhost:8000/docs
   ```

2. Các endpoint có sẵn:
   - Lấy prompt:
     - `/get_text_prompt`
     - `/get_image_prompt`
     - `/get_course_prompt`
   - Tạo nội dung:
     - `/generate_text`
     - `/generate_image`
     - `/generate_course`
   - Tạo nội dung tùy chỉnh:
     - `/generate_custom_text`
     - `/generate_custom_image`
     - `/generate_custom_course`

## Yêu cầu

- Docker
- OpenAI API key

## Lưu ý bảo mật

Đảm bảo bảo vệ API key của bạn và không chia sẻ nó công khai.

## Hỗ trợ

Nếu bạn gặp vấn đề hoặc có câu hỏi, vui lòng tạo issue trong repository này.

## Giấy phép

[MIT License](LICENSE)
