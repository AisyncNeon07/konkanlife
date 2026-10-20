import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_connections():
    print("Testing PostgreSQL Database Connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    print("\nTesting Supabase S3 Storage Connection...")
    try:
        file_path = default_storage.save('test_supabase_connection.txt', ContentFile(b'Connection successful!'))
        print(f"✅ S3 Storage connection successful! File saved at: {file_path}")
        
        # Clean up the test file
        default_storage.delete(file_path)
        print("✅ Test file cleaned up successfully.")
    except Exception as e:
        print(f"❌ S3 Storage connection failed: {e}")

if __name__ == "__main__":
    test_connections()
