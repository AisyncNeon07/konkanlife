from django.forms import ModelForm
from django import forms
from .models import Profile


class Profileform(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'short_intro',
            'bio',
            'profile_image',
            'social_github',
            'social_twitter',
            'social_linkedin',
            'social_youtube',
            'social_website',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})

   