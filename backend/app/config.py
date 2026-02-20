import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Insert key for production
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-for-production')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # Semantic Kernel / OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
