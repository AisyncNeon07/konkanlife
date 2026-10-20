from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'comment']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (optional)'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Share your experience...'}),
        }

