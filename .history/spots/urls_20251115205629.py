from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('details/<uuid:pk>/', views.home3, name='details'),
    path('create_spot/', views.create_food, name='create_spot'),
    path('update_spot/<uuid:pk>/', views.update_food, name='update_spot'),   
    path('delete_spot/<uuid:pk>/', views.delete_food, name='delete_spot'),   
]   # URL patterns for food app
