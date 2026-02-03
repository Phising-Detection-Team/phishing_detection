"""  
    Model representing human mannually override the results
"""

from datetime import datetime
from . import db

class Override(db.Model):
    __tablename__ = 'Manual_Overrides'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    email_test_id = db.Column(
        db.Integer,
        db.ForeignKey('Emails.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Verdict result
    verdict = db.Column(
        db.String(20),
        nullable=False
    )

    # Who overrode this
    overridden_by = db.Column(
        db.String(100),
        nullable=True
    )

    # Reason for the manual override
    reason = db.Column(
        db.Text,
        nullable=True
    )

    # When was this created
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
            'verdict': self.verdict,
            'overridden_by': self.overridden_by,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
