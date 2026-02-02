"""
Log Model - stores system events and errors

Helps with:
- Debugging issues
- Monitoring system health
- Auditing operations
- Performance analysis
"""

from datetime import datetime
from . import db

class Log(db.Model):
    """ 
    Model representing a system log entry

    Stores events, errors, and important state changes
    """

    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)

    round_id = db.Column(
        db.Integer,
        db.ForeignKey('rounds.id', ondelete='CASCADE'),
        nullable=True,      # If NULL, this is a system-level log
        index=True          # Index for faster filtering
    )

    # Log level: info, warning, error, critical
    # Helps filter logs by severity
    level = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )

    # Log message
    message = db.Column(
        db.Text,
        nullable=False
    )

    # Additional context as JSON
    # Example: {
    #   "round_id": 5,
    #   "total_emails": 100,
    #   "error_type": "APIError",
    #   "stack_trace": "..."
    # }
    context = db.Column(
        db.JSON,
        nullable=True
    )

    # When this log was created
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True      # Index for date range queries
    )

    # METHODS
    def __repr__(self):
        """String representing for debugging"""
        return f'<Log {self.id} [{self.level}] {self.message[:30]}...>'
    
    def to_dict(self):
        """Converting to dictionary for JSON responses"""
        return {
            'id': self.id,
            'round_id': self.round_id,
            'level': self.level,
            'message': self.message,
            'context': self.context,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @staticmethod
    def create_log(level, message, round_id=None, context=None):
        """Helper method to create and save a log entry"""

        log = Log()
        
        log.level = level
        log.message = message
        log.context = context
        log.round_id = round_id

        db.session.add(log)
        db.session.commit()
        return log