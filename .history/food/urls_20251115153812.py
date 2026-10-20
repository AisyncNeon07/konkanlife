from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('details/<str:pk>/', views.home3, name='details'),
    path('create_food/', views.create_food, name='create_food'),
    path('update_food/<str:pk>/', views.update_food, name='update_food'),   
    path('delete_food/<str:pk>/', views.delete_food, name='delete_food'),   
]   # URL patterns for food app
