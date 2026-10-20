import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.storage import default_storage
from django.conf import settings

def migrate_media():
    local_media_dir = Path(settings.BASE_DIR) / 'media'
    
    if not local_media_dir.exists():
        print("No local media directory found. Nothing to migrate.")
        return

    print(f"Scanning local media directory: {local_media_dir}\n")
    
    total_uploaded = 0
    total_skipped = 0
    total_failed = 0

    # Recursively find all files in the local media directory
    for root, dirs, files in os.walk(local_media_dir):
        for file in files:
            local_file_path = Path(root) / file
            
            # Get the relative path (e.g., 'spots/image.jpg' instead of 'C:/path/media/spots/image.jpg')
            relative_path = local_file_path.relative_to(local_media_dir)
            relative_path_str = str(relative_path).replace('\\', '/') # Ensure forward slashes for S3
            
            print(f"Processing: {relative_path_str}...")
            
            try:
                with open(local_file_path, 'rb') as f:
                    # Check if the file already exists in the Supabase bucket
                    if not default_storage.exists(relative_path_str):
                        default_storage.save(relative_path_str, f)
                        print(f"   ✅ Uploaded successfully.")
                        total_uploaded += 1
                    else:
                        print(f"   ⚠️ Skipped (Already exists in bucket).")
                        total_skipped += 1
            except Exception as e:
                print(f"   ❌ Failed to upload: {e}")
                total_failed += 1

    print("\n--- Migration Summary ---")
    print(f"Successfully uploaded: {total_uploaded}")
    print(f"Skipped (already exist): {total_skipped}")
    print(f"Failed to upload: {total_failed}")

if __name__ == '__main__':
    migrate_media()
