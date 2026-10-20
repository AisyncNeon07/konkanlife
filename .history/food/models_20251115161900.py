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


class FoodItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Snacks, Seafood, Veg, Sweets
    tags = models.ManyToManyField(Tag, blank=True)  # "spicy", "veg", "street-food"

    price = models.FloatField()  # food price
    rating = models.FloatField(default=0.0)

    photo = models.ImageField(upload_to='food_photos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FoodInfo(models.Model):
    
    food = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    description = models.TextField()                 # About the dish
    ingredients = models.TextField(blank=True)       # Ingredients list
    recipe_link = models.URLField(blank=True, null=True)  # YouTube, blog link
    calories = models.IntegerField(blank=True, null=True) # optional

    best_time_to_eat = models.CharField(max_length=100, blank=True)  # Morning / Evening / Anytime

    def __str__(self):
        return f"Info for {self.food.name}"
