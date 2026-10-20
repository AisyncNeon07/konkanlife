import uuid
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Spots(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    distance = models.IntegerField()
    rate = models.CharField(max_length=50)  
    photo = models.ImageField(upload_to='spots_photos/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
