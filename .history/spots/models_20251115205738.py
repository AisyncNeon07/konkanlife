import uuid
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):  # ex: spicy, sweet, veg, non-veg
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Spots(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    # Main Info
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # Display Info
    price = models.FloatField()
    rating = models.FloatField(default=0.0)
    photo = models.ImageField(null=True, blank=True , default='default_food.jpg')

    # FoodInfo (now merged)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    recipe_link = models.URLField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    best_time_to_eat = models.CharField(max_length=100, blank=True, null=True)

    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


