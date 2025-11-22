"""
Database Migration Script: SQLite to Cloud SQL PostgreSQL
Migrates schema and data from local SQLite database to Cloud SQL
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from google.cloud.sql.connector import Connector
import sqlalchemy

# Load environment variables
load_dotenv()

def get_sqlite_engine():
    """Create SQLite engine connection"""
    db_path = os.environ.get('DATABASE_PATH', 'spa.db')
    if not os.path.exists(db_path):
        # Try instance directory
        instance_path = os.path.join('instance', 'spa.db')
        if os.path.exists(instance_path):
            db_path = instance_path
        else:
            print(f"Warning: SQLite database not found at {db_path}")
            return None

    return create_engine(f'sqlite:///{db_path}')

def get_cloudsql_engine():
    """Create Cloud SQL PostgreSQL engine connection"""
    connector = Connector()

    def getconn():
        conn = connector.connect(
            os.environ.get('CLOUD_SQL_CONNECTION_NAME'),
            "pg8000",
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            db=os.environ.get('DB_NAME')
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return pool

def initialize_schema():
    """Initialize database schema using Flask-SQLAlchemy models"""
    print("Initializing database schema...")

    # Import Flask app and models
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models.models import db, Service, Therapist

    # Create a minimal Flask app for database initialization
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure Cloud SQL connection
    connector = Connector()

    def getconn():
        conn = connector.connect(
            os.environ.get('CLOUD_SQL_CONNECTION_NAME'),
            "pg8000",
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            db=os.environ.get('DB_NAME')
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool': pool}
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"

    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database schema created successfully")

        # Initialize default data
        if Service.query.count() == 0:
            print("Adding default services...")
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
            print(f"✓ Added {len(default_services)} default services")

        if Therapist.query.count() == 0:
            print("Adding default therapists...")
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
            print(f"✓ Added {len(default_therapists)} default therapists")

    connector.close()
    print("✓ Schema initialization complete")

def migrate_data():
    """Migrate data from SQLite to Cloud SQL"""
    print("\nMigrating data from SQLite to Cloud SQL...")

    sqlite_engine = get_sqlite_engine()
    if not sqlite_engine:
        print("No SQLite database found to migrate from. Skipping data migration.")
        return

    cloudsql_engine = get_cloudsql_engine()

    # Get list of tables
    inspector = inspect(sqlite_engine)
    tables = inspector.get_table_names()

    print(f"Found {len(tables)} tables to migrate: {', '.join(tables)}")

    # Tables to migrate (in order to respect foreign key constraints)
    migration_order = [
        'customers',
        'therapists',
        'services',
        'appointments',
        'newsletter_subscribers',
        'contact_messages'
    ]

    with sqlite_engine.connect() as sqlite_conn, cloudsql_engine.connect() as cloud_conn:
        for table in migration_order:
            if table not in tables:
                continue

            print(f"\nMigrating table: {table}")

            # Read data from SQLite
            result = sqlite_conn.execute(sqlalchemy.text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            columns = result.keys()

            if not rows:
                print(f"  No data to migrate in {table}")
                continue

            print(f"  Found {len(rows)} rows")

            # Clear existing data in Cloud SQL table
            cloud_conn.execute(sqlalchemy.text(f"DELETE FROM {table}"))
            cloud_conn.commit()

            # Insert data into Cloud SQL
            for row in rows:
                placeholders = ', '.join([f':{col}' for col in columns])
                insert_sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

                row_dict = dict(zip(columns, row))
                cloud_conn.execute(sqlalchemy.text(insert_sql), row_dict)

            cloud_conn.commit()
            print(f"  ✓ Migrated {len(rows)} rows to {table}")

    print("\n✓ Data migration complete!")

def test_connection():
    """Test Cloud SQL connection"""
    print("\nTesting Cloud SQL connection...")

    try:
        engine = get_cloudsql_engine()
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Successfully connected to Cloud SQL!")
            print(f"  PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def main():
    """Main migration workflow"""
    print("=" * 70)
    print("Cloud SQL Migration Script")
    print("=" * 70)

    # Verify environment variables
    required_vars = ['CLOUD_SQL_CONNECTION_NAME', 'DB_USER', 'DB_PASS', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"\n✗ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please ensure your .env file is configured correctly.")
        return

    print(f"\nConnection Details:")
    print(f"  Instance: {os.environ.get('CLOUD_SQL_CONNECTION_NAME')}")
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

    # Ask user if they want to migrate existing data
    migrate = input("\nDo you want to migrate existing data from SQLite? (y/n): ").lower()
    if migrate == 'y':
        try:
            migrate_data()
        except Exception as e:
            print(f"\n✗ Data migration failed: {e}")
            import traceback
            traceback.print_exc()
            return

    print("\n" + "=" * 70)
    print("Migration completed successfully!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Test your application locally to ensure everything works")
    print("2. Deploy to App Engine: gcloud app deploy")
    print("3. Monitor your application logs for any issues")

if __name__ == '__main__':
    main()
