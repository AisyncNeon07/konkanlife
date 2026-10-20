import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from destinations.models import Destination, Gallery
from reviews.models import Review
from spots.models import Spots, Category as SpotCategory, Tag as SpotTag
from food.models import FoodItem, Category as FoodCategory, Tag as FoodTag
from users.models import Profile
from companion.models import (
    Partner, Itinerary, ItineraryDay, ItineraryStop,
    NFCTag, NFCTapEvent, EmergencyContact, FAQ, TravelTip, Announcement, AdminAuditLog
)

print("=== DATABASE INVENTORY AUDIT ===")
print(f"Destinations: {Destination.objects.count()}")
for d in Destination.objects.all():
    print(f"  - [{d.category}] {d.title} ({d.location_name}) | Verified: {d.is_verified} | GPS: {d.latitude}, {d.longitude}")

print(f"\nReviews: {Review.objects.count()}")
print(f"Spots Categories: {SpotCategory.objects.count()}, Spot Tags: {SpotTag.objects.count()}, Spots: {Spots.objects.count()}")
print(f"Food Categories: {FoodCategory.objects.count()}, Food Tags: {FoodTag.objects.count()}, Food Items: {FoodItem.objects.count()}")
for f in FoodItem.objects.all():
    print(f"  - {f.name} (Price: {f.price}, Rating: {f.rating})")

print(f"\nPartners: {Partner.objects.count()}")
for p in Partner.objects.all():
    print(f"  - [{p.partner_type}] {p.business_name} (Slug: {p.slug}) | Verified: {p.is_verified} | Featured: {p.is_featured}")

print(f"\nItineraries: {Itinerary.objects.count()}")
for itin in Itinerary.objects.all():
    days_count = itin.days.count()
    stops_count = ItineraryStop.objects.filter(day__itinerary=itin).count()
    print(f"  - {itin.title} ({itin.duration_days} Days, {days_count} Days configured, {stops_count} Stops)")

print(f"\nNFC Tags: {NFCTag.objects.count()}")
for tag in NFCTag.objects.all():
    print(f"  - [{tag.tag_uid}] {tag.title} -> Experience: {tag.target_experience}")

print(f"\nEmergency Contacts: {EmergencyContact.objects.count()}")
for ec in EmergencyContact.objects.all():
    print(f"  - [{ec.category}] {ec.name}: {ec.phone_number} (24x7: {ec.is_24x7})")

print(f"\nFAQs: {FAQ.objects.count()}")
for faq in FAQ.objects.all():
    print(f"  - [{faq.category}] {faq.question}")

print(f"\nTravel Tips: {TravelTip.objects.count()}")
for tip in TravelTip.objects.all():
    print(f"  - [{tip.category}] {tip.title} (Icon: {tip.icon})")

print(f"\nAnnouncements: {Announcement.objects.count()}")
for ann in Announcement.objects.all():
    print(f"  - [{ann.urgency_level}] {ann.title}")

print("\nAudit complete.")
