from app import create_app

# Tạo app ở module level
# Gunicorn (production) sẽ import: gunicorn run:app
# Nếu app nằm trong if __name__, Gunicorn không thấy
app = create_app()

if __name__ == '__main__':
    # Chỉ chạy khi gõ: python run.py
    # Gunicorn/import sẽ KHÔNG chạy block này
    app.run(
        debug=True,
        host='0.0.0.0',    # Cho phép truy cập từ máy khác (cần cho Docker)
        port=5000
    )
