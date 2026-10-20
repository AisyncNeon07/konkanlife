from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name='food_home'),
    path('details/<uuid:pk>/', views.home3, name='details'),
    path('create_food/', views.create_food, name='create_food'),
    path('update_food/<uuid:pk>/', views.update_food, name='update_food'),   
    path('delete_food/<uuid:pk>/', views.delete_food, name='delete_food'),   
]   # URL patterns for food app
