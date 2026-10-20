import uuid
from django.db import models

# Create your models here.


class Spots(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    distance = models.IntegerField()
    rate = models.CharField(max_length=50)  
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    def __str__(self):
        return self.id