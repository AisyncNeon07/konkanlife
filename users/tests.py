import uuid
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile

class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='konkanexplorer', password='Password123!')
        self.profile = self.user.profile
        self.profile.name = 'Konkan Explorer'
        self.profile.save()
        
        self.other_user = User.objects.create_user(username='otherperson', password='Password123!')
        self.other_profile = self.other_user.profile

    def test_user_profile_view_success(self):
        response = self.client.get(reverse('user_profile', kwargs={'pk': str(self.profile.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Konkan Explorer')

    def test_user_profile_view_404(self):
        random_uuid = str(uuid.uuid4())
        response = self.client.get(reverse('user_profile', kwargs={'pk': random_uuid}))
        self.assertEqual(response.status_code, 404)

    def test_my_profile_redirects_unauthenticated(self):
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 302)

    def test_my_profile_view_authenticated(self):
        self.client.login(username='konkanexplorer', password='Password123!')
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_owner_success(self):
        self.client.login(username='konkanexplorer', password='Password123!')
        response = self.client.post(reverse('edit_profile'), {
            'name': 'Updated Explorer',
            'short_intro': 'Local Guide & Storyteller',
            'bio': 'Passionate coastal explorer and photographer.'
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, 'Updated Explorer')
        self.assertEqual(self.profile.short_intro, 'Local Guide & Storyteller')
