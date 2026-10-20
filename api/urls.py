"""
Central API router for Konkan Guide REST API (v1).

All API endpoints are prefixed with /api/v1/ from config/urls.py.
Visit /api/v1/ in a browser for the DRF browsable root.
"""
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from spots.api_views import SpotListCreateView, SpotDetailView
from food.api_views import FoodItemListCreateView, FoodItemDetailView


@api_view(['GET'])
def api_root(request, format=None):
    """
    DRF browsable API root — lists all available endpoints.
    Visible at /api/v1/ in your browser.
    """
    return Response({
        '🗺️  spots_list':   reverse('api-spots-list',   request=request, format=format),
        '🗺️  spots_detail':  '/api/v1/spots/<uuid>/',
        '🍽️  food_list':    reverse('api-food-list',    request=request, format=format),
        '🍽️  food_detail':   '/api/v1/food/<uuid>/',
    })


urlpatterns = [
    # API root — browsable in browser at /api/v1/
    path('', api_root, name='api-root'),

    # ── Spots ──────────────────────────────────────────────────────────────
    path('spots/',           SpotListCreateView.as_view(), name='api-spots-list'),
    path('spots/<uuid:pk>/', SpotDetailView.as_view(),     name='api-spots-detail'),

    # ── Food ───────────────────────────────────────────────────────────────
    path('food/',            FoodItemListCreateView.as_view(), name='api-food-list'),
    path('food/<uuid:pk>/',  FoodItemDetailView.as_view(),    name='api-food-detail'),
]
