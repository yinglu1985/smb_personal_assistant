"""
Initialize Cloud SQL Database with Schema and Default Data
Uses direct PostgreSQL connection for local development
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

# Cloud SQL public IP (for local testing)
CLOUD_SQL_IP = "34.27.96.189"

def test_connection():
    """Test database connection"""
    print("\nTesting Cloud SQL connection...")

    try:
        conn = psycopg2.connect(
            host=CLOUD_SQL_IP,
            port=5432,
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS')
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        print(f"✓ Successfully connected to Cloud SQL!")
        print(f"  {version}")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def initialize_schema():
    """Initialize database schema"""
    print("\nInitializing database schema...")

    # Import Flask app and models
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Create a minimal Flask app for database initialization
    from flask import Flask
    from models.models import db

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Use direct PostgreSQL connection
    db_uri = f"postgresql://{ os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{CLOUD_SQL_IP}:5432/{os.environ.get('DB_NAME')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    with app.app_context():
        # Drop all tables (for clean start)
        print("  Dropping existing tables...")
        db.drop_all()

        # Create all tables
        print("  Creating tables...")
        db.create_all()
        print("  ✓ Database schema created successfully")

        # Initialize default data
        from models.models import Service, Therapist

        if Service.query.count() == 0:
            print("  Adding default services...")
            default_services = [
                Service(name='Swedish Massage', description='Relaxing full-body massage',
                       duration_minutes=60, price=80.0, category='massage'),
                Service(name='Deep Tissue Massage', description='Intensive therapeutic massage',
                       duration_minutes=60, price=95.0, category='massage'),
                Service(name='Hot Stone Massage', description='Massage with heated stones',
                       duration_minutes=90, price=120.0, category='massage'),
                Service(name='Aromatherapy Massage', description='Massage with essential oils',
                       duration_minutes=60, price=90.0, category='massage'),
                Service(name='Couples Massage', description='Side-by-side massage for two',
                       duration_minutes=60, price=160.0, category='massage'),
                Service(name='Prenatal Massage', description='Gentle massage for expectant mothers',
                       duration_minutes=60, price=85.0, category='massage'),
                Service(name='Signature Facial', description='Customized facial treatment',
                       duration_minutes=60, price=75.0, category='facial'),
                Service(name='Anti-Aging Facial', description='Advanced facial with anti-aging benefits',
                       duration_minutes=75, price=95.0, category='facial'),
                Service(name='Body Scrub', description='Exfoliating full-body treatment',
                       duration_minutes=45, price=65.0, category='body'),
                Service(name='Body Wrap', description='Detoxifying body wrap treatment',
                       duration_minutes=60, price=85.0, category='body'),
                Service(name='Manicure', description='Complete nail care for hands',
                       duration_minutes=30, price=30.0, category='nails'),
                Service(name='Pedicure', description='Complete nail care for feet',
                       duration_minutes=45, price=45.0, category='nails'),
                Service(name='Spa Day Package', description='Massage, facial, and body treatment',
                       duration_minutes=180, price=250.0, category='package'),
                Service(name='Couples Retreat', description='Couples massage and champagne',
                       duration_minutes=120, price=300.0, category='package'),
            ]
            db.session.bulk_save_objects(default_services)
            db.session.commit()
            print(f"  ✓ Added {len(default_services)} default services")

        if Therapist.query.count() == 0:
            print("  Adding default therapists...")
            default_therapists = [
                Therapist(name='Lily', specialty='Swedish & Deep Tissue Massage',
                         bio='Certified massage therapist with 10+ years experience'),
                Therapist(name='Wendy', specialty='Aromatherapy & Hot Stone',
                         bio='Specialist in therapeutic and relaxation techniques'),
                Therapist(name='Elaine', specialty='Facials & Body Treatments',
                         bio='Licensed esthetician with expertise in skincare'),
            ]
            db.session.bulk_save_objects(default_therapists)
            db.session.commit()
            print(f"  ✓ Added {len(default_therapists)} default therapists")

    print("✓ Schema initialization complete")

def main():
    """Main initialization workflow"""
    print("=" * 70)
    print("Cloud SQL Database Initialization")
    print("=" * 70)

    # Verify environment variables
    required_vars = ['DB_USER', 'DB_PASS', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"\n✗ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please ensure your .env file is configured correctly.")
        return

    print(f"\nConnection Details:")
    print(f"  Host: {CLOUD_SQL_IP}")
    print(f"  Database: {os.environ.get('DB_NAME')}")
    print(f"  User: {os.environ.get('DB_USER')}")

    # Test connection
    if not test_connection():
        return

    # Initialize schema
    try:
        initialize_schema()
    except Exception as e:
        print(f"\n✗ Schema initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n" + "=" * 70)
    print("Database initialization completed successfully!")
    print("=" * 70)
    print("\nYour Cloud SQL database is now ready with:")
    print("  - All required tables created")
    print("  - Default services populated")
    print("  - Default therapists populated")
    print("\nNext steps:")
    print("1. Test your application locally: python app.py")
    print("2. Deploy to App Engine: gcloud app deploy")

if __name__ == '__main__':
    main()
