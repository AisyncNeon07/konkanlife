from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Spots
from .serializers import SpotSerializer
from config.permissions import IsOwnerOrReadOnly


class SpotListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/spots/   → List all spots (paginated, searchable, filterable)
    POST /api/v1/spots/   → Create a new spot (must be logged in)

    Query parameters:
        ?search=beach         → search name & description
        ?category=1           → filter by category ID
        ?ordering=-rating     → sort by rating descending
        ?page=2               → page number
        ?page_size=20         → override items per page
    """
    queryset = (
        Spots.objects
        .select_related('category', 'uploaded_by')  # avoids N+1 on FK lookups
        .prefetch_related('tags')                   # avoids N+1 on M2M lookups
        .order_by('-created_at')
    )
    serializer_class = SpotSerializer

    # Filtering, search, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['rating', 'price', 'distance', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        POST requires authentication.
        GET is public.
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        """
        Called automatically by DRF when a POST is valid.
        Sets the uploaded_by to the logged-in user's profile.
        """
        serializer.save(uploaded_by=self.request.user.profile)


class SpotDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/spots/<uuid>/  → Retrieve a single spot
    PUT    /api/v1/spots/<uuid>/  → Full update (owner only)
    PATCH  /api/v1/spots/<uuid>/  → Partial update (owner only)
    DELETE /api/v1/spots/<uuid>/  → Delete (owner only)
    """
    queryset = (
        Spots.objects
        .select_related('category', 'uploaded_by')
        .prefetch_related('tags')
    )
    serializer_class = SpotSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """Called on PUT/PATCH — don't allow changing the owner."""
        serializer.save(uploaded_by=self.get_object().uploaded_by)
