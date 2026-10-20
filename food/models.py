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


from users.models import Profile

class FoodItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    # Main Info
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
  
    # Display Info
    price = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    photo = models.ImageField(null=True, blank=True , default='default_food.jpg')

    # FoodInfo (now merged)
    description = models.TextField(blank=True, null=True)
 
    best_time_to_eat = models.CharField(max_length=100, blank=True, null=True)

    # System fields
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', '-created_at']
        indexes = [
            models.Index(fields=['-rating'], name='food_rating_idx'),
            models.Index(fields=['-created_at'], name='food_created_idx'),
            models.Index(fields=['name'], name='food_name_idx'),
        ]

    def __str__(self):
        return self.name

    
    

