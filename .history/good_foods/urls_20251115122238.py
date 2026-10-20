from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='food_home'),
 
]   # URL patterns for good_foods app