import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from destinations.models import Destination
from companion.models import Itinerary, ItineraryDay, ItineraryStop, NFCTag, Partner

User = get_user_model()

def run_verification():
    print("=== Starting Automated Mobile Routes Verification ===")
    
    # 1. Setup staff user
    staff_user, created = User.objects.get_or_create(
        username="staff_tester",
        defaults={"is_staff": True, "is_superuser": True, "email": "staff@test.com"}
    )
    if not staff_user.is_staff:
        staff_user.is_staff = True
        staff_user.is_superuser = True
        staff_user.save()
    staff_user.set_password("pass1234")
    staff_user.save()

    # 2. Setup mock data if needed
    dest = Destination.objects.first()
    if not dest:
        dest = Destination.objects.create(
            title="Ganpatipule Beach & Temple",
            slug="ganpatipule-beach-temple",
            category="Beach",
            description="Golden white sands and sacred Ganesha temple by the sea.",
            location_name="Ganpatipule, Ratnagiri",
            latitude=17.1456,
            longitude=73.2689,
            is_verified=True
        )

    itin = Itinerary.objects.first()
    if not itin:
        itin = Itinerary.objects.create(
            title="3-Day Coastal Heritage Trail",
            slug="3-day-coastal-heritage-trail",
            tagline="Ancient sea forts and pristine beaches",
            description="Explore the best of Ratnagiri in 3 unforgettable days.",
            duration_days=3,
            difficulty="MODERATE",
            season="WINTER",
            audience="FAMILY",
            is_active=True
        )
        day1 = ItineraryDay.objects.create(itinerary=itin, day_number=1, title="Arrival & Jaigad Fort")
        ItineraryStop.objects.create(
            day=day1, order_index=1, title="Jaigad Fort Exploration",
            stop_type="DESTINATION", destination=dest, duration_minutes=90
        )

    partner = Partner.objects.first()
    if not partner:
        partner = Partner.objects.create(
            business_name="Ocean View Beach Resort",
            partner_type="HOTEL",
            address="Ganpatipule Main Road, Ratnagiri",
            phone="+91 98765 43210",
            is_verified=True
        )

    tag = NFCTag.objects.first()
    if not tag:
        tag = NFCTag.objects.create(
            tag_uid="HOTEL-OCEAN-001",
            title="Ocean View Lobby NFC Kiosk",
            tag_type="EXPERIENCE",
            target_experience="HOTEL_CHECKIN",
            assigned_partner=partner,
            assigned_destination=dest,
            is_active=True
        )

    client = Client()
    
    # Public Routes to test
    public_urls = [
        ('/', 'Home'),
        ('/destinations/', 'Destinations List'),
        (f'/destinations/{dest.slug}/', 'Destination Detail'),
        ('/companion/', 'Companion Hub'),
        ('/itineraries/', 'Itineraries List'),
        (f'/itineraries/{itin.slug}/', 'Itinerary Detail'),
        ('/near-me/', 'Near Me'),
        ('/my-trip/', 'My Trip Planner'),
        ('/emergency/', 'Emergency Hub'),
        ('/food-trail/', 'Food Trail'),
        ('/partners/', 'Partner Directory'),
        (f'/t/{tag.tag_uid}/', 'NFC Tap Fallback Gateway'),
        (f'/t/{tag.tag_uid}/qr/', 'NFC QR View Gateway'),
        ('/accounts/login/', 'Login Page'),
        ('/accounts/register/', 'Register Page'),
    ]

    print("\n--- Testing Public Routes ---")
    all_passed = True
    for url, name in public_urls:
        response = client.get(url, follow=True)
        content = response.content.decode('utf-8', errors='ignore')
        if response.status_code == 200:
            # Check for mobile indicators
            has_viewport = 'name="viewport"' in content
            print(f"[PASS] 200 OK | {name:<25} | {url:<35} | Viewport: {'YES' if has_viewport else 'NO'}")
        else:
            print(f"[FAIL] {response.status_code} | {name:<25} | {url:<35}")
            all_passed = False

    # Login staff user for /ops/
    client.force_login(staff_user)

    # Ops Routes to test
    ops_urls = [
        ('/ops/', 'Ops Dashboard'),
        ('/ops/places/', 'Ops Places List'),
        ('/ops/places/new/', 'Ops Place Create'),
        (f'/ops/places/{dest.pk}/edit/', 'Ops Place Edit'),
        ('/ops/itineraries/', 'Ops Itineraries List'),
        ('/ops/itineraries/new/', 'Ops Itinerary Create'),
        (f'/ops/itineraries/{itin.pk}/builder/', 'Ops Itinerary Builder'),
        ('/ops/nfc/', 'Ops NFC List'),
        ('/ops/nfc/new/', 'Ops NFC Create'),
        (f'/ops/nfc/{tag.pk}/', 'Ops NFC Detail Router'),
        ('/ops/nfc/bulk/', 'Ops NFC Bulk Generator'),
        ('/ops/nfc/print/', 'Ops NFC Print Sheet'),
        ('/ops/partners/', 'Ops Partners List'),
        ('/ops/partners/new/', 'Ops Partner Create'),
        (f'/ops/partners/{partner.pk}/edit/', 'Ops Partner Edit'),
        ('/ops/content/', 'Ops Content CMS'),
        ('/ops/media/', 'Ops Media Asset Hub'),
        ('/ops/analytics/', 'Ops Analytics Center'),
        ('/ops/system/', 'Ops System Audit Trail'),
        ('/ops/search/?q=Beach', 'Ops Search Query'),
    ]

    print("\n--- Testing /ops/ Operations & Control Center Routes ---")
    for url, name in ops_urls:
        response = client.get(url)
        content = response.content.decode('utf-8', errors='ignore')
        if response.status_code == 200:
            has_bottom_bar = 'ops-bottom-bar' in content
            has_drawer = 'ops-mobile-drawer' in content
            print(f"[PASS] 200 OK | {name:<25} | {url:<35} | BottomBar: {'YES' if has_bottom_bar else 'N/A'} | Drawer: {'YES' if has_drawer else 'N/A'}")
        else:
            print(f"[FAIL] {response.status_code} | {name:<25} | {url:<35}")
            all_passed = False

    print("\n=======================================================")
    if all_passed:
        print("[SUCCESS] ALL PUBLIC AND /OPS ROUTES PASSED 100% VERIFICATION!")
    else:
        print("[ERROR] SOME ROUTES FAILED - CHECK OUTPUT ABOVE")
    print("=======================================================")

if __name__ == '__main__':
    run_verification()
