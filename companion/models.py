import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from destinations.models import Destination


class Partner(models.Model):
    """
    Local business, hotel, resort, restaurant, or service partner distributing NFC tags.
    """
    PARTNER_TYPE_CHOICES = (
        ('HOTEL', 'Hotel & Resort'),
        ('HOMESTAY', 'Authentic Homestay'),
        ('RESTAURANT', 'Restaurant & Café'),
        ('TOUR_OPERATOR', 'Tour Operator & Guide'),
        ('LOCAL_ARTISAN', 'Local Artisan & Mango/Cashew Store'),
        ('TRANSPORT', 'Transport & Taxi Service'),
        ('ATTRACTION', 'Attraction & Kiosk'),
        ('OTHER', 'Other Partner'),
    )

    business_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPE_CHOICES, default='HOTEL', db_index=True)
    short_tagline = models.CharField(max_length=250, blank=True, help_text="e.g., Beachfront luxury stay in Ganpatipule")
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='partners/logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='partners/covers/', blank=True, null=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    google_maps_url = models.URLField(blank=True, help_text="Google Maps share link or location URL")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    exclusive_offer = models.CharField(max_length=250, blank=True, help_text="e.g. 10% Off on Dining or Welcome Drink for Konkan Guide Explorers")
    offer_code = models.CharField(max_length=50, blank=True, help_text="e.g. KONKAN10")
    amenities = models.CharField(max_length=255, blank=True, help_text="Comma-separated: Free Wi-Fi, Beach View, AC, Parking, Seafood, Pool")
    operating_hours = models.CharField(max_length=150, blank=True, help_text="e.g. Check-in 12:00 PM / Check-out 10:00 AM")
    price_range = models.CharField(max_length=100, blank=True, help_text="e.g. ?1,500 - ?3,500 / night or ?? Moderate")
    instagram_handle = models.CharField(max_length=100, blank=True, help_text="e.g. @sawantvilla_konkan")
    is_verified = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_map_url(self):
        if self.google_maps_url:
            return self.google_maps_url
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
        if self.address:
            import urllib.parse
            q = f"{self.business_name} {self.address}"
            return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(q)}"
        return None

    def get_amenities_list(self):
        if not self.amenities:
            return []
        return [a.strip() for a in self.amenities.split(',') if a.strip()]

    def primary_nfc_tag(self):
        return self.nfc_tags.filter(is_active=True).first() or self.nfc_tags.first()

    class Meta:
        ordering = ['-is_featured', 'business_name']
        indexes = [
            models.Index(fields=['is_active', '-is_featured'], name='partner_active_feat_idx'),
            models.Index(fields=['partner_type', 'is_active'], name='partner_type_active_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.business_name) or 'partner'
            slug = base_slug
            counter = 1
            while Partner.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.business_name} ({self.get_partner_type_display()})"


class Itinerary(models.Model):
    """
    Structured multi-day or single-day curated journeys for tourists.
    """
    AUDIENCE_CHOICES = (
        ('ALL', 'All Travelers'),
        ('FAMILY', 'Family with Kids'),
        ('COUPLE', 'Couples & Romantic'),
        ('BUDGET', 'Budget & Backpackers'),
        ('SOLO', 'Solo Explorers'),
        ('FOODIE', 'Culinary & Food Trails'),
        ('HERITAGE', 'History & Fort Trail'),
    )

    SEASON_CHOICES = (
        ('ALL', 'All Seasons'),
        ('WINTER', 'Winter (Nov - Feb)'),
        ('MONSOON', 'Monsoon Magic (Jun - Sep)'),
        ('SUMMER', 'Summer Coastal (Mar - May)'),
    )

    DIFFICULTY_CHOICES = (
        ('EASY', 'Relaxed & Easy Pace'),
        ('MODERATE', 'Moderate Sightseeing'),
        ('ACTIVE', 'Active & Adventurous'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=250, blank=True, help_text="e.g., Sea forts, tranquil beaches and authentic Malvani thalis")
    description = models.TextField()
    duration_days = models.PositiveIntegerField(default=1, help_text="Number of days (e.g., 1, 2, 3)")
    audience = models.CharField(max_length=30, choices=AUDIENCE_CHOICES, default='ALL', db_index=True)
    season = models.CharField(max_length=30, choices=SEASON_CHOICES, default='ALL', db_index=True)
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='EASY')
    cover_image = models.ImageField(upload_to='itineraries/', blank=True, null=True)
    estimated_cost_inr = models.CharField(max_length=100, blank=True, default="₹1,500 - ₹3,500 / day", help_text="Estimated budget range")
    total_distance_km = models.FloatField(default=0.0, help_text="Approximate travel distance in KM")
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Itineraries"
        ordering = ['order', 'duration_days', 'title']
        indexes = [
            models.Index(fields=['is_active', 'order'], name='itin_active_order_idx'),
            models.Index(fields=['is_active', 'duration_days'], name='itin_active_dur_idx'),
            models.Index(fields=['is_active', 'audience'], name='itin_active_aud_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'itinerary'
            slug = base_slug
            counter = 1
            while Itinerary.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.duration_days} Day{'s' if self.duration_days > 1 else ''})"

    def get_absolute_url(self):
        return reverse('itinerary_detail', kwargs={'slug': self.slug})


class ItineraryDay(models.Model):
    """
    Represents a specific day (Day 1, Day 2...) within a curated Itinerary.
    """
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200, help_text="e.g., Coastal Sea Forts & Sunset Horizons")
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['day_number', 'order']
        unique_together = ('itinerary', 'day_number')

    def __str__(self):
        return f"{self.itinerary.title} - Day {self.day_number}: {self.title}"


class ItineraryStop(models.Model):
    """
    An individual planned stop or activity during a specific day of an Itinerary.
    """
    STOP_TYPE_CHOICES = (
        ('MORNING', 'Morning Exploration'),
        ('BREAKFAST', 'Local Breakfast'),
        ('SIGHTSEEING', 'Sightseeing Landmark'),
        ('BEACH', 'Beach Relaxation'),
        ('FORT', 'Historic Fort Trail'),
        ('LUNCH', 'Authentic Lunch'),
        ('ADVENTURE', 'Water Sports & Adventure'),
        ('SUNSET', 'Sunset Vantage Point'),
        ('SHOPPING', 'Local Market & Souvenirs'),
        ('DINNER', 'Coastal Dinner'),
        ('STAY', 'Resort / Homestay Check-in'),
    )

    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='stops')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='itinerary_stops')
    custom_title = models.CharField(max_length=200, blank=True, help_text="Override or custom stop name")
    stop_type = models.CharField(max_length=30, choices=STOP_TYPE_CHOICES, default='SIGHTSEEING')
    order_index = models.PositiveIntegerField(default=1)
    start_time = models.CharField(max_length=50, blank=True, default="09:00 AM", help_text="e.g. 09:00 AM")
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Estimated time spent in minutes")
    activity_description = models.TextField(blank=True)
    travel_note_to_next = models.CharField(max_length=250, blank=True, help_text="e.g. 15 min drive via coastal bypass")
    travel_time_minutes = models.PositiveIntegerField(default=15, help_text="Estimated drive time to next stop")
    map_lat = models.FloatField(null=True, blank=True)
    map_lng = models.FloatField(null=True, blank=True)
    tips = models.TextField(blank=True, help_text="Local insider advice for this stop")

    class Meta:
        ordering = ['order_index']

    @property
    def title(self):
        if self.custom_title:
            return self.custom_title
        if self.destination:
            return self.destination.title
        return f"Stop #{self.order_index}"

    @property
    def latitude(self):
        if self.map_lat:
            return self.map_lat
        if self.destination and self.destination.latitude:
            return self.destination.latitude
        return None

    @property
    def longitude(self):
        if self.map_lng:
            return self.map_lng
        if self.destination and self.destination.longitude:
            return self.destination.longitude
        return None

    def __str__(self):
        return f"{self.day.itinerary.title} - Day {self.day.day_number} - Stop {self.order_index}: {self.title}"


class NFCTag(models.Model):
    """
    Physical smart NFC tag deployed at a hotel, monument, café, or welcome kiosk.
    """
    TAG_TYPE_CHOICES = (
        ('GENERAL', 'General Tourism NFC'),
        ('HOTEL', 'Hotel / Homestay Guest NFC'),
        ('RESTAURANT', 'Restaurant / Food Hub NFC'),
        ('ATTRACTION', 'Monument / Attraction NFC'),
        ('ITINERARY', 'Specific Itinerary NFC'),
        ('EMERGENCY', 'Safety & Emergency NFC'),
        ('FOOD_TRAIL', 'Food Trail NFC'),
    )

    TARGET_EXPERIENCE_CHOICES = (
        ('HOME', 'Companion Home Gateway'),
        ('ITINERARIES', 'Itinerary Navigator'),
        ('NEAR_ME', 'Live GPS Near-Me Radar'),
        ('EXPLORE', 'Explore Hub & Categories'),
        ('EMERGENCY', '1-Click SOS Emergency Hub'),
        ('FOOD_TRAIL', 'Taste of Ratnagiri Food Trail'),
        ('SPECIFIC_ITINERARY', 'Direct Specific Itinerary'),
        ('SPECIFIC_DESTINATION', 'Direct Landmark Brief'),
        ('PARTNER_PAGE', 'Partner Welcome Concierge'),
        ('CUSTOM_URL', 'Custom External/Internal Route'),
    )

    tag_uid = models.CharField(max_length=64, unique=True, db_index=True, help_text="Short unique token, e.g., RATNA-HOTEL-01")
    title = models.CharField(max_length=200, help_text="Descriptive tag name, e.g., Hotel Sea Breeze Room 102")
    tag_type = models.CharField(max_length=30, choices=TAG_TYPE_CHOICES, default='GENERAL', db_index=True)
    target_experience = models.CharField(max_length=30, choices=TARGET_EXPERIENCE_CHOICES, default='HOME')
    custom_url = models.CharField(max_length=255, blank=True, help_text="Target URL path if custom_url is selected")
    
    assigned_partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='nfc_tags')
    assigned_destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='nfc_tags')
    assigned_itinerary = models.ForeignKey(Itinerary, on_delete=models.SET_NULL, null=True, blank=True, related_name='nfc_tags')
    
    custom_welcome_title = models.CharField(max_length=200, blank=True, help_text="e.g. Welcome Guest of Hotel Sea Breeze!")
    custom_welcome_message = models.TextField(blank=True, help_text="Personalized note displayed upon tap")
    
    tap_count = models.PositiveIntegerField(default=0, help_text="Total taps recorded")
    unique_visitor_count = models.PositiveIntegerField(default=0, help_text="Estimated unique sessions")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_tapped_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "NFC Tag"
        verbose_name_plural = "NFC Tags"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-tap_count'], name='nfc_active_taps_idx'),
            models.Index(fields=['tag_type', 'is_active'], name='nfc_type_active_idx'),
        ]

    def __str__(self):
        return f"[{self.tag_uid}] {self.title} ({self.get_tag_type_display()})"

    def get_tap_url(self):
        return reverse('nfc_tap_entry', kwargs={'tag_uid': self.tag_uid})

    def get_qr_url(self):
        return reverse('nfc_qr_view', kwargs={'tag_uid': self.tag_uid})


class NFCTapEvent(models.Model):
    """
    Privacy-safe, zero-PII tap event log for companion telemetry and partner analytics.
    """
    tag = models.ForeignKey(NFCTag, on_delete=models.CASCADE, related_name='tap_events')
    tapped_at = models.DateTimeField(auto_now_add=True, db_index=True)
    session_hash = models.CharField(max_length=64, blank=True, db_index=True, help_text="Anonymous daily session hash")
    device_type = models.CharField(max_length=30, default='Mobile')
    browser_family = models.CharField(max_length=50, blank=True)
    referrer = models.CharField(max_length=255, blank=True)
    action_taken = models.CharField(max_length=100, blank=True, default='tap_opened')

    class Meta:
        ordering = ['-tapped_at']
        indexes = [
            models.Index(fields=['tag', 'session_hash'], name='tap_tag_session_idx'),
            models.Index(fields=['tag', '-tapped_at'], name='tap_tag_tapped_idx'),
            models.Index(fields=['-tapped_at'], name='tap_tapped_at_idx'),
        ]

    def __str__(self):
        return f"Tap on {self.tag.tag_uid} at {self.tapped_at.strftime('%Y-%m-%d %H:%M')}"


class EmergencyContact(models.Model):
    """
    Essential SOS contacts, police, hospitals, and emergency services for Ratnagiri visitors.
    """
    CATEGORY_CHOICES = (
        ('POLICE', 'Police & Coastal Security'),
        ('HOSPITAL', 'Hospital & Medical Emergency (24x7)'),
        ('AMBULANCE', 'Ambulance & Emergency Response'),
        ('FIRE', 'Fire & Rescue'),
        ('TOURIST_HELPLINE', 'Tourist Assistance Helpline'),
        ('COASTAL_POLICE', 'Marine & Coastal Rescue'),
        ('TOWING', 'Vehicle Breakdown & Towing'),
    )

    name = models.CharField(max_length=200, help_text="e.g. Ratnagiri District Civil Hospital")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='HOSPITAL', db_index=True)
    phone_number = models.CharField(max_length=50, help_text="Primary telephone or SOS number (e.g. +91 2352 222333 or 112)")
    alternate_phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_24x7 = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'order'], name='emg_active_order_idx'),
            models.Index(fields=['category', 'is_active'], name='emg_cat_active_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) - {self.phone_number}"


class FAQ(models.Model):
    """
    Frequently Asked Questions for Ratnagiri tourists.
    """
    CATEGORY_CHOICES = (
        ('GENERAL', 'General & Travel Guide'),
        ('TRANSPORT', 'Local Transport & Taxis'),
        ('FOOD', 'Cuisine, Seafood & Mango Season'),
        ('SAFETY', 'Beach Safety & Tides'),
        ('STAY', 'Homestays & Resorts'),
        ('NFC', 'NFC Tag & Companion Guide'),
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='GENERAL', db_index=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['is_published', 'order'], name='faq_pub_order_idx'),
            models.Index(fields=['category', 'is_published'], name='faq_cat_pub_idx'),
        ]

    def __str__(self):
        return self.question


class TravelTip(models.Model):
    """
    Local insider tips, cultural customs, and travel hacks.
    """
    CATEGORY_CHOICES = (
        ('BEST_TIME', 'Best Time & Seasons'),
        ('PACKING', 'What to Pack & Essentials'),
        ('CULTURE', 'Local Etiquette & Marathi Phrases'),
        ('SAVINGS', 'Budget Hacks & Dining Tips'),
        ('PHOTO', 'Photography & Sunset Vantage'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='BEST_TIME', db_index=True)
    icon = models.CharField(max_length=50, default='fa-lightbulb', help_text="FontAwesome icon class, e.g. fa-umbrella-beach")
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'order'], name='tip_active_order_idx'),
        ]

    def __str__(self):
        return self.title


class Announcement(models.Model):
    """
    Live platform announcements, high tide warnings, or festival notices.
    """
    URGENCY_CHOICES = (
        ('INFO', 'Informational Notice'),
        ('WARNING', 'Travel Advisory / Tide Alert'),
        ('CRITICAL', 'Emergency / Heavy Weather Warning'),
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='INFO', db_index=True)
    link_url = models.CharField(max_length=255, blank=True, help_text="Optional target link URL")
    is_active = models.BooleanField(default=True, db_index=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-created_at'], name='ann_active_created_idx'),
        ]

    def __str__(self):
        return f"[{self.get_urgency_level_display()}] {self.title}"


class AdminAuditLog(models.Model):
    """
    Audit log recording all critical operations actions for transparency and safety.
    """
    ACTION_CHOICES = (
        ('CREATE', 'Created Object'),
        ('UPDATE', 'Updated Object'),
        ('DELETE', 'Deleted Object'),
        ('STATUS_CHANGE', 'Status Changed'),
        ('BULK_ACTION', 'Bulk Generated / Batch Action'),
        ('VERIFY', 'Verification Status Changed'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='ops_audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    resource_type = models.CharField(max_length=50, db_index=True, help_text="e.g. Place, Itinerary, NFC Tag, Partner")
    resource_name = models.CharField(max_length=255, blank=True)
    details_json = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        user_name = self.user.username if self.user else "System"
        return f"{user_name} - {self.action} on {self.resource_type} '{self.resource_name}' at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
