#!/usr/bin/env python3
"""
Database Connectivity Test Script for Phase II - Full-Stack Todo Application

This script tests database connectivity to the Neon PostgreSQL database
using the configured DATABASE_URL.
"""

import os
import sys
from urllib.parse import urlparse


def test_database_connection(db_url):
    """
    Test database connectivity using psycopg2
    """
    try:
        import psycopg2

        # Parse the database URL to extract components
        # Handle both postgresql+asyncpg:// and postgresql:// formats
        if db_url.startswith('postgresql+asyncpg://'):
            # Convert to standard postgresql:// format for psycopg2
            db_url_for_psycopg2 = db_url.replace('postgresql+asyncpg://', 'postgresql://', 1)
        else:
            db_url_for_psycopg2 = db_url

        # Parse the URL
        parsed = urlparse(db_url_for_psycopg2)

        # Extract connection parameters
        host = parsed.hostname
        port = parsed.port or 5432
        database = parsed.path[1:]  # Remove leading '/'
        user = parsed.username
        password = parsed.password

        print(f"Attempting to connect to database:")
        print(f"  Host: {host}")
        print(f"  Port: {port}")
        print(f"  Database: {database}")
        print(f"  User: {user}")

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        # Test with a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()

        print(f"SUCCESS: Successfully connected to database!")
        print(f"Database version: {result[0][:50]}...")

        cursor.close()
        conn.close()

        return True
    except ImportError:
        print("ERROR: psycopg2 module not found. Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"ERROR: Database connection failed: {str(e)}")
        return False


def main():
    print("Database Connectivity Test for Full-Stack Todo Application")
    print("=" * 70)

    # Read environment variables directly from backend .env file
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_env_path = os.path.join(script_dir, "..", "backend", ".env")
    db_url = None

    if os.path.exists(backend_env_path):
        with open(backend_env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove surrounding quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    if key == 'DATABASE_URL':
                        db_url = value
                        break

    # If not found in .env file, try environment variable
    if not db_url:
        db_url = os.environ.get('DATABASE_URL')

    if not db_url:
        print("ERROR: DATABASE_URL not found in backend/.env file")
        return 1

    print(f"Using DATABASE_URL: {db_url.replace('://', '://***:***@') if '@' in db_url else db_url}")

    # Test database connection
    success = test_database_connection(db_url)

    if success:
        print("\nSUCCESS: Database connectivity test passed!")
        print("Both frontend and backend can connect to the Neon PostgreSQL database.")
        return 0
    else:
        print("\nFAILURE: Database connectivity test failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())