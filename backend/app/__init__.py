"""
Flask application factory and database initialization.
"""

from flask import Flask
from .config import get_config
from .models import db


def create_app(config_env=None):
    """
    Create and configure Flask application.
    
    Args:
        config_env: Environment name ('development', 'testing', 'production')
                   Defaults to FLASK_ENV or 'development'
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_env)
    app.config.from_object(config)
    
    # Initialize database
    db.init_app(app)
    
    # Register database operations
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from app.models.email import Email
        from app.models.round import Round
        from app.models.log import Log
        from app.models.api import API
        from app.models.override import Override
        
        # Create tables if they don't exist
        db.create_all()
    
    return app
