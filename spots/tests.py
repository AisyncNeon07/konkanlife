from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from spots.models import Spots

class SpotsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner_user = User.objects.create_user(username='spotowner', password='Password123!')
        self.owner_profile = self.owner_user.profile
        
        self.other_user = User.objects.create_user(username='otheruser', password='Password123!')
        self.other_profile = self.other_user.profile
        
        self.spot = Spots.objects.create(
            name='Secret Cliff Viewpoint',
            uploaded_by=self.owner_profile,
            price=0,
            rating=4.8,
            description='Incredible vantage point over the Arabian Sea.'
        )

    def test_spots_home_view(self):
        response = self.client.get(reverse('home_spots'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Secret Cliff Viewpoint')

    def test_spot_detail_view(self):
        response = self.client.get(reverse('details_spots', kwargs={'pk': self.spot.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Secret Cliff Viewpoint')

    def test_spot_create_view_authenticated(self):
        self.client.login(username='spotowner', password='Password123!')
        response = self.client.post(reverse('create_spot'), {
            'name': 'New Hidden Waterfall',
            'price': 50.0,
            'rating': 4.5,
            'description': 'Lush monsoon waterfall'
        })
        self.assertEqual(response.status_code, 302)
        new_spot = Spots.objects.filter(name='New Hidden Waterfall').first()
        self.assertIsNotNone(new_spot)
        self.assertEqual(new_spot.uploaded_by, self.owner_profile)

    def test_spot_update_by_owner_allowed(self):
        self.client.login(username='spotowner', password='Password123!')
        response = self.client.post(reverse('update_spot', kwargs={'pk': self.spot.id}), {
            'name': 'Updated Cliff Viewpoint',
            'price': 0,
            'rating': 4.9,
            'description': 'Updated description.'
        })
        self.assertEqual(response.status_code, 302)
        self.spot.refresh_from_db()
        self.assertEqual(self.spot.name, 'Updated Cliff Viewpoint')

    def test_spot_update_by_non_owner_forbidden(self):
        self.client.login(username='otheruser', password='Password123!')
        response = self.client.post(reverse('update_spot', kwargs={'pk': self.spot.id}), {
            'name': 'Hacked Spot Name',
            'price': 0,
            'rating': 1.0,
            'description': 'Hacked.'
        })
        self.assertEqual(response.status_code, 403)
        self.spot.refresh_from_db()
        self.assertEqual(self.spot.name, 'Secret Cliff Viewpoint')

    def test_spot_delete_by_non_owner_forbidden(self):
        self.client.login(username='otheruser', password='Password123!')
        response = self.client.post(reverse('delete_spot', kwargs={'pk': self.spot.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Spots.objects.filter(id=self.spot.id).exists())

    def test_spot_delete_by_owner_allowed(self):
        self.client.login(username='spotowner', password='Password123!')
        response = self.client.post(reverse('delete_spot', kwargs={'pk': self.spot.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Spots.objects.filter(id=self.spot.id).exists())
