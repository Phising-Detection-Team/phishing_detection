"""
    Representing API Calls
"""

from datetime import datetime
from . import db

class API(db.Model):
    __tablename__ ='API_calls'

    # Primary Key
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Foreign Key
    email_test_id = db.Column(
        db.Integer,
        db.ForeignKey('Emails.id', ondelete='CASCADE'),
        nullable=True,
        index=True                      
    )

    # Agent type (generator, detector, judge)
    agent_type = db.Column(db.String(20))

    # Model Name
    model_name = db.Column(db.String(50))

    # Token used
    token_used = db.Column(db.Integer)

    # Cost (USD)
    cost = db.Column(db.Float)

    # latency
    latency_ms = db.Column(db.Integer)

    # When was it created
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # METHODS
    def __repr__(self):
        """String representing for debugging"""
        # !!! NEEDED TO DESIGN OUTPUT !!!
        return f''
    
    def to_dict(self):
        """Converting to dictionary for JSON responses"""
        return {
            'id': self.id,
            'email_test_id': self.email_test_id,
            'agent_type': self.agent_type,
            'model_name': self.model_name,
            'token_used': self.token_used,
            'cost': self.cost,
            'latency_ms': self.latency_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }