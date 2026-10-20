from django.urls import path
from . import views
urlpatterns = [
    path('', home, name='home'),
    path('second/<str:pk>/', home2, name='home2'),
]   