from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.ops_dashboard, name='ops_dashboard'),

    # Places & Destinations CMS
    path('places/', views.places_list, name='ops_places_list'),
    path('places/new/', views.place_create, name='ops_place_create'),
    path('places/<int:pk>/edit/', views.place_edit, name='ops_place_edit'),
    path('places/<int:place_pk>/gallery/<int:gallery_pk>/delete/', views.place_gallery_delete, name='ops_place_gallery_delete'),
    path('places/<int:pk>/verify/', views.place_toggle_verify, name='ops_place_toggle_verify'),
    path('places/<int:pk>/delete/', views.place_delete, name='ops_place_delete'),

    # Itineraries & Builder
    path('itineraries/', views.itineraries_list, name='ops_itineraries_list'),
    path('itineraries/new/', views.itinerary_create, name='ops_itinerary_create'),
    path('itineraries/<int:pk>/edit/', views.itinerary_edit, name='ops_itinerary_edit'),
    path('itineraries/<int:pk>/delete/', views.itinerary_delete, name='ops_itinerary_delete'),
    path('itineraries/<int:pk>/builder/', views.itinerary_builder, name='ops_itinerary_builder'),
    path('itineraries/<int:pk>/days/add/', views.itinerary_add_day, name='ops_itinerary_add_day'),
    path('itineraries/<int:pk>/days/<int:day_id>/delete/', views.itinerary_delete_day, name='ops_itinerary_delete_day'),
    path('itineraries/<int:pk>/days/<int:day_id>/stops/add/', views.itinerary_add_stop, name='ops_itinerary_add_stop'),
    path('itineraries/<int:pk>/stops/<int:stop_id>/delete/', views.itinerary_delete_stop, name='ops_itinerary_delete_stop'),
    path('itineraries/<int:pk>/stops/<int:stop_id>/reorder/<str:direction>/', views.itinerary_reorder_stop, name='ops_itinerary_reorder_stop'),

    # NFC Tag Operations
    path('nfc/', views.nfc_list, name='ops_nfc_list'),
    path('nfc/new/', views.nfc_create, name='ops_nfc_create'),
    path('nfc/<int:pk>/', views.nfc_detail, name='ops_nfc_detail'),
    path('nfc/<int:pk>/delete/', views.nfc_delete, name='ops_nfc_delete'),
    path('nfc/<int:pk>/toggle/', views.nfc_toggle_status, name='ops_nfc_toggle_status'),
    path('nfc/bulk/', views.nfc_bulk_generate, name='ops_nfc_bulk_generate'),
    path('nfc/print/', views.nfc_print_sheet, name='ops_nfc_print_sheet'),
    path('nfc/export/', views.nfc_export_csv, name='ops_nfc_export_csv'),

    # Partners
    path('partners/', views.partners_list, name='ops_partners_list'),
    path('partners/new/', views.partner_create, name='ops_partner_create'),
    path('partners/<int:pk>/edit/', views.partner_edit, name='ops_partner_edit'),
    path('partners/<int:pk>/generate-nfc/', views.partner_generate_nfc, name='ops_partner_generate_nfc'),
    path('partners/<int:pk>/delete/', views.partner_delete, name='ops_partner_delete'),

    # Content & Safety CMS
    path('content/', views.content_hub, name='ops_content_hub'),
    path('content/faqs/new/', views.faq_create, name='ops_faq_create'),
    path('content/faqs/<int:pk>/edit/', views.faq_edit, name='ops_faq_edit'),
    path('content/faqs/<int:pk>/delete/', views.faq_delete, name='ops_faq_delete'),
    path('content/tips/new/', views.tip_create, name='ops_tip_create'),
    path('content/tips/<int:pk>/edit/', views.tip_edit, name='ops_tip_edit'),
    path('content/tips/<int:pk>/delete/', views.tip_delete, name='ops_tip_delete'),
    path('content/emergency/new/', views.emergency_create, name='ops_emergency_create'),
    path('content/emergency/<int:pk>/edit/', views.emergency_edit, name='ops_emergency_edit'),
    path('content/emergency/<int:pk>/delete/', views.emergency_delete, name='ops_emergency_delete'),
    path('content/announcements/new/', views.announcement_create, name='ops_announcement_create'),
    path('content/announcements/<int:pk>/edit/', views.announcement_edit, name='ops_announcement_edit'),
    path('content/announcements/<int:pk>/delete/', views.announcement_delete, name='ops_announcement_delete'),

    # Media Hub
    path('media/', views.media_hub, name='ops_media_hub'),

    # Analytics Intelligence Center
    path('analytics/', views.analytics_center, name='ops_analytics_center'),

    # System & Audit Trail
    path('system/', views.system_hub, name='ops_system_hub'),

    # Global Operations Search
    path('search/', views.global_search, name='ops_global_search'),
]
