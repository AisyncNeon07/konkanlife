from rest_framework import serializers
from .models import Spots, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class SpotSerializer(serializers.ModelSerializer):
    """
    Serializer for the Spots model.

    - On READ  (GET):  returns nested category & tags objects, plus uploader username.
    - On WRITE (POST): accepts category as an ID (integer).
    """
    # Read-only computed fields
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username', read_only=True, default=None
    )

    class Meta:
        model = Spots
        fields = [
            'id',
            'name',
            'description',
            'category',       # accepts category ID on write
            'category_name',  # returned on read (human-readable)
            'tags',
            'rating',
            'price',
            'photo',
            'distance',
            'opening_hours',
            'closing_hours',
            'map_link',
            'uploaded_by_username',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'uploaded_by']

    # ---- Field-level validation ----

    def validate_rating(self, value):
        """Rating must be between 0.0 and 5.0."""
        if not (0.0 <= value <= 5.0):
            raise serializers.ValidationError(
                "Rating must be between 0.0 and 5.0."
            )
        return value

    def validate_price(self, value):
        """Price cannot be negative."""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_distance(self, value):
        """Distance must be positive if provided."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Distance cannot be negative.")
        return value

    # ---- Object-level validation ----

    def validate(self, data):
        """Cross-field validation example: map_link must start with http."""
        map_link = data.get('map_link')
        if map_link and not map_link.startswith('http'):
            raise serializers.ValidationError({
                'map_link': "Map link must be a valid URL starting with http or https."
            })
        return data
