from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .models import db


# Migrate ở ngoài create_app vì Alembic (migrations/env.py) cần truy cập global
# Giống pattern db = SQLAlchemy() trong models/__init__.py
migrate = Migrate()


def create_app(config_class=Config):
    """
    Application Factory Pattern.

    Tạo và cấu hình Flask app instance.

    Tại sao dùng factory?
    1. Tránh circular imports
    2. Dễ test (truyền TestConfig riêng)
    3. Có thể tạo nhiều instances

    Args:
        config_class: Class chứa cấu hình (default: Config)

    Returns:
        Flask app instance đã configured
    """

    # Tạo Flask app
    # __name__ = 'app', giúp Flask xác định thư mục gốc
    app = Flask(__name__)

    # Load config: đọc tất cả UPPERCASE attributes từ Config class
    # Sau dòng này: app.config['SECRET_KEY'], app.config['SQLALCHEMY_DATABASE_URI'], v.v.
    app.config.from_object(config_class)

    # Khởi tạo extensions
    # init_app() gắn extension vào app instance cụ thể
    db.init_app(app)
    migrate.init_app(app, db)

    # CORS: cho phép frontend (React) gọi API từ domain khác
    # Không có CORS → browser block request từ localhost:3000 → localhost:5000
    CORS(app)

    # Đăng ký routes
    register_blueprints(app)

    return app


def register_blueprints(app):
    """
    Đăng ký tất cả blueprints (route modules) vào app.

    Import trong function để tránh circular imports.
    """
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Sẽ thêm khi implement API endpoints (task 3, 4):
    # from app.routes.rounds import rounds_bp
    # from app.routes.emails import emails_bp
    # app.register_blueprint(rounds_bp, url_prefix='/api')
    # app.register_blueprint(emails_bp, url_prefix='/api')
