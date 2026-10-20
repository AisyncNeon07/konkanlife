from django.forms import ModelForm

from  . models import FoodItem , FoodInfo


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        fields = "__all__"
class FoodInfoForm(ModelForm):
    class Meta:
        model = FoodInfo
        fields = "__all__"