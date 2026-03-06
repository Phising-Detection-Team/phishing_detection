"""
Database utilities for openai-agentic services.

Identical path/bootstrap logic to LLMs/utils/db_utils.py so it works from
the same project layout (project_root/openai-agentic/utils/db_utils.py).
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load .env from project root BEFORE importing any backend modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_file = os.path.join(project_root, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    print(f"⚠️  Warning: .env file not found at {env_file}")

# backend/app/__init__.py uses bare `from app.models import db` (absolute imports),
# so `backend/` must be on sys.path in addition to the project root.
backend_path = os.path.join(project_root, 'backend')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.app import create_app
from backend.app.models import db, API, Email, Round, Log

# Global Flask app instance — initialized once
_app = None
_app_context = None


def init_db() -> None:
    """Initialize Flask app and database connection. Call once at startup."""
    global _app, _app_context

    if _app is not None:
        return

    _app = create_app(config_name='development')
    _app_context = _app.app_context()
    _app_context.push()

    database_url = os.getenv('DATABASE_URL') or os.getenv('DEV_DATABASE_URL', '')
    host = database_url.split('@')[1] if '@' in database_url else database_url
    print(f"📦 Connecting to database: {host}")
    print("✅ Database connection initialized")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def save_log(
    level: str,
    message: str,
    round_id: int = None,
    context: dict = None,
) -> bool:
    if _app is None:
        return False
    try:
        Log.create_log(level=level, message=message, round_id=round_id, context=context)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# API call tracking
# ---------------------------------------------------------------------------

def save_api_call(
    round_id: int,
    agent_type: str,
    model_name: str,
    token_used: int,
    cost: float,
    latency_ms: int,
    email_id: int = None,
) -> bool:
    if _app is None:
        print("⚠️  Database not initialized. Call init_db() first.")
        return False

    try:
        if round_id is not None:
            if not db.session.get(Round, round_id):
                print(f"⚠️  Round {round_id} does not exist. Skipping API call logging.")
                return False

        api_record = API(
            email_id=email_id,
            round_id=round_id,
            agent_type=agent_type,
            model_name=model_name,
            token_used=token_used,
            cost=cost,
            latency_ms=latency_ms,
        )
        db.session.add(api_record)
        db.session.commit()
        return True

    except Exception as e:
        msg = f"Failed to log API call: {e}"
        print(f"❌ {msg}")
        save_log('error', msg, round_id=round_id)
        db.session.rollback()
        return False


# ---------------------------------------------------------------------------
# Email persistence
# ---------------------------------------------------------------------------

def save_email(round_id: int, email_result: dict, processing_time: float = None) -> int | None:
    """Save a generated + detected email to the database.

    Expected keys in email_result (mapped from openai-agentic output):
        generated_content, generated_subject, generated_body,
        is_phishing, generated_email_metadata,
        detection_verdict, detection_risk_score, detection_confidence,
        detection_reasoning, cost
    """
    if _app is None:
        print("⚠️  Database not initialized. Call init_db() first.")
        return None

    try:
        generated_content   = email_result.get('generated_content')
        generated_prompt    = email_result.get('generated_prompt')
        generated_subject   = email_result.get('generated_subject')
        generated_body      = email_result.get('generated_body')
        is_phishing         = email_result.get('is_phishing', True)
        generated_metadata  = email_result.get('generated_email_metadata', {})
        generator_latency   = email_result.get('generated_latency_ms')

        # Normalise verdict → 'phishing' | 'legitimate'
        raw_verdict = str(email_result.get('detection_verdict', '')).upper()
        if any(w in raw_verdict for w in ('SCAM', 'PHISHING', 'SUSPICIOUS', 'FRAUD', 'MALICIOUS')):
            detector_verdict = 'phishing'
        else:
            detector_verdict = 'legitimate'

        detector_risk_score  = email_result.get('detection_risk_score')
        detector_confidence  = email_result.get('detection_confidence')
        detector_reasoning   = email_result.get('detection_reasoning')
        detector_latency     = email_result.get('detector_latency_ms')

        if detector_confidence is not None:
            detector_confidence = max(0.0, min(1.0, float(detector_confidence)))
        if detector_risk_score is not None:
            detector_risk_score = max(0.0, min(1.0, float(detector_risk_score)))

        cost = email_result.get('cost', 0.0)

        email_record = Email(
            round_id=round_id,
            generated_content=generated_content,
            generated_prompt=generated_prompt,
            generated_subject=generated_subject,
            generated_body=generated_body,
            is_phishing=is_phishing,
            generated_email_metadata=generated_metadata,
            generator_latency_ms=generator_latency,
            detector_verdict=detector_verdict,
            detector_risk_score=detector_risk_score,
            detector_confidence=detector_confidence,
            detector_reasoning=detector_reasoning,
            detector_latency_ms=detector_latency,
            processing_time=processing_time,
            cost=cost,
            created_at=datetime.utcnow(),
        )

        db.session.add(email_record)
        db.session.commit()
        print(f"✅ Email saved with ID: {email_record.id}")
        return email_record.id

    except Exception as e:
        msg = f"Failed to save email: {e}"
        print(f"❌ {msg}")
        save_log('error', msg, round_id=round_id)
        db.session.rollback()
        return None


# ---------------------------------------------------------------------------
# Round lifecycle
# ---------------------------------------------------------------------------

def create_round(total_emails: int, status: str = 'running') -> int | None:
    if _app is None:
        print("⚠️  Database not initialized. Call init_db() first.")
        return None

    try:
        round_record = Round(
            status=status,
            total_emails=total_emails,
            processed_emails=0,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
        )
        db.session.add(round_record)
        db.session.flush()
        db.session.commit()
        print(f"✅ Round created with ID: {round_record.id}")
        return round_record.id

    except Exception as e:
        msg = f"Failed to create round: {e}"
        print(f"❌ {msg}")
        save_log('error', msg)
        db.session.rollback()
        return None


def update_round(
    round_id: int,
    status: str = None,
    processed_emails: int = None,
    detector_accuracy: float = None,
    generator_success_rate: float = None,
    processing_time: int = None,
    total_cost: float = None,
) -> bool:
    if _app is None:
        print("⚠️  Database not initialized. Call init_db() first.")
        return False

    try:
        round_record = db.session.get(Round, round_id)
        if not round_record:
            print(f"❌ Round {round_id} not found")
            return False

        if status is not None:
            round_record.status = status
        if processed_emails is not None:
            round_record.processed_emails = processed_emails
        if detector_accuracy is not None:
            round_record.detector_accuracy = detector_accuracy
        if generator_success_rate is not None:
            round_record.generator_success_rate = generator_success_rate
        if processing_time is not None:
            round_record.processing_time = processing_time
        if total_cost is not None:
            round_record.total_cost = total_cost
        if status == 'completed':
            round_record.completed_at = datetime.utcnow()

        db.session.commit()
        print(f"✅ Round {round_id} updated")
        return True

    except Exception as e:
        msg = f"Failed to update round {round_id}: {e}"
        print(f"❌ {msg}")
        save_log('error', msg, round_id=round_id)
        db.session.rollback()
        return False
