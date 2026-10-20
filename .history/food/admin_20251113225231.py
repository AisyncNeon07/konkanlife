from django.contrib import admin

# Register your models here.
from .models import Spots  , Category

admin.site.register(Category)

admin.site.register(Spots)