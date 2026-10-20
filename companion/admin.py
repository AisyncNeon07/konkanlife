from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Partner,
    Itinerary,
    ItineraryDay,
    ItineraryStop,
    NFCTag,
    NFCTapEvent,
    EmergencyContact,
    FAQ,
    TravelTip,
    Announcement,
    AdminAuditLog
)

# Admin Site Customization
admin.site.site_header = "Ratnagiri Tourism Operations Control Center"
admin.site.site_title = "Konkan Ops CMS"
admin.site.index_title = "Platform Operations & Content Management"


class ItineraryStopInline(admin.TabularInline):
    model = ItineraryStop
    extra = 1
    fields = ('order_index', 'stop_type', 'destination', 'custom_title', 'start_time', 'duration_minutes', 'travel_time_minutes')
    ordering = ('order_index',)


class ItineraryDayInline(admin.StackedInline):
    model = ItineraryDay
    extra = 1
    fields = ('day_number', 'title', 'summary', 'order')
    ordering = ('day_number',)


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_days', 'audience', 'season', 'difficulty', 'estimated_cost_inr', 'is_featured', 'is_active', 'view_on_site_link')
    list_filter = ('audience', 'season', 'difficulty', 'duration_days', 'is_featured', 'is_active')
    search_fields = ('title', 'tagline', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ItineraryDayInline]

    def view_on_site_link(self, obj):
        url = reverse('itinerary_detail', kwargs={'slug': obj.slug})
        return format_html('<a href="{}" target="_blank" class="button">Open ↗</a>', url)
    view_on_site_link.short_description = "Live Preview"


@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ('itinerary', 'day_number', 'title')
    list_filter = ('itinerary',)
    inlines = [ItineraryStopInline]


@admin.register(ItineraryStop)
class ItineraryStopAdmin(admin.ModelAdmin):
    list_display = ('day', 'order_index', 'title', 'stop_type', 'start_time', 'duration_minutes')
    list_filter = ('stop_type', 'day__itinerary')
    search_fields = ('custom_title', 'destination__title', 'activity_description')


@admin.register(NFCTag)
class NFCTagAdmin(admin.ModelAdmin):
    list_display = ('tag_uid', 'title', 'tag_type', 'target_experience', 'assigned_partner', 'tap_count', 'unique_visitor_count', 'is_active', 'live_tap_link', 'qr_code_link')
    list_filter = ('tag_type', 'target_experience', 'is_active', 'assigned_partner')
    search_fields = ('tag_uid', 'title', 'custom_welcome_title')
    readonly_fields = ('tap_count', 'unique_visitor_count', 'created_at', 'last_tapped_at', 'live_tap_link', 'qr_code_link')
    actions = ['activate_tags', 'pause_tags']

    @admin.action(description="Activate selected NFC tags")
    def activate_tags(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Pause selected NFC tags")
    def pause_tags(self, request, queryset):
        queryset.update(is_active=False)

    def live_tap_link(self, obj):
        url = reverse('nfc_tap_entry', kwargs={'tag_uid': obj.tag_uid})
        return format_html('<a href="{}" target="_blank" style="color:#0284c7; font-weight:bold;">Tap / Test ↗</a>', url)
    live_tap_link.short_description = "NFC Tap URL"

    def qr_code_link(self, obj):
        url = reverse('nfc_qr_view', kwargs={'tag_uid': obj.tag_uid})
        return format_html('<a href="{}" target="_blank" style="color:#059669; font-weight:bold;">QR Fallback ↗</a>', url)
    qr_code_link.short_description = "QR Code"


@admin.register(NFCTapEvent)
class NFCTapEventAdmin(admin.ModelAdmin):
    list_display = ('tag', 'tapped_at', 'device_type', 'action_taken', 'referrer')
    list_filter = ('device_type', 'action_taken', 'tapped_at')
    search_fields = ('tag__tag_uid', 'tag__title', 'session_hash')
    readonly_fields = ('tag', 'tapped_at', 'session_hash', 'device_type', 'browser_family', 'referrer', 'action_taken')

    def has_add_permission(self, request):
        return False


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'partner_type', 'phone', 'is_verified', 'is_featured', 'is_active')
    list_filter = ('partner_type', 'is_verified', 'is_featured', 'is_active')
    search_fields = ('business_name', 'address', 'phone', 'email')
    prepopulated_fields = {'slug': ('business_name',)}


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'phone_number', 'alternate_phone', 'is_24x7', 'is_active', 'order')
    list_filter = ('category', 'is_24x7', 'is_active')
    search_fields = ('name', 'phone_number', 'address')
    list_editable = ('order', 'is_active')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_published')


@admin.register(TravelTip)
class TravelTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('order', 'is_active')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'urgency_level', 'is_active', 'start_time', 'end_time', 'created_at')
    list_filter = ('urgency_level', 'is_active')
    search_fields = ('title', 'message')


@admin.register(AdminAuditLog)
class AdminAuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'resource_type', 'resource_name')
    list_filter = ('action', 'resource_type', 'timestamp')
    search_fields = ('user__username', 'resource_name', 'resource_type')
    readonly_fields = ('user', 'action', 'resource_type', 'resource_name', 'details_json', 'timestamp')

    def has_add_permission(self, request):
        return False
