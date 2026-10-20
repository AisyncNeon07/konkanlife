from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('second/<str:pk>/', views.home2, name='home2'),
]   