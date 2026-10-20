from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    """One Category -> Many Spots (One-to-Many)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Many-to-Many tags for flexible labeling"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Spot(models.Model):
    """Main place model"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="spots")
    name = models.CharField(max_length=200)
    description_short = models.CharField(max_length=255, blank=True)
    distance_km = models.PositiveIntegerField(null=True, blank=True)
    rate = models.CharField(max_length=50, default="Free")      # string because some rates are "Free"
    tags = models.ManyToManyField(Tag, blank=True, related_name="spots")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SpotInfo(models.Model):
    """One-to-One extra details for a Spot (One-to-One)"""
    spot = models.OneToOneField(Spot, on_delete=models.CASCADE, related_name="info")
    long_description = models.TextField(blank=True)
    map_iframe = models.TextField(blank=True)   # store google-maps iframe or link
    opening_hours = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Info for {self.spot.name}"


class Photo(models.Model):
    """Photos: One Spot -> Many Photos (One-to-Many)"""
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="spots/photos/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Photo {self.id} for {self.spot.name}"


class Review(models.Model):
    """User reviews for Spots (One-to-Many from Spot; One-to-Many from User)"""
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="spot_reviews")
    rating = models.PositiveSmallIntegerField(default=5)   # 1-5
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.spot.name} - {self.rating} ★"
