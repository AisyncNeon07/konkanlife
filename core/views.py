from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from destinations.models import Destination
from spots.models import Spots
from food.models import FoodItem


def home(request):
    featured_destinations = list(
        Destination.objects.filter(is_verified=True)
        .only('id', 'title', 'slug', 'category', 'location_name', 'main_image', 'description', 'best_time_to_visit', 'is_verified')
        .order_by('-created_at')[:8]
    )
    categories = [c[0] for c in Destination.CATEGORY_CHOICES]
    trending_forts = list(
        Destination.objects.filter(category='Fort', is_verified=True)
        .only('id', 'title', 'slug', 'main_image')[:4]
    )
    featured_spots = list(
        Spots.objects.select_related('category', 'uploaded_by')
        .order_by('-rating')[:6]
    )
    featured_food = list(
        FoodItem.objects.select_related('uploaded_by')
        .order_by('-rating')[:6]
    )

    context = {
        'featured_destinations': featured_destinations,
        'categories': categories,
        'trending_forts': trending_forts,
        'featured_spots': featured_spots,
        'featured_food': featured_food,
    }
    return render(request, 'core/index.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    is_json = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('format') == 'json'

    if query:
        destination_results = list(
            Destination.objects.filter(
                Q(title__icontains=query) | Q(location_name__icontains=query),
                is_verified=True
            ).only('id', 'title', 'slug', 'category', 'location_name', 'main_image', 'description')[:10]
        )

        spot_results = list(
            Spots.objects.filter(name__icontains=query)
            .select_related('category')[:6]
        )
        food_results = list(
            FoodItem.objects.filter(name__icontains=query)
            .select_related('uploaded_by')[:6]
        )
    else:
        destination_results = []
        spot_results = []
        food_results = []

    if is_json:
        data = {
            'query': query,
            'destinations': [
                {
                    'id': d.id,
                    'title': d.title,
                    'url': reverse('destination_detail', kwargs={'slug': d.slug}),
                    'category': d.category,
                    'location': d.location_name,
                    'image': d.main_image.url if d.main_image else '/static/images/default_destination.jpg'
                }
                for d in destination_results
            ],
            'spots': [
                {
                    'id': str(s.id),
                    'title': s.name,
                    'url': reverse('details_spots', kwargs={'pk': s.id}),
                    'image': s.photo.url if s.photo else '/static/images/default_spot.jpg'
                }
                for s in spot_results
            ],
            'food': [
                {
                    'id': str(f.id),
                    'title': f.name,
                    'url': reverse('details', kwargs={'pk': f.id}),
                    'image': f.photo.url if f.photo else '/static/images/default_food.jpg'
                }
                for f in food_results
            ]
        }
        return JsonResponse(data)

    context = {
        'query': query,
        'destination_results': destination_results,
        'spot_results': spot_results,
        'food_results': food_results,
    }
    return render(request, 'core/search_results.html', context)
