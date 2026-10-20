from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from companion.models import (
    NFCTag, NFCTapEvent, Partner, Itinerary, ItineraryDay, ItineraryStop,
    EmergencyContact, FAQ, TravelTip, Announcement, AdminAuditLog
)
from destinations.models import Destination


class OperationsControlCenterTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Staff Admin User
        self.admin_user = User.objects.create_superuser(
            username='opsadmin',
            email='ops@konkan.test',
            password='TestAdminPassword123'
        )

        # Non-Staff Regular Tourist User
        self.tourist_user = User.objects.create_user(
            username='tourist_bob',
            email='bob@konkan.test',
            password='TestUserPassword123'
        )

        # Sample Partner
        self.partner = Partner.objects.create(
            business_name="Ratnagiri Beach Resort",
            partner_type="HOTEL",
            short_tagline="Beachfront resort overlooking Arabian sea",
            phone="+91 98221 00001",
            is_active=True
        )

        # Sample Destination
        self.destination = Destination.objects.create(
            title="Ratnadurg Fort",
            category="Fort",
            location_name="Ratnagiri City",
            latitude=16.9856,
            longitude=73.2678,
            description="Historic fort by the sea",
            is_verified=False
        )

        # Sample NFC Tag
        self.nfc_tag = NFCTag.objects.create(
            tag_uid="RATNAGIRI-TEST-001",
            title="Beach Resort Tag #01",
            assigned_partner=self.partner,
            tag_type="HOTEL",
            target_experience="HOME",
            is_active=True
        )

        # Sample Itinerary
        self.itinerary = Itinerary.objects.create(
            title="2 Days Heritage Coastal Trail",
            slug="2-days-heritage-coastal-trail",
            duration_days=2,
            audience="COUPLES",
            is_featured=True
        )
        self.day1 = ItineraryDay.objects.create(
            itinerary=self.itinerary,
            day_number=1,
            title="Forts and Coastal Panoramas"
        )
        self.stop1 = ItineraryStop.objects.create(
            day=self.day1,
            destination=self.destination,
            custom_title="Morning Walk at Fort",
            stop_type="FORT",
            order_index=1
        )

    def test_anonymous_user_redirected_from_ops(self):
        """Anonymous tourists must be redirected to login when accessing ops."""
        response = self.client.get(reverse('ops_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_regular_user_redirected_from_ops(self):
        """Non-staff users must not be allowed to access ops views."""
        self.client.login(username='tourist_bob', password='TestUserPassword123')
        response = self.client.get(reverse('ops_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_staff_admin_can_access_dashboard(self):
        """Staff administrators can access the SaaS operations dashboard."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        response = self.client.get(reverse('ops_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ops/dashboard.html')
        self.assertIn('stats', response.context)
        self.assertEqual(response.context['stats']['total_destinations'], 1)

    def test_places_list_and_create(self):
        """Test destination list and creation through the ops CMS."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        # Access list
        list_resp = self.client.get(reverse('ops_places_list'))
        self.assertEqual(list_resp.status_code, 200)
        self.assertTemplateUsed(list_resp, 'ops/places_list.html')

        # Create destination
        create_data = {
            'title': 'Bhatye Beach',
            'category': 'Beach',
            'location_name': 'Bhatye, Ratnagiri',
            'latitude': 16.9740,
            'longitude': 73.2840,
            'description': 'Calm black sand beach with casuarina trees',
            'entry_fees': 'Free',
            'timings': 'Open 24 hours',
            'is_verified': True
        }
        create_resp = self.client.post(reverse('ops_place_create'), create_data)
        self.assertEqual(create_resp.status_code, 302)
        self.assertTrue(Destination.objects.filter(title='Bhatye Beach').exists())

        # Verify audit log was created
        audit_entry = AdminAuditLog.objects.filter(resource_type='Place', action='CREATE').first()
        self.assertIsNotNone(audit_entry)

    def test_place_toggle_verify(self):
        """Staff can 1-click toggle verification of destinations."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        self.assertFalse(self.destination.is_verified)

        toggle_url = reverse('ops_place_toggle_verify', kwargs={'pk': self.destination.pk})
        resp = self.client.post(toggle_url)
        self.assertEqual(resp.status_code, 302)

        self.destination.refresh_from_db()
        self.assertTrue(self.destination.is_verified)

    def test_itinerary_builder_and_stop_reordering(self):
        """Test visual journey builder stop management and reordering."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        # View visual builder
        builder_url = reverse('ops_itinerary_builder', kwargs={'pk': self.itinerary.pk})
        resp = self.client.get(builder_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'ops/itinerary_builder.html')

        # Add second stop
        dest2 = Destination.objects.create(
            title="Thiba Palace",
            category="Viewpoint",
            location_name="Ratnagiri",
            is_verified=True
        )
        stop2 = ItineraryStop.objects.create(
            day=self.day1,
            destination=dest2,
            custom_title="Afternoon Museum Tour",
            stop_type="SIGHTSEEING",
            order_index=2
        )

        # Move stop2 UP
        reorder_url = reverse('ops_itinerary_reorder_stop', kwargs={'pk': self.itinerary.pk, 'stop_id': stop2.pk, 'direction': 'up'})
        reorder_resp = self.client.post(reorder_url)
        self.assertEqual(reorder_resp.status_code, 302)

        # Reload stops and verify swapped orders
        self.stop1.refresh_from_db()
        stop2.refresh_from_db()
        self.assertEqual(stop2.order_index, 1)
        self.assertEqual(self.stop1.order_index, 2)

    def test_bulk_nfc_generator(self):
        """Test commercial batch generation of sequential NFC tags."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        bulk_data = {
            'prefix': 'HOTEL-SEAVIEW-',
            'start_number': 1,
            'count': 10,
            'tag_type': 'HOTEL',
            'target_experience': 'HOME',
            'assigned_partner': self.partner.pk,
            'custom_welcome_title': 'Welcome to Seaview',
            'custom_welcome_message': 'Enjoy your stay in Konkan!'
        }
        resp = self.client.post(reverse('ops_nfc_bulk_generate'), bulk_data)
        self.assertEqual(resp.status_code, 302)

        # Check that 10 tags were created with correct prefix
        created_count = NFCTag.objects.filter(tag_uid__startswith='HOTEL-SEAVIEW-').count()
        self.assertEqual(created_count, 10)

    def test_nfc_csv_export(self):
        """Test production CSV export of NFC tags for tag flashing equipment."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        csv_resp = self.client.get(reverse('ops_nfc_export_csv'))
        self.assertEqual(csv_resp.status_code, 200)
        self.assertEqual(csv_resp['Content-Type'], 'text/csv')
        self.assertIn('RATNAGIRI-TEST-001', csv_resp.content.decode('utf-8'))
        self.assertIn('https://konkantravel.in/t/RATNAGIRI-TEST-001/', csv_resp.content.decode('utf-8'))

    def test_nfc_print_sheet(self):
        """Test printable QR/NFC sticker sheet generation."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        sheet_resp = self.client.get(reverse('ops_nfc_print_sheet'))
        self.assertEqual(sheet_resp.status_code, 200)
        self.assertTemplateUsed(sheet_resp, 'ops/nfc_print_sheet.html')
        self.assertIn(b'RATNAGIRI-TEST-001', sheet_resp.content)

    def test_content_hub_crud(self):
        """Test adding and managing FAQs, Tips, and Announcements."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        # Add FAQ
        faq_data = {
            'question': 'How do I tap the NFC card?',
            'answer': 'Simply hold the top of your phone near the card logo.',
            'category': 'NFC',
            'order': 1,
            'is_published': True
        }
        faq_resp = self.client.post(reverse('ops_faq_create'), faq_data)
        self.assertEqual(faq_resp.status_code, 302)
        self.assertTrue(FAQ.objects.filter(question='How do I tap the NFC card?').exists())

        # Add Travel Tip
        tip_data = {
            'title': 'Ferry Timings from Jaigad to Tavsal',
            'content': 'Ferries run every 45 minutes between 6:00 AM and 10:00 PM.',
            'category': 'BEST_TIME',
            'icon': 'fa-ship',
            'order': 1,
            'is_active': True
        }
        tip_resp = self.client.post(reverse('ops_tip_create'), tip_data)
        self.assertEqual(tip_resp.status_code, 302)
        self.assertTrue(TravelTip.objects.filter(title__contains='Ferry').exists())

        # Add Announcement
        ann_data = {
            'title': 'Konkan Alphonso Mango Festival 2026',
            'message': 'Visit local farms for fresh Hapus mango tastings all week!',
            'urgency_level': 'INFO',
            'link_url': 'https://konkantravel.in',
            'is_active': True
        }
        ann_resp = self.client.post(reverse('ops_announcement_create'), ann_data)
        self.assertEqual(ann_resp.status_code, 302)
        self.assertTrue(Announcement.objects.filter(title__contains='Mango').exists())

    def test_partner_crud(self):
        """Test partner directory management."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        partner_data = {
            'business_name': 'Ganpatipule Beach Homestay',
            'partner_type': 'HOMESTAY',
            'short_tagline': 'Cozy authentic stay near Ganpatipule beach',
            'phone': '+91 98221 00099',
            'address': 'Ganpatipule Main Road',
            'is_active': True
        }
        p_resp = self.client.post(reverse('ops_partner_create'), partner_data)
        self.assertEqual(p_resp.status_code, 302)
        self.assertTrue(Partner.objects.filter(business_name='Ganpatipule Beach Homestay').exists())

    def test_media_and_analytics_views(self):
        """Test Media Hub, Analytics Center, and System Audit views load with 200 OK."""
        self.client.login(username='opsadmin', password='TestAdminPassword123')
        
        media_resp = self.client.get(reverse('ops_media_hub'))
        self.assertEqual(media_resp.status_code, 200)

        analytics_resp = self.client.get(reverse('ops_analytics_center'))
        self.assertEqual(analytics_resp.status_code, 200)

        audit_resp = self.client.get(reverse('ops_system_hub'))
        self.assertEqual(audit_resp.status_code, 200)
