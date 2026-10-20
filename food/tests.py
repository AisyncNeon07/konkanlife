from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from food.models import Category, Tag, FoodItem

class FoodViewsAndModelsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='chefuser', password='Password123!')
        self.profile = self.user.profile

        self.other_user = User.objects.create_user(username='otherchef', password='Password123!')
        self.other_profile = self.other_user.profile

        self.category = Category.objects.create(name='Seafood')
        self.tag = Tag.objects.create(name='Spicy')

        self.food_item = FoodItem.objects.create(
            name='Surmai Fry',
            uploaded_by=self.profile,
            price=350.0,
            rating=4.9,
            description='Freshly caught kingfish spiced with Malvani masala.',
            best_time_to_eat='Dinner'
        )

    def test_category_and_tag_str(self):
        self.assertEqual(str(self.category), 'Seafood')
        self.assertEqual(str(self.tag), 'Spicy')

    def test_food_home_view(self):
        response = self.client.get(reverse('food_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Surmai Fry')

    def test_food_detail_view(self):
        response = self.client.get(reverse('details', kwargs={'pk': self.food_item.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Surmai Fry')

    def test_food_create_view_authenticated(self):
        self.client.login(username='chefuser', password='Password123!')
        response = self.client.post(reverse('create_food'), {
            'name': 'Solkadhi',
            'price': 60.0,
            'rating': 5.0,
            'description': 'Refreshing digestive drink with coconut milk and kokum',
            'best_time_to_eat': 'After meals'
        })
        self.assertEqual(response.status_code, 302)
        item = FoodItem.objects.filter(name='Solkadhi').first()
        self.assertIsNotNone(item)
        self.assertEqual(item.uploaded_by, self.profile)

    def test_food_update_by_owner_allowed(self):
        self.client.login(username='chefuser', password='Password123!')
        response = self.client.post(reverse('update_food', kwargs={'pk': self.food_item.id}), {
            'name': 'Surmai Rawa Fry',
            'price': 380.0,
            'rating': 5.0,
            'description': 'Crispy rawa fried kingfish.',
            'best_time_to_eat': 'Dinner'
        })
        self.assertEqual(response.status_code, 302)
        self.food_item.refresh_from_db()
        self.assertEqual(self.food_item.name, 'Surmai Rawa Fry')

    def test_food_update_by_non_owner_forbidden(self):
        self.client.login(username='otherchef', password='Password123!')
        response = self.client.post(reverse('update_food', kwargs={'pk': self.food_item.id}), {
            'name': 'Malicious Item',
            'price': 1.0,
            'rating': 1.0
        })
        self.assertEqual(response.status_code, 403)
        self.food_item.refresh_from_db()
        self.assertEqual(self.food_item.name, 'Surmai Fry')

    def test_food_delete_by_non_owner_forbidden(self):
        self.client.login(username='otherchef', password='Password123!')
        response = self.client.post(reverse('delete_food', kwargs={'pk': self.food_item.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(FoodItem.objects.filter(id=self.food_item.id).exists())

    def test_food_delete_by_owner_allowed(self):
        self.client.login(username='chefuser', password='Password123!')
        response = self.client.post(reverse('delete_food', kwargs={'pk': self.food_item.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FoodItem.objects.filter(id=self.food_item.id).exists())
