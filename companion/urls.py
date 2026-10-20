from django.urls import path
from . import views

urlpatterns = [
    # NFC Tap Gateway & Fallback
    path('t/<str:tag_uid>/', views.nfc_tap_entry, name='nfc_tap_entry'),
    path('t/<str:tag_uid>/qr/', views.nfc_qr_view, name='nfc_qr_view'),

    # Tourist Companion Core Hubs
    path('companion/', views.companion_home, name='companion_home'),
    path('explore/', views.explore_hub_view, name='explore_hub'),
    path('itineraries/', views.itinerary_list, name='itinerary_list'),
    path('itineraries/<slug:slug>/', views.itinerary_detail, name='itinerary_detail'),
    path('near-me/', views.near_me_view, name='near_me'),
    path('my-trip/', views.my_trip_view, name='my_trip'),
    path('my-trip/share/', views.trip_share_view, name='trip_share'),
    path('emergency/', views.emergency_hub_view, name='emergency_hub'),
    path('food-trail/', views.food_trail_view, name='food_trail'),
    path('partners/', views.partner_directory_view, name='partner_directory'),
    path('partners/<slug:slug>/', views.partner_detail_view, name='partner_detail'),

    # Telemetry & Admin Analytics
    path('analytics/', views.analytics_dashboard_view, name='companion_analytics'),
    path('analytics/dashboard/', views.analytics_dashboard_view, name='analytics_dashboard'),
]
