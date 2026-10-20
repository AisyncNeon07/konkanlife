from django.urls import path
from . import views
urlpatterns = [
    path('', views.users, name='home_users'),
]   # URL patterns for food a