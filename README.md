# AI Writing Server cho Giáo dục

Đây là một ứng dụng web Flask đơn giản cho phép người dùng tạo nội dung văn bản, hình ảnh và khóa học sử dụng API của OpenAI.

## Tính năng

- Sinh văn bản sử dụng GPT-3.5-turbo
- Tạo hình ảnh sử dụng DALL-E 3
- Sinh nội dung khóa học với tiêu đề, mô tả và khung chương trình

## Yêu cầu

- Python 3.7+
- Flask
- OpenAI Python Library
- Pillow (PIL)

## Cài đặt

1. Clone repository này:
   ```
   git clone https://github.com/your-username/ai-writing-server.git
   cd ai-writing-server
   ```

2. Cài đặt các thư viện cần thiết:
   ```
   pip install flask openai pillow
   ```

3. Thiết lập biến môi trường cho API key của OpenAI:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Sử dụng

1. Chạy server:
   ```
   python server.py
   ```

2. Mở trình duyệt web và truy cập `http://localhost:5001`

3. Chọn loại nội dung bạn muốn tạo (văn bản, hình ảnh hoặc khóa học), nhập prompt và nhấn "Tạo"

## Cấu trúc dự án
ai-writing-server/
│
├── server.py
├── templates/
│ └── index.html
└── README.md


## Đóng góp

Nếu bạn muốn đóng góp cho dự án, vui lòng tạo một pull request hoặc mở một issue để thảo luận về những thay đổi bạn muốn thực hiện.

## Giấy phép

[MIT](https://choosealicense.com/licenses/mit/)