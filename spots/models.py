import uuid
from django.db import models
from users.models import Profile
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    uploaded_by = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)

    # Display Info
    distance = models.FloatField(null=True, blank=True)
    rating = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0, help_text="Estimated cost or entry fee")
    photo = models.ImageField(upload_to='spots/', null=True, blank=True)

    # Travel Info
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=100, blank=True, null=True, default="Sunrise - Sunset")
    closing_hours = models.CharField(max_length=100, blank=True, null=True, default="Sunset")
    map_link = models.URLField(blank=True, null=True, help_text="Google Maps URL")

    # System fields
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-rating'], name='spots_rating_idx'),
            models.Index(fields=['-created_at'], name='spots_created_idx'),
            models.Index(fields=['name'], name='spots_name_idx'),
        ]

    def __str__(self):
        return self.name


