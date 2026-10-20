from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from destinations.models import Destination
from reviews.models import Review

class DestinationsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='traveler', password='Password123!')
        self.dest1 = Destination.objects.create(
            title='Ganpatipule Beach',
            description='A serene beach with white sands.',
            category='Beach',
            location_name='Ratnagiri',
            is_verified=True
        )

    def test_slug_generation_and_uniqueness(self):
        dest2 = Destination.objects.create(
            title='Ganpatipule Beach',
            description='Duplicate name test.',
            category='Beach',
            location_name='Ratnagiri',
            is_verified=True
        )
        self.assertEqual(self.dest1.slug, 'ganpatipule-beach')
        self.assertTrue(dest2.slug.startswith('ganpatipule-beach-'))
        self.assertNotEqual(self.dest1.slug, dest2.slug)

    def test_destination_list_view(self):
        response = self.client.get(reverse('destination_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ganpatipule Beach')

    def test_destination_detail_public(self):
        response = self.client.get(reverse('destination_detail', kwargs={'slug': self.dest1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ganpatipule Beach')

    def test_destination_review_submission_authenticated(self):
        self.client.login(username='traveler', password='Password123!')
        response = self.client.post(reverse('destination_detail', kwargs={'slug': self.dest1.slug}), {
            'rating': 5,
            'comment': 'Amazing coastal vibes!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(destination=self.dest1, user=self.user).exists())

    def test_destination_review_submission_guest(self):
        response = self.client.post(reverse('destination_detail', kwargs={'slug': self.dest1.slug}), {
            'rating': 4,
            'comment': 'Loved the peaceful sunset!',
            'author_name': 'Guest Wanderer'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(destination=self.dest1, author_name='Guest Wanderer').exists())
