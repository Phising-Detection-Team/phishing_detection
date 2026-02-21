from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .models import db
from .errors import register_error_handlers
from .services.kernel_service import KernelService


# Defined outside create_app so Alembic/Gunicorn can access them globally
migrate = Migrate()
kernel_service = KernelService()


def create_app(config_class=Config):
    """
    Application Factory Pattern.

    Creates and configures a Flask app instance.

    Why use a factory?
    1. Avoids circular imports
    2. Easier to test (pass a different config class)
    3. Allows multiple app instances

    Args:
        config_class: Configuration class to use (default: Config)

    Returns:
        Fully configured Flask app instance
    """

    app = Flask(__name__)

    # Load all UPPERCASE attributes from the Config class into app.config
    app.config.from_object(config_class)

    # Initialize extensions - init_app() binds each extension to this app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # CORS: allow frontend (React) to call API from a different origin
    CORS(app)

    # Error handlers: return JSON instead of HTML for 400, 404, 500
    register_error_handlers(app)

    # Semantic Kernel: initialize AI orchestration (skipped if no API key)
    kernel_service.init_app(app)

    # Register route blueprints
    register_blueprints(app)

    return app


def register_blueprints(app):
    """
    Register all blueprints (route modules) with the app.

    Imports are inside the function to avoid circular imports.
    """
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Will be added when implementing API endpoints:
    # from app.routes.rounds import rounds_bp
    # from app.routes.emails import emails_bp
    # app.register_blueprint(rounds_bp, url_prefix='/api')
    # app.register_blueprint(emails_bp, url_prefix='/api')
