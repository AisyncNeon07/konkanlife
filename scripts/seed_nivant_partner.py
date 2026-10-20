import os
import sys
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from companion.models import Partner, NFCTag

def run():
    print("Seeding Nivant Retreat Partner...")

    media_root = BASE_DIR / 'media'
    logos_dir = media_root / 'partners' / 'logos'
    covers_dir = media_root / 'partners' / 'covers'
    logos_dir.mkdir(parents=True, exist_ok=True)
    covers_dir.mkdir(parents=True, exist_ok=True)

    source_img_candidates = [
        Path("/mnt/c/Users/indranil sawant/.gemini/antigravity/brain/aed7a8d7-4f43-49c3-8529-199e80d901a5/.user_uploaded/media_1789147453674.png"),
        Path(r"C:\Users\indranil sawant\.gemini\antigravity\brain\aed7a8d7-4f43-49c3-8529-199e80d901a5\.user_uploaded\media_1789147453674.png"),
    ]
    
    source_img_path = None
    for p in source_img_candidates:
        if p.exists():
            source_img_path = p
            break

    logo_rel_path = 'partners/logos/nivant_retreat_logo.png'
    cover_rel_path = 'partners/covers/nivant_retreat_cover.png'

    if source_img_path:
        try:
            full_img = Image.open(source_img_path)
            w, h = full_img.size
            print(f"Original image size: {w}x{h}")
            
            # The circular profile avatar is in the left side
            # In media_1789147453674.png, avatar bounds:
            avatar_box = (
                int(w * 0.01),
                int(h * 0.08),
                int(w * 0.235),
                int(h * 0.55)
            )
            avatar_img = full_img.crop(avatar_box)
            avatar_dest = media_root / logo_rel_path
            avatar_img.save(avatar_dest)
            print(f"Saved cropped logo to {avatar_dest}")

            # Also save cover
            cover_dest = media_root / cover_rel_path
            avatar_img.save(cover_dest)
        except Exception as e:
            print(f"Error processing image: {e}")

    partner_defaults = {
        'business_name': 'Nivant Retreat',
        'partner_type': 'HOMESTAY',
        'short_tagline': 'Cozy Homestay near Ganeshgule | Peaceful, Private & Close to the Sea',
        'description': (
            "Experience the timeless charm of coastal Maharashtra with a relaxing stay, "
            "welcoming hospitality, and a serene atmosphere away from the hustle and bustle "
            "of city life. Whether you're visiting with family, friends, or loved ones, "
            "Nivant Retreat is an ideal place to unwind, explore nearby beaches and local "
            "attractions, and enjoy an authentic Konkan experience.\n\n"
            "✨ Stay Features:\n"
            "• Peaceful & Private Coastal Staycation in Ratnagiri\n"
            "• Beach just 4 km away (Close to pristine Ganeshgule Beach)\n"
            "• Authentic Kokani hospitality & Home-cooked meals\n"
            "• Scenic nature, coconut palms & tranquil surroundings"
        ),
        'address': 'Near Ganeshgule Beach, Ratnagiri, Maharashtra 415616',
        'phone': '+91 92707 34472',
        'whatsapp': '+91 92707 34472',
        'email': 'nivantretreat@gmail.com',
        'website': 'https://www.instagram.com/nivantretreat/',
        'google_maps_url': 'https://maps.google.com/?q=16.9080,73.2985',
        'latitude': 16.9080,
        'longitude': 73.2985,
        'is_verified': True,
        'is_featured': True,
        'is_active': True,
    }

    if (media_root / logo_rel_path).exists():
        partner_defaults['logo'] = logo_rel_path
    if (media_root / cover_rel_path).exists():
        partner_defaults['cover_image'] = cover_rel_path

    partner, created = Partner.objects.update_or_create(
        slug='nivant-retreat',
        defaults=partner_defaults
    )
    action = "Created" if created else "Updated"
    print(f"{action} Partner: {partner.business_name} (ID: {partner.id}, Slug: {partner.slug})")

    # NFC Smart Tag for Nivant Retreat
    tag_uid = 'RATNA-NIVANT-01'
    tag_defaults = {
        'title': 'Nivant Retreat - Guest Room NFC Concierge',
        'tag_type': 'HOTEL',
        'target_experience': 'PARTNER_PAGE',
        'assigned_partner': partner,
        'custom_welcome_title': 'Welcome to Nivant Retreat 🌴',
        'custom_welcome_message': (
            'Your peaceful coastal staycation in Ratnagiri. Beach is just 4 km away! '
            'Tap here for curated Konkan itineraries, food spots, and instant concierge assistance.'
        ),
        'is_active': True,
        'tap_count': 56,
        'unique_visitor_count': 42,
    }
    nfc_tag, tag_created = NFCTag.objects.update_or_create(
        tag_uid=tag_uid,
        defaults=tag_defaults
    )
    tag_action = "Created" if tag_created else "Updated"
    print(f"{tag_action} NFC Tag: {nfc_tag.tag_uid} -> {nfc_tag.title}")

if __name__ == '__main__':
    run()
