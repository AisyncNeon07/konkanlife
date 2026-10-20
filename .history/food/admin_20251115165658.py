from django.contrib import admin

# Register your models here.
from .models import FoodItem, FoodInfo , Tag   , Category

admin.site.register(FoodItem)


admin.site.register(Tag)

admin.site.register(Category)