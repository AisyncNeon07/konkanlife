from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('details/<str:pk>/', views.home3, name='details'),
]   