from django.forms import ModelForm

from  . models import FoodItem 


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        exclude = ['uploaded_by']
   