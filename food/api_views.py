from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import FoodItem
from .serializers import FoodItemSerializer
from config.permissions import IsOwnerOrReadOnly

class FoodItemListCreateView(generics.ListCreateAPIView):

    queryset = (
        FoodItem.objects
        .select_related('uploaded_by')
        .order_by('-rating')
    )

    serializer_class = FoodItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['rating', 'price', 'created_at']
    ordering = ['-rating']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # 🔥 THIS IS THE FIX
    def create(self, request, *args, **kwargs):

        # Check if incoming data is list
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(
            data=request.data,
            many=is_many
        )

        serializer.is_valid(raise_exception=True)

        # Save with uploaded_by
        serializer.save(uploaded_by=request.user.profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED )

class FoodItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/food/<uuid>/  → Retrieve a single food item
    PUT    /api/v1/food/<uuid>/  → Full update (owner only)
    PATCH  /api/v1/food/<uuid>/  → Partial update (owner only)
    DELETE /api/v1/food/<uuid>/  → Delete (owner only)
    """
    queryset = FoodItem.objects.select_related('uploaded_by').all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsOwnerOrReadOnly]
