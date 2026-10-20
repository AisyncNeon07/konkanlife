from django import forms
from destinations.models import Destination, Gallery
from companion.models import (
    Itinerary, ItineraryDay, ItineraryStop,
    NFCTag, Partner, EmergencyContact,
    FAQ, TravelTip, Announcement
)


class DestinationForm(forms.ModelForm):
    main_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-file-ops'}))
    class Meta:
        model = Destination
        fields = [
            'title', 'category', 'location_name', 'latitude', 'longitude',
            'description', 'best_time_to_visit', 'travel_tips', 'entry_fees',
            'timings', 'is_verified', 'main_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Ratnadurg Fort (Bhagwati Durg)'}),
            'category': forms.Select(attrs={'class': 'form-select-ops'}),
            'location_name': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Killa, Ratnagiri'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input-ops', 'placeholder': '16.9856', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input-ops', 'placeholder': '73.2678', 'step': 'any'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 4, 'placeholder': 'Comprehensive historical and cultural description...'}),
            'best_time_to_visit': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Oct - March (Sunset 5:30 PM)'}),
            'travel_tips': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 3, 'placeholder': 'Insider tips for shoes, photography, safety...'}),
            'entry_fees': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Free or ?20 per adult'}),
            'timings': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. 06:00 AM - 07:00 PM'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-file-ops'}),
        }


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = [
            'title', 'tagline', 'description', 'duration_days', 'audience',
            'season', 'difficulty', 'estimated_cost_inr', 'total_distance_km',
            'is_featured', 'is_active', 'order', 'cover_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. 2-Day Essential Ratnagiri Discovery'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Sea forts, tranquil beaches and authentic Malvani thalis'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 4}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-input-ops', 'min': 1, 'max': 14}),
            'audience': forms.Select(attrs={'class': 'form-select-ops'}),
            'season': forms.Select(attrs={'class': 'form-select-ops'}),
            'difficulty': forms.Select(attrs={'class': 'form-select-ops'}),
            'estimated_cost_inr': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. ?1,500 - ?3,000 / day'}),
            'total_distance_km': forms.NumberInput(attrs={'class': 'form-input-ops', 'step': '0.1'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'order': forms.NumberInput(attrs={'class': 'form-input-ops'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-file-ops'}),
        }


class ItineraryDayForm(forms.ModelForm):
    class Meta:
        model = ItineraryDay
        fields = ['day_number', 'title', 'summary', 'order']
        widgets = {
            'day_number': forms.NumberInput(attrs={'class': 'form-input-ops', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Coastal Forts & Sunset Horizons'}),
            'summary': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 2, 'placeholder': 'Brief theme for this day...'}),
            'order': forms.NumberInput(attrs={'class': 'form-input-ops'}),
        }


class ItineraryStopForm(forms.ModelForm):
    class Meta:
        model = ItineraryStop
        fields = [
            'destination', 'custom_title', 'stop_type', 'order_index',
            'start_time', 'duration_minutes', 'activity_description',
            'travel_note_to_next', 'travel_time_minutes', 'tips'
        ]
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-select-ops'}),
            'custom_title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'Custom title (e.g. Authentic Malvani Lunch)'}),
            'stop_type': forms.Select(attrs={'class': 'form-select-ops'}),
            'order_index': forms.NumberInput(attrs={'class': 'form-input-ops', 'min': 1}),
            'start_time': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': '09:00 AM'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input-ops', 'min': 5, 'step': 5}),
            'activity_description': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 2, 'placeholder': 'What to do during this stop...'}),
            'travel_note_to_next': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. 15 min drive via coastal bypass'}),
            'travel_time_minutes': forms.NumberInput(attrs={'class': 'form-input-ops', 'min': 0}),
            'tips': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 2, 'placeholder': 'Insider advice...'}),
        }


class NFCTagForm(forms.ModelForm):
    class Meta:
        model = NFCTag
        fields = [
            'tag_uid', 'title', 'tag_type', 'target_experience', 'custom_url',
            'assigned_partner', 'assigned_destination', 'assigned_itinerary',
            'custom_welcome_title', 'custom_welcome_message', 'is_active'
        ]
        widgets = {
            'tag_uid': forms.TextInput(attrs={'class': 'form-input-ops font-mono uppercase', 'placeholder': 'e.g. HOTEL-OCEAN-01'}),
            'title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Ocean Breeze Room 204 NFC Tag'}),
            'tag_type': forms.Select(attrs={'class': 'form-select-ops'}),
            'target_experience': forms.Select(attrs={'class': 'form-select-ops'}),
            'custom_url': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': '/destinations/ratnadurg-fort/'}),
            'assigned_partner': forms.Select(attrs={'class': 'form-select-ops'}),
            'assigned_destination': forms.Select(attrs={'class': 'form-select-ops'}),
            'assigned_itinerary': forms.Select(attrs={'class': 'form-select-ops'}),
            'custom_welcome_title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'Welcome Guest of Ocean Breeze ??'}),
            'custom_welcome_message': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 3, 'placeholder': 'Personalized greeting shown when tapped...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
        }


class BulkNFCTagForm(forms.Form):
    prefix = forms.CharField(
        max_length=30,
        initial='HOTEL-ROOM-',
        widget=forms.TextInput(attrs={'class': 'form-input-ops font-mono uppercase', 'placeholder': 'e.g. HOTEL-OCEAN-'}),
        help_text='Prefix for generated tag tokens (e.g. HOTEL-OCEAN- will generate HOTEL-OCEAN-01, HOTEL-OCEAN-02...)'
    )
    start_number = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-input-ops'}),
        help_text='Starting sequence number'
    )
    count = forms.IntegerField(
        initial=10,
        min_value=1,
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-input-ops'}),
        help_text='Number of tags to generate (1 to 200)'
    )
    tag_type = forms.ChoiceField(
        choices=NFCTag.TAG_TYPE_CHOICES,
        initial='HOTEL',
        widget=forms.Select(attrs={'class': 'form-select-ops'})
    )
    target_experience = forms.ChoiceField(
        choices=NFCTag.TARGET_EXPERIENCE_CHOICES,
        initial='HOME',
        widget=forms.Select(attrs={'class': 'form-select-ops'})
    )
    assigned_partner = forms.ModelChoiceField(
        queryset=Partner.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select-ops'})
    )
    custom_welcome_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'Welcome Hotel Guest!'})
    )
    custom_welcome_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 2, 'placeholder': 'Your digital companion is ready to guide your stay.'})
    )


class PartnerForm(forms.ModelForm):
    generate_nfc = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
        label="Auto-generate Smart NFC Tag & QR Code for this Partner"
    )

    class Meta:
        model = Partner
        fields = [
            'business_name', 'partner_type', 'short_tagline', 'description',
            'logo', 'cover_image', 'address', 'phone', 'whatsapp',
            'email', 'website', 'google_maps_url', 'latitude', 'longitude',
            'exclusive_offer', 'offer_code', 'amenities', 'operating_hours',
            'price_range', 'instagram_handle',
            'is_verified', 'is_featured', 'is_active'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Ocean Breeze Beach Resort'}),
            'partner_type': forms.Select(attrs={'class': 'form-select-ops'}),
            'short_tagline': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Beachfront luxury stay in Ganpatipule'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 3, 'placeholder': 'Detailed overview of hotel rooms, dining, hospitality & amenities...'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-file-ops'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-file-ops'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 2, 'placeholder': 'Physical road address, landmark, village/city...'}),
            'phone': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': '+91 98765 43210'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': '+91 98765 43210'}),
            'email': forms.EmailInput(attrs={'class': 'form-input-ops', 'placeholder': 'contact@oceanbreeze.in'}),
            'website': forms.URLInput(attrs={'class': 'form-input-ops', 'placeholder': 'https://oceanbreeze.in'}),
            'google_maps_url': forms.URLInput(attrs={'class': 'form-input-ops', 'placeholder': 'https://maps.app.goo.gl/... or Google Maps share link'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input-ops', 'step': 'any', 'placeholder': 'Optional (e.g. 16.9856)'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input-ops', 'step': 'any', 'placeholder': 'Optional (e.g. 73.2678)'}),
            'exclusive_offer': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. 10% Off on Food / Complimentary Welcome Drink for Explorers'}),
            'offer_code': forms.TextInput(attrs={'class': 'form-input-ops font-mono uppercase', 'placeholder': 'e.g. KONKAN10'}),
            'amenities': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'Free Wi-Fi, Beach View, AC, Parking, Malvani Seafood, Swimming Pool'}),
            'operating_hours': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Check-in 12:00 PM / Check-out 10:00 AM'}),
            'price_range': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. ?1,500 - ?3,500 / night or ?? Moderate'}),
            'instagram_handle': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. @oceanbreeze_konkan'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
        }


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = [
            'name', 'category', 'phone_number', 'alternate_phone',
            'address', 'latitude', 'longitude', 'is_24x7', 'is_active', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Civil Hospital Emergency Ward'}),
            'category': forms.Select(attrs={'class': 'form-select-ops'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': '112 or +91 2352 222333'}),
            'alternate_phone': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'Optional second number'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 2}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input-ops', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input-ops', 'step': 'any'}),
            'is_24x7': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'order': forms.NumberInput(attrs={'class': 'form-input-ops'}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'order', 'is_published']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. When is the best time to visit Ratnagiri for Alphonso Mangoes?'}),
            'answer': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select-ops'}),
            'order': forms.NumberInput(attrs={'class': 'form-input-ops'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
        }


class TravelTipForm(forms.ModelForm):
    class Meta:
        model = TravelTip
        fields = ['title', 'content', 'category', 'icon', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Monsoon Sea Swimming Warning'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select-ops'}),
            'icon': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'fa-triangle-exclamation'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'order': forms.NumberInput(attrs={'class': 'form-input-ops'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'urgency_level', 'link_url', 'is_active', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'e.g. Ratnagiri Mango Festival 2026 Starting This Weekend'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea-ops', 'rows': 3}),
            'urgency_level': forms.Select(attrs={'class': 'form-select-ops'}),
            'link_url': forms.TextInput(attrs={'class': 'form-input-ops', 'placeholder': 'https://... or /itineraries/...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox-ops'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-input-ops', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-input-ops', 'type': 'datetime-local'}),
        }
