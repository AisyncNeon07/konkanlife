from django import forms
from .models import Destination

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['title', 'description', 'category', 'location_name', 'latitude', 'longitude', 'main_image', 'best_time_to_visit', 'travel_tips', 'entry_fees', 'timings']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'travel_tips': forms.Textarea(attrs={'rows': 4}),
        }
