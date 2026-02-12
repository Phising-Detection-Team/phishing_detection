"""
Simple test to verify create_app works and database initializes.
"""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    from app import create_app, db
    print("✅ Successfully imported create_app and db")
    
    # Create app with in-memory database
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    print("✅ Created Flask app successfully")
    
    with app.app_context():
        # Test database connection
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Quick model import test
        from app.models.email import Email
        from app.models.round import Round
        from app.models.log import Log
        from app.models.api import API
        from app.models.human_override import Override
        
        print("✅ All models imported successfully")
        print("\n✅ CREATE_APP INITIALIZATION COMPLETE")
        print("   Database: In-memory SQLite")
        print("   Tables: Email, Round, Log, API_calls, Manual_Overrides")
        print("   Status: Ready for operations")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
