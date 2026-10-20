from django.contrib import admin

# Register your models here.
from .models import FoodItem, Tag   , Category

admin.site.register(FoodItem)


admin.site.register(Tag)

admin.site.register(Category)