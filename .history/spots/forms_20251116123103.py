from django.forms import ModelForm

from  . models import Spots


class SpotsForm(ModelForm):
    class Meta:
        model = Spots
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})