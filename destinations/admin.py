from django.contrib import admin
from .models import Destination, Gallery

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location_name', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'category', 'created_at')
    list_editable = ('is_verified',)
    search_fields = ('title', 'location_name', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryInline]
    actions = ['verify_selected', 'unverify_selected']

    @admin.action(description="Mark selected destinations as Verified 🟢")
    def verify_selected(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected destinations as Unverified ⚪")
    def unverify_selected(self, request, queryset):
        queryset.update(is_verified=False)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Location & Logistics', {
            'fields': ('location_name', 'latitude', 'longitude', 'best_time_to_visit', 'timings', 'entry_fees')
        }),
        ('Media & Content', {
            'fields': ('main_image', 'travel_tips')
        }),
        ('Administration', {
            'fields': ('is_verified', 'submitted_by'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Gallery)
