from django.forms import ModelForm

from  . models import Spots , spot_info

class SpotForm(ModelForm):
    class Meta:
        model = Spots
        fields = "__all__"
class spot_infoForm(ModelForm):
    class Meta:
        model = spot_info
        fields = ["description", "map_location", "opening_hours", "closing_hours"]