from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='Password123!')

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'StrongPass123!@#',
            'password2': 'StrongPass123!@#'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_post_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'mismatchuser',
            'password1': 'StrongPass123!@#',
            'password2': 'DifferentPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_post(self):
        self.client.login(username='testuser', password='Password123!')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_get(self):
        self.client.login(username='testuser', password='Password123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
