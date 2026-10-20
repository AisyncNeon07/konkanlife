from rest_framework import serializers
from .models import FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the FoodItem model.
    """
    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username', read_only=True, default=None
    )

    class Meta:
        model = FoodItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'rating',
            'photo',
            'best_time_to_eat',
            'uploaded_by_username',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'uploaded_by']

    def validate_rating(self, value):
        if not (0.0 <= value <= 5.0):
            raise serializers.ValidationError("Rating must be between 0.0 and 5.0.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
