from django.urls import path
from food.views import home , home2

urlpatterns = [
    path('', home, name='home'),
    path('second/<str:pk>/', home2, name='home2'),
]   