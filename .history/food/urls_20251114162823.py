from django.urls import path
from . views import home_view 
urlpatterns = [
    path('', home_view.home, name='home'),
    path('about/', home_view.home2, name='about'),
    path('details/<uuid:pk>/', home_view.home3, name='details'),
]   # URL patterns for food app