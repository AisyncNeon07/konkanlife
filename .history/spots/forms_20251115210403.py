from django.forms import ModelForm

from  . models import Spots


class SpotsForm(ModelForm):
    class Meta:
        model = Spots
        fields = "__all__"
   