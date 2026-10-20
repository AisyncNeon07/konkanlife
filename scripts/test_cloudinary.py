import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

print("Cloudinary Storage Settings:")
print("  Cloud Name:", settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'))
print("  API Key:", settings.CLOUDINARY_STORAGE.get('API_KEY')[:6] + "...")

try:
    ping = cloudinary.api.ping()
    print("Cloudinary Ping Response:", ping)
    print("SUCCESS: Cloudinary is connected and authenticated successfully!")
except Exception as e:
    print("Cloudinary Connection Error:", e)
