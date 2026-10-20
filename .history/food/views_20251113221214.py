
from django.shortcuts import render
from django.http import HttpResponse    
from .data.spots import foods, spots
# Create your views here.



context = {
        'foods': foods,
        'spots': spots
    }

def home(request):
    return render(request, 'food/index.html', context)

def home2(request):
    return render(request, 'food/about.html', {"spots":spots})

def home3(request ,pk):
    item = None
    for i in spots:
        if str(i['id']) == pk:
            item = i
            break
    return render(request, 'food/details.html', {"spot":item})

from django.shortcuts import render, get_object_or_404
from .models import Spot, Category, Tag

def spot_list(request):
    spots = Spot.objects.select_related("category").prefetch_related("tags", "photos")[:100]
    return render(request, "spots/list.html", {"spots": spots})

def spot_detail(request, pk):
    spot = get_object_or_404(Spot.objects.prefetch_related("photos", "reviews__user", "tags"), pk=pk)
    return render(request, "spots/detail.html", {"spot": spot})

def category_spots(request, category_slug):
    cat = get_object_or_404(Category, name=category_slug)   # or slugify & store slug
    spots = cat.spots.all()
    return render(request, "spots/category.html", {"category": cat, "spots": spots})

def tag_spots(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    spots = tag.spots.all()
    return render(request, "spots/tag.html", {"tag": tag, "spots": spots})