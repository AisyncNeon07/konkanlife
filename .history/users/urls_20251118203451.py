from django.urls import path
from . import views
urlpatterns = [
    path('', views.users, name='home_users'),
    path('create_users/',views.create_users,name='create_users'),
    path('user_profile', views.user_page , name='user_profile') ,
]   # URL patterns for food a