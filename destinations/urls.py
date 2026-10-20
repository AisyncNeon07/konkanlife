from django.urls import path
from . import views

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('temples/', views.temples, name='temples'),
    path('create/', views.create_destination, name='create_destination'),
    path('<slug:slug>/', views.destination_detail, name='destination_detail'),
]
