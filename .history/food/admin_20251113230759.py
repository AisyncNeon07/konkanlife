from django.contrib import admin

# Register your models here.
from .models import Spots  , Category , spot_info , Tag

admin.site.register(Category)

admin.site.register(Spots)

admin.site.register(spot_info)  

admin.site.register(Tag)