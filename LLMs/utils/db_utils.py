"""
Database utilities for LLM services.

Provides database connection and logging functionality for API calls.
"""

import os
from flask import Flask
from backend.app.models import db, API
from sqlalchemy.orm import scoped_session


# Global Flask app and session instances
_app = None
_db_session = None


def init_db() -> None:
    """Initialize Flask app and database connection.

    This should be called once at application startup.
    Reads DATABASE_URL from environment variables.
    """
    global _app, _db_session

    if _app is not None:
        return  # Already initialized

    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠️  Warning: DATABASE_URL not set. Database logging will fail.")
        print("   Set it in your .env file:")
        print("   DATABASE_URL=postgresql://user:password@localhost:5432/phishing_detection")
        return

    # Create minimal Flask app for database access
    _app = Flask(__name__)
    _app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }

    # Initialize SQLAlchemy with the app
    db.init_app(_app)

    # Create application context
    _app.app_context().push()

    print(f"✅ Database connection initialized")


def get_db():
    """Get the database instance.

    Returns:
        SQLAlchemy database instance
    """
    return db


def log_api_call(
    round_id: int,
    agent_type: str,
    model_name: str,
    token_used: int,
    cost: float,
    latency_ms: int,
    email_id: int = None
) -> bool:
    """Log an API call to the database.

    Args:
        round_id: ID of the round this API call belongs to
        agent_type: Type of agent (generator, detector, judge)
        model_name: Name of the model used
        token_used: Total tokens used in the API call
        cost: Cost in USD
        latency_ms: Latency in milliseconds
        email_id: Optional email ID if associated with specific email

    Returns:
        bool: True if successful, False otherwise
    """
    if _app is None:
        print("⚠️  Database not initialized. Call init_db() first.")
        return False

    try:
        # Create API record
        api_record = API(
            email_id=email_id,
            round_id=round_id,
            agent_type=agent_type,
            model_name=model_name,
            token_used=token_used,
            cost=cost,
            latency_ms=latency_ms
        )

        # Add and commit
        db.session.add(api_record)
        db.session.commit()

        return True

    except Exception as e:
        print(f"❌ Failed to log API call to database: {e}")
        db.session.rollback()
        return False
