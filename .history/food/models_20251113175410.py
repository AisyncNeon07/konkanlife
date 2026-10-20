from django.db import models

# Create your models here.


class Name(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    distance = models.IntegerField()
    rate = models.CharField(max_length=50)  
    id = models.UUIDField(primary_key=True, editable=False)