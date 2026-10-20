from django.forms import ModelForm

from  . models import Profile


class Profileform(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
   