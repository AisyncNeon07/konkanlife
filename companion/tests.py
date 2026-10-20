import json
import base64
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from destinations.models import Destination
from companion.models import (
    Partner,
    Itinerary,
    ItineraryDay,
    ItineraryStop,
    NFCTag,
    NFCTapEvent,
    EmergencyContact
)


class CompanionModelsAndViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Partner
        self.partner = Partner.objects.create(
            business_name='Hotel Sea Breeze Resort',
            partner_type='HOTEL',
            address='Bhatye Beach Road, Ratnagiri',
            phone='+91 98220 12345'
        )

        # 2. Destination
        self.dest = Destination.objects.create(
            title='Ratnadurg Fort',
            description='Magnificent coastal sea fort overlooking Mirya Bay.',
            category='Fort',
            location_name='Ratnagiri',
            latitude=16.9902,
            longitude=73.3120,
            is_verified=True
        )

        # 3. Itinerary & Stops
        self.itinerary = Itinerary.objects.create(
            title='2-Day Essential Ratnagiri',
            tagline='Forts, beaches and food.',
            description='Complete weekend guide.',
            duration_days=2,
            audience='ALL',
            season='ALL',
            difficulty='EASY',
            estimated_cost_inr='₹2,500 - ₹4,500',
            total_distance_km=48.0,
            is_active=True
        )
        self.day1 = ItineraryDay.objects.create(
            itinerary=self.itinerary,
            day_number=1,
            title='Sea Forts & Sunset Horizons'
        )
        self.stop1 = ItineraryStop.objects.create(
            day=self.day1,
            destination=self.dest,
            stop_type='FORT',
            order_index=1,
            start_time='09:00 AM',
            duration_minutes=90,
            activity_description='Explore ramparts.'
        )

        # 4. NFC Tags
        self.tag_home = NFCTag.objects.create(
            tag_uid='TEST-HOTEL-01',
            title='Test Hotel Room Tag',
            tag_type='HOTEL',
            target_experience='HOME',
            assigned_partner=self.partner,
            custom_welcome_title='Welcome to Hotel Sea Breeze!'
        )

        self.tag_itin = NFCTag.objects.create(
            tag_uid='TEST-2DAY-TRIP',
            title='2-Day Trip Tag',
            tag_type='ITINERARY',
            target_experience='SPECIFIC_ITINERARY',
            assigned_itinerary=self.itinerary
        )

        # 5. Emergency Contact
        self.hospital = EmergencyContact.objects.create(
            name='Civil Hospital',
            category='HOSPITAL',
            phone_number='+91 2352 222333',
            is_24x7=True
        )

    def test_nfc_tap_entry_success_and_telemetry(self):
        initial_taps = self.tag_home.tap_count
        response = self.client.get(reverse('nfc_tap_entry', kwargs={'tag_uid': 'TEST-HOTEL-01'}))
        
        # Should redirect to companion home with tapped param
        self.assertEqual(response.status_code, 302)
        self.assertIn('companion', response.url)

        # Check metrics updated
        self.tag_home.refresh_from_db()
        self.assertEqual(self.tag_home.tap_count, initial_taps + 1)
        self.assertGreaterEqual(self.tag_home.unique_visitor_count, 1)

        # Check telemetry logged
        event = NFCTapEvent.objects.filter(tag=self.tag_home).first()
        self.assertIsNotNone(event)
        self.assertEqual(event.action_taken, 'tap_entry')

    def test_nfc_tap_entry_specific_itinerary_redirect(self):
        response = self.client.get(reverse('nfc_tap_entry', kwargs={'tag_uid': 'TEST-2DAY-TRIP'}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.itinerary.slug, response.url)

    def test_nfc_tap_entry_invalid_tag_fallback(self):
        response = self.client.get(reverse('nfc_tap_entry', kwargs={'tag_uid': 'NON-EXISTENT-TAG'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, Traveller!')

    def test_nfc_qr_view(self):
        # QR route routes directly to the target experience page (no duplicate QR on browser)
        response = self.client.get(reverse('nfc_qr_view', kwargs={'tag_uid': 'TEST-HOTEL-01'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hotel Sea Breeze Resort')

    def test_companion_home_view(self):
        response = self.client.get(reverse('companion_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Ratnagiri')
        self.assertContains(response, 'Curated Ratnagiri Itineraries')

    def test_itinerary_list_and_filters(self):
        response = self.client.get(reverse('itinerary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2-Day Essential Ratnagiri')

        # Filter by duration
        response_filtered = self.client.get(reverse('itinerary_list') + '?duration=2')
        self.assertEqual(response_filtered.status_code, 200)
        self.assertContains(response_filtered, '2-Day Essential Ratnagiri')

    def test_itinerary_detail_view(self):
        response = self.client.get(reverse('itinerary_detail', kwargs={'slug': self.itinerary.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2-Day Essential Ratnagiri')
        self.assertContains(response, 'Day 01')
        self.assertContains(response, 'Ratnadurg Fort')

    def test_near_me_view(self):
        response = self.client.get(reverse('near_me'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Near Me in Ratnagiri')
        self.assertContains(response, 'Ratnadurg Fort')

    def test_my_trip_view(self):
        response = self.client.get(reverse('my_trip'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Custom Ratnagiri Trip')

    def test_trip_share_view_with_valid_payload(self):
        sample_trip = [{'id': 1, 'title': 'Ratnadurg Fort', 'category': 'Fort', 'slug': 'ratnadurg-fort'}]
        json_str = json.dumps(sample_trip)
        b64 = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')

        response = self.client.get(reverse('trip_share') + f'?data={b64}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ratnadurg Fort')

    def test_emergency_hub_view(self):
        response = self.client.get(reverse('emergency_hub'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Civil Hospital')
        self.assertContains(response, '+91 2352 222333')

    def test_partner_directory_and_detail(self):
        response_dir = self.client.get(reverse('partner_directory'))
        self.assertEqual(response_dir.status_code, 200)
        self.assertContains(response_dir, 'Hotel Sea Breeze Resort')

        response_detail = self.client.get(reverse('partner_detail', kwargs={'slug': self.partner.slug}))
        self.assertEqual(response_detail.status_code, 200)
        self.assertContains(response_detail, 'Hotel Sea Breeze Resort')

    def test_analytics_dashboard_view(self):
        response = self.client.get(reverse('companion_analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NFC Companion Analytics')
        self.assertContains(response, 'TEST-HOTEL-01')
