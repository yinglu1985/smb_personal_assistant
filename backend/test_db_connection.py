"""
Simple database connection test using direct PostgreSQL connection
"""

import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def test_direct_connection():
    """Test direct PostgreSQL connection"""
    print("Testing direct PostgreSQL connection to Cloud SQL...")
    print(f"Host: 34.27.96.189")
    print(f"Database: {os.environ.get('DB_NAME')}")
    print(f"User: {os.environ.get('DB_USER')}")

    try:
        conn = psycopg2.connect(
            host="34.27.96.189",
            port=5432,
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS')
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        print(f"\n✓ Successfully connected to Cloud SQL!")
        print(f"PostgreSQL version: {version}")

        # Test creating a simple table
        print("\nTesting table operations...")
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));")
        cursor.execute("INSERT INTO test_table (name) VALUES ('test');")
        cursor.execute("SELECT * FROM test_table;")
        result = cursor.fetchall()
        print(f"✓ Created test table and inserted data: {result}")

        # Clean up
        cursor.execute("DROP TABLE test_table;")
        conn.commit()
        print("✓ Cleaned up test table")

        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        return False

if __name__ == '__main__':
    test_direct_connection()
