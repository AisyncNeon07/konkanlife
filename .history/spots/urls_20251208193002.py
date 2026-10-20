from django.urls import path
from . import views
urlpatterns = [
    path('home', views.spots_home, name='home_spots'),
    path('details/<uuid:pk>/', views.home3, name='details_spots'),
    path('create_spot/', views.create_spot, name='create_spot'),
    path('update_spot/<uuid:pk>/', views.update_spot, name='update_spot'),   
    path('delete_spot/<uuid:pk>/', views.delete_spot, name='delete_spot'),   
]   # URL patterns for food app
