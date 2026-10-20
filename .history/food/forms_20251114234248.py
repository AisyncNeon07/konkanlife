from django.forms import ModelForm

from  . models import Spots

class SpotForm(ModelForm):
    class Meta:
        model = Spots
        fields = 