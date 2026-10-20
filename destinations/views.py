from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Destination
from .forms import DestinationForm
from reviews.models import Review
from reviews.forms import ReviewForm 

def destination_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    destinations = Destination.objects.filter(is_verified=True).select_related('submitted_by')

    if query:
        destinations = destinations.filter(
            Q(title__icontains=query) | Q(location_name__icontains=query)
        )
    
    if category:
        destinations = destinations.filter(category=category)

    destinations_list = list(destinations)

    context = {
        'destinations': destinations_list,
        'category': category,
        'query': query
    }
    return render(request, 'destinations/destination_list.html', context)

def temples(request):
    destinations = list(Destination.objects.filter(category='Temple', is_verified=True).select_related('submitted_by'))
    context = {
        'destinations': destinations,
        'category': 'Temple',
    }
    return render(request, 'destinations/destination_list.html', context)

@login_required
def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                destination = form.save(commit=False)
                destination.submitted_by = request.user
                destination.is_verified = False # Explicitly set to False
                destination.save()
                return render(request, 'destinations/submission_success.html') # Redirect to a success page or render a success message
            except Exception as e:
                messages.error(request, f"Error saving destination: {str(e)}")
    else:
        form = DestinationForm()
    
    return render(request, 'destinations/destination_form.html', {'form': form})

def destination_detail(request, slug):
    reviews_prefetch = Prefetch(
        'reviews',
        queryset=Review.objects.select_related('user').order_by('-created_at')
    )
    destination = get_object_or_404(
        Destination.objects.select_related('submitted_by').prefetch_related('gallery', reviews_prefetch),
        slug=slug
    )
    reviews = destination.reviews.all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.destination = destination
            if request.user.is_authenticated:
                review.user = request.user
                if not review.author_name:
                    review.author_name = request.user.get_full_name() or request.user.username
            elif not review.author_name:
                review.author_name = 'Anonymous Explorer'
            review.save()
            return redirect('destination_detail', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'destination': destination,
        'reviews': reviews,
        'review_form': form,
    }
    return render(request, 'destinations/destination_detail.html', context)

