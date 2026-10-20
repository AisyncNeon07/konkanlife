from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Spots(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="spots")
    name = models.CharField(max_length=200)
    distance_km = models.PositiveIntegerField(null=True, blank=True)
    rate = models.CharField(max_length=50, default="Free")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


