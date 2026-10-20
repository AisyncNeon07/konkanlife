from django.test import TestCase, Client
from django.urls import reverse
from destinations.models import Destination

class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.verified_dest = Destination.objects.create(
            title='Sindhudurg Fort',
            description='Historic sea fort built by Chhatrapati Shivaji Maharaj.',
            category='Fort',
            location_name='Malvan',
            is_verified=True
        )
        self.unverified_dest = Destination.objects.create(
            title='Unverified Private Beach',
            description='Private unverified spot.',
            category='Beach',
            location_name='Unknown',
            is_verified=False
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_culture_temples_view(self):
        response = self.client.get(reverse('temples'))
        self.assertEqual(response.status_code, 200)

    def test_search_view_verified_results(self):
        response = self.client.get(reverse('search') + '?q=Sindhudurg')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sindhudurg Fort')
        self.assertNotContains(response, 'Unverified Private Beach')

    def test_search_view_empty_query(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
