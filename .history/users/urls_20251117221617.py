from django.urls import path
from . import views
urlpatterns = [
    path('', views.spots_home, name='home_users'),
]   # URL patterns for food a