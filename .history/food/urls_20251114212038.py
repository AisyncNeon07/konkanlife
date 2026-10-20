from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.home2, name='about'),
    path('details/<str:pk>/', views.home3, name='details'),
    path('create-spot/', views.create_spot, name='create_spot'),
]   # URL patterns for food app