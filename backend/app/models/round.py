"""
Model representing a competition round.

Each round consists off generating N emails, detecting them, 
judging the detector's accuracy.
"""

from datetime import datetime
from . import db

class Round(db.Model):
    __tablename__ = 'rounds'

    # Primary Column
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Status column - stores current state of the round
    status = db.Column(
        db.String(20),
        nullable=False
    )

    # Timestamp when round started
    started_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # Timestamp when round completed
    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # Total number of emails to process
    total_emails = db.Column(
        db.Integer,
        default=100     # Defaults to 100 if not specified
    )

    # Number of emails processed so far
    processed_emails = db.Column(
        db.Integer,
        default=0
    )

    # Final detector accuracy (percentage)
    detector_accuracy = db.Column(
        db.Float,
        nullable=True   # NULL until round completes
    )

    # Generator success rate (percentage)
    # how often generator fooled the detector
    generator_success_rate = db.Column(
        db.Float,
        nullable=True
    )

    # Total API cost for this round (USD)
    total_cost = db.Column(
        db.Float,
        default=0.0
    )

    # RELATIONSHIPS

    # One-to-many relationship with Email model
    # A round has many emails
    emails = db.relationship(
        'Email',                        # Related model name
        backref='round',                # Creates reverse reference: email.round
        lazy='dynamic',                 # Do not load all emails immediately (query when needed)
        cascade='all, delete-orphan'    # Delete emails when round is deleted
    )

    # One-to-many relationship with Log model
    # A round has many log entries
    logs = db.relationship(
        'Log',
        backref='round',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # METHODS
    def __repr__(self):
        """
        String representation of the object (for debugging)
        """
        return f'<Round {self.id} ({self.status})>'
    
    def to_dict(self):
        """
        Convert model to dictionary (for JSON responses)

        Returns:
            dict: Dictionary representation of the round
        
        Example:
            >>> round = Round.query.get(1)
            >>> round.to_dict()
            {
                'id': 1,
                'status': 'completed',
                'started_at': '2026-01-29T10:00:00',
                ...
            }
        """

        