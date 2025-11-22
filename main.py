"""
Main entry point for Google App Engine
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app, init_db

# Initialize database
# Multiple workers may try to create tables simultaneously, which is fine
# SQLite will handle concurrent table creation gracefully
import threading

_init_lock = threading.Lock()
_initialized = False

def ensure_db_initialized():
    global _initialized
    with _init_lock:
        if not _initialized:
            try:
                with app.app_context():
                    init_db()
                _initialized = True
                print("✓ Database initialized successfully")
            except Exception as e:
                # Log error but don't crash - tables might already exist
                print(f"Database initialization: {e}")
                _initialized = True  # Mark as attempted to avoid repeated failures

ensure_db_initialized()

# This is used by App Engine
if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
