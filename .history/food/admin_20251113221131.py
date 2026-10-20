from django.contrib import admin
from .models import Category, Tag, Spot, SpotInfo, Photo, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

class SpotInfoInline(admin.StackedInline):
    model = SpotInfo
    max_num = 1
    can_delete = True

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "distance_km", "rate", "created")
    list_filter = ("category", "tags")
    search_fields = ("name",)
    inlines = (SpotInfoInline, PhotoInline)
    filter_horizontal = ("tags",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("spot", "user", "rating", "created")
    list_filter = ("rating",)
