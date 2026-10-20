from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'rating', 'created_at', 'user')
    list_filter = ('rating', 'created_at')
    search_fields = ('destination__title', 'comment')
