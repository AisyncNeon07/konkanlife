import uuid
from django.db import models

# Create your models here.


class Catergory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Spots(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Catergory, on_delete=models.CASCADE)
    distance = models.IntegerField()
    rate = models.CharField(max_length=50)  
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    def __int__(self):
        return self.id
    
