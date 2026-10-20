from django.urls import path
from . import views
urlpatterns = [
    path('', views.users, name='home_users'),
    path('users/', views.create_users, name='users')
]   # URL patterns for food a