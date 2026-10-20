from django.urls import path
from . import views.home_view as view
urlpatterns = [
    path('', view.home, name='home'),
    path('about/', view.home2, name='about'),
    path('details/<slug:pk>/', view.home3, name='details'),
]   # URL patterns for food app