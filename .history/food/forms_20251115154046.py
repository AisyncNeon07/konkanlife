from django.forms import ModelForm

from  . models import FoodItem 


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        fields = "__all__"
   