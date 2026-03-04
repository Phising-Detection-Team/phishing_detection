import os


class BaseConfig:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        os.environ.get('DEV_DATABASE_URL', os.environ.get('PROD_DATABASE_URL', 'sqlite:///app.db'))
    )
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CORS_ORIGINS = '*'
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """Testing configuration with in-memory SQLite."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    TESTING = False

    def __init__(self):
        # Ensure DATABASE_URL is set and uses PostgreSQL in production
        if 'DATABASE_URL' not in os.environ:
            raise ValueError('DATABASE_URL environment variable must be set in production')
        if self.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
            raise ValueError('SQLite is not allowed in production. Use PostgreSQL via DATABASE_URL.')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
=======
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(
        days=int(os.environ.get('SESSION_LIFETIME_DAYS', 7))
    )
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    
    # Application Settings
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///app.db'
    )


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = os.environ.get('TEST_SERVER_NAME', 'localhost')


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'PROD_DATABASE_URL',
        'postgresql://localhost/phishing_db'
    )
    
    # Ensure critical settings are set in production
    if not os.environ.get('SECRET_KEY') or os.environ.get('SECRET_KEY') == 'dev-secret-key-change-in-production':
        raise ValueError('SECRET_KEY must be set in .env for production')
    
    if not os.environ.get('PROD_DATABASE_URL'):
        raise ValueError('PROD_DATABASE_URL must be set in .env for production')


def get_config(env=None):
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name ('development', 'testing', 'production')
             Defaults to FLASK_ENV from .env or 'development'
    
    Returns:
        Configuration class
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }
    
    return configs.get(env, DevelopmentConfig)
>>>>>>> 255f55c (Finish up OpenAi Agentic SDK)import os


class BaseConfig:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        os.environ.get('DEV_DATABASE_URL', os.environ.get('PROD_DATABASE_URL', 'sqlite:///app.db'))
    )
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CORS_ORIGINS = '*'
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """Testing configuration with in-memory SQLite."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    TESTING = False

    def __init__(self):
        # Ensure DATABASE_URL is set and uses PostgreSQL in production
        if 'DATABASE_URL' not in os.environ:
            raise ValueError('DATABASE_URL environment variable must be set in production')
        if self.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
            raise ValueError('SQLite is not allowed in production. Use PostgreSQL via DATABASE_URL.')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
