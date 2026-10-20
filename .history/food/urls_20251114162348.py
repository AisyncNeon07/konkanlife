from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.home2, name='about'),
    path('details/<slug:pk>/', views.home3, name='details'),
]   # URL patterns for food app