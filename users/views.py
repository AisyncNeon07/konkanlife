from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.urls import reverse
from .models import Profile
from .forms import Profileform
from destinations.models import Destination
from spots.models import Spots
from food.models import FoodItem
from reviews.models import Review

# Create your views here.

def build_profile_context(profile):
    user = profile.user
    destination_qs = Destination.objects.filter(submitted_by=user) if user else Destination.objects.none()
    spot_qs = Spots.objects.filter(uploaded_by=profile)
    food_qs = FoodItem.objects.filter(uploaded_by=profile)
    review_qs = Review.objects.filter(user=user).select_related('destination') if user else Review.objects.none()

    destination_count = destination_qs.count()
    spot_count = spot_qs.count()
    food_count = food_qs.count()
    review_count = review_qs.count()
    total_contributions = destination_count + spot_count + food_count
    verified_destination_count = destination_qs.filter(is_verified=True).count()

    average_review_rating = review_qs.aggregate(avg=Avg('rating'))['avg']
    if average_review_rating is not None:
        average_review_rating = round(average_review_rating, 1)

    recent_destinations = list(destination_qs.only('id', 'title', 'slug', 'location_name', 'main_image', 'created_at').order_by('-created_at')[:3])
    recent_spots = list(spot_qs.only('id', 'name', 'description', 'photo', 'created_at').order_by('-created_at')[:3])
    recent_food_items = list(food_qs.only('id', 'name', 'description', 'photo', 'created_at').order_by('-created_at')[:3])
    recent_reviews = list(review_qs.select_related('destination').order_by('-created_at')[:3])

    latest_items = []
    for destination in recent_destinations:
        latest_items.append({
            'timestamp': destination.created_at,
            'url': destination.get_absolute_url(),
            'title': destination.title,
            'subtitle': destination.location_name,
            'label': 'Destination',
            'icon': 'fa-map-marker-alt',
        })
    for spot in recent_spots:
        latest_items.append({
            'timestamp': spot.created_at,
            'url': reverse('details_spots', args=[spot.id]),
            'title': spot.name,
            'subtitle': spot.description or 'A hidden spot shared with the community.',
            'label': 'Hidden Spot',
            'icon': 'fa-map-pin',
        })
    for food in recent_food_items:
        latest_items.append({
            'timestamp': food.created_at,
            'url': reverse('details', args=[food.id]),
            'title': food.name,
            'subtitle': food.description or 'A food story shared with the community.',
            'label': 'Food Story',
            'icon': 'fa-utensils',
        })

    latest_contribution = None
    if latest_items:
        latest_contribution = sorted(latest_items, key=lambda item: item['timestamp'], reverse=True)[0]

    recent_activity = []
    for destination in recent_destinations:
        recent_activity.append({
            'timestamp': destination.created_at,
            'url': destination.get_absolute_url(),
            'title': destination.title,
            'subtitle': destination.location_name,
            'label': 'Destination Added',
            'icon': 'fa-map-marker-alt',
            'photo_url': destination.main_image.url if destination.main_image else None,
        })
    for spot in recent_spots:
        recent_activity.append({
            'timestamp': spot.created_at,
            'url': reverse('details_spots', args=[spot.id]),
            'title': spot.name,
            'subtitle': spot.description or 'A hidden spot from this explorer.',
            'label': 'Spot Shared',
            'icon': 'fa-map-pin',
            'photo_url': spot.photo.url if spot.photo else None,
        })
    for food in recent_food_items:
        recent_activity.append({
            'timestamp': food.created_at,
            'url': reverse('details', args=[food.id]),
            'title': food.name,
            'subtitle': food.description or 'A food story from this explorer.',
            'label': 'Food Shared',
            'icon': 'fa-utensils',
            'photo_url': food.photo.url if food.photo else None,
        })
    for review in recent_reviews:
        dest = review.destination
        recent_activity.append({
            'timestamp': review.created_at,
            'url': dest.get_absolute_url() if dest else '#',
            'title': dest.title if dest else 'Destination',
            'subtitle': review.comment[:100],
            'label': 'Review Written',
            'icon': 'fa-star',
            'photo_url': dest.main_image.url if (dest and dest.main_image) else None,
        })
    recent_activity = sorted(recent_activity, key=lambda item: item['timestamp'], reverse=True)[:5]

    return {
        'profile': profile,
        'total_contributions': total_contributions,
        'destination_count': destination_count,
        'spot_count': spot_count,
        'food_count': food_count,
        'review_count': review_count,
        'verified_destination_count': verified_destination_count,
        'average_review_rating': average_review_rating,
        'recent_destinations': recent_destinations,
        'recent_spots': recent_spots,
        'recent_food_items': recent_food_items,
        'recent_reviews': recent_reviews,
        'recent_activity': recent_activity,
        'latest_contribution': latest_contribution,
    }

def users(request):
    profiles = list(Profile.objects.all()) 
    return render(request, 'users/users.html', {'profiles': profiles})


@login_required
def create_users(request):
    return redirect('edit_profile')


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(
            user=request.user,
            username=request.user.username,
            name=request.user.first_name or request.user.username,
            email=request.user.email
        )
    if request.method == 'POST':
        users_form = Profileform(request.POST, request.FILES, instance=profile)
        if users_form.is_valid():
            try:
                users_form.save()
                return redirect('my_profile')
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
    else:
        users_form = Profileform(instance=profile)
    return render(request, 'users/users_form.html', {"users_form": users_form, "is_edit": True})


def user_page(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    context = build_profile_context(profile)
    return render(request, 'users/user_profile.html', context)


@login_required
def my_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(
            user=request.user,
            username=request.user.username,
            name=request.user.first_name or request.user.username,
            email=request.user.email
        )
    context = build_profile_context(profile)
    return render(request, 'users/user_profile.html', context)