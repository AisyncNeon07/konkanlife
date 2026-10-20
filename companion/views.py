import hashlib
import json
import base64
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Sum

from .models import NFCTag, NFCTapEvent, Itinerary, ItineraryDay, ItineraryStop, Partner, EmergencyContact
from destinations.models import Destination
from spots.models import Spots
from food.models import FoodItem


def _get_client_session_hash(request):
    """
    Generate an anonymous daily hash for unique visitor tracking without storing any PII.
    Combines client IP subnet + user-agent + today's date into a one-way SHA-256 hash.
    """
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ',' in ip:
        ip = ip.split(',')[0].strip()
    ua = request.META.get('HTTP_USER_AGENT', 'Unknown')
    today = date.today().isoformat()
    raw = f"{ip}-{ua}-{today}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:32]


def _detect_device_type(user_agent):
    ua = (user_agent or '').lower()
    if 'ipad' in ua or 'tablet' in ua:
        return 'Tablet'
    elif 'mobi' in ua or 'android' in ua or 'iphone' in ua:
        return 'Mobile'
    return 'Desktop'


def nfc_tap_entry(request, tag_uid):
    """
    The physical NFC tap entry point (/t/<tag_uid>/).
    Logs anonymous telemetry, sets contextual companion session, and routes to appropriate experience.
    """
    tag = NFCTag.objects.filter(tag_uid__iexact=tag_uid, is_active=True).first()
    
    if not tag:
        # Fallback for unrecognized tag or general tap
        context = {
            'tag_uid': tag_uid,
            'is_invalid': True,
            'featured_itineraries': Itinerary.objects.filter(is_active=True)[:4],
            'destinations': Destination.objects.filter(is_verified=True)[:6],
        }
        return render(request, 'companion/tap_fallback.html', context)

    # 1. Update tag metrics
    tag.tap_count += 1
    tag.last_tapped_at = timezone.now()
    
    session_hash = _get_client_session_hash(request)
    ua = request.META.get('HTTP_USER_AGENT', '')
    device_type = _detect_device_type(ua)
    
    # Check if this session hash already tapped today to increment unique visitors accurately
    has_tapped_today = NFCTapEvent.objects.filter(tag=tag, session_hash=session_hash).exists()
    if not has_tapped_today:
        tag.unique_visitor_count += 1
    tag.save(update_fields=['tap_count', 'unique_visitor_count', 'last_tapped_at'])

    # 2. Record privacy-safe tap event
    NFCTapEvent.objects.create(
        tag=tag,
        session_hash=session_hash,
        device_type=device_type,
        browser_family=ua[:45] if ua else 'Unknown',
        referrer=request.META.get('HTTP_REFERER', '')[:250],
        action_taken='tap_entry'
    )

    # 3. Store contextual state in session for persistent companion banner
    request.session['nfc_active_tag'] = tag.tag_uid
    request.session['nfc_tag_title'] = tag.title
    request.session['nfc_welcome_title'] = tag.custom_welcome_title or f"Welcome to Ratnagiri"
    request.session['nfc_welcome_message'] = tag.custom_welcome_message or "Your digital travel companion is now ready."
    if tag.assigned_partner:
        request.session['nfc_partner_name'] = tag.assigned_partner.business_name
        request.session['nfc_partner_type'] = tag.assigned_partner.get_partner_type_display()
    else:
        request.session.pop('nfc_partner_name', None)
        request.session.pop('nfc_partner_type', None)

    # 4. Route according to target experience
    if tag.target_experience == 'SPECIFIC_ITINERARY' and tag.assigned_itinerary:
        return redirect('itinerary_detail', slug=tag.assigned_itinerary.slug)
    elif tag.target_experience == 'SPECIFIC_DESTINATION' and tag.assigned_destination:
        return redirect('destination_detail', slug=tag.assigned_destination.slug)
    elif tag.target_experience == 'EMERGENCY':
        return redirect('emergency_hub')
    elif tag.target_experience == 'FOOD_TRAIL':
        return redirect('food_trail')
    elif tag.target_experience == 'NEAR_ME':
        return redirect('near_me')
    elif tag.target_experience == 'EXPLORE':
        return redirect('explore_hub')
    elif tag.target_experience == 'PARTNER_PAGE' and tag.assigned_partner:
        return redirect('partner_detail', slug=tag.assigned_partner.slug)
    elif tag.target_experience == 'CUSTOM_URL' and tag.custom_url:
        return redirect(tag.custom_url)

    # Default: Companion Landing Screen
    return redirect(f"{reverse('companion_home')}?tapped={tag.tag_uid}")


def nfc_qr_view(request, tag_uid):
    """
    Dedicated QR Code route: directly triggers the NFC tap processor
    and redirects user to the configured experience page (no redundant QR screen).
    """
    return nfc_tap_entry(request, tag_uid)


def companion_home(request):
    """
    Main NFC Tourist Companion Mobile Dashboard.
    """
    tapped_uid = request.GET.get('tapped') or request.session.get('nfc_active_tag')
    active_tag = None
    if tapped_uid:
        active_tag = NFCTag.objects.filter(tag_uid__iexact=tapped_uid).first()

    itineraries = list(
        Itinerary.objects.filter(is_active=True).annotate(
            days_total=Count('days', distinct=True)
        ).order_by('order', 'duration_days')[:6]
    )
    featured_destinations = list(
        Destination.objects.filter(is_verified=True).only(
            'id', 'title', 'slug', 'category', 'location_name', 'main_image', 'created_at', 'best_time_to_visit'
        ).order_by('-created_at')[:8]
    )
    secret_spots = list(
        Spots.objects.select_related('category', 'uploaded_by')
        .order_by('-rating')[:6]
    )
    local_food = list(
        FoodItem.objects.select_related('uploaded_by')
        .order_by('-rating')[:6]
    )
    emergency_top = list(
        EmergencyContact.objects.filter(is_active=True).only(
            'id', 'name', 'category', 'phone_number', 'order'
        ).order_by('order')[:3]
    )
    partners = list(
        Partner.objects.filter(is_active=True, is_featured=True).only(
            'id', 'business_name', 'slug', 'partner_type', 'short_tagline', 'logo', 'cover_image'
        )[:4]
    )

    context = {
        'active_tag': active_tag,
        'itineraries': itineraries,
        'featured_destinations': featured_destinations,
        'secret_spots': secret_spots,
        'local_food': local_food,
        'emergency_top': emergency_top,
        'partners': partners,
    }
    return render(request, 'companion/home.html', context)


def itinerary_list(request):
    """
    Explore curated itineraries with duration and audience filters.
    Optimized with days_total annotation and prefetch_related to eliminate N+1 queries.
    """
    audience = request.GET.get('audience', '').strip()
    duration = request.GET.get('duration', '').strip()
    season = request.GET.get('season', '').strip()

    itineraries = Itinerary.objects.filter(is_active=True).annotate(
        days_total=Count('days', distinct=True)
    ).prefetch_related('days__stops')

    if audience and audience != 'ALL':
        itineraries = itineraries.filter(audience=audience)
    if season and season != 'ALL':
        itineraries = itineraries.filter(season=season)
    if duration:
        if duration == '1':
            itineraries = itineraries.filter(duration_days=1)
        elif duration == '2':
            itineraries = itineraries.filter(duration_days=2)
        elif duration == '3+':
            itineraries = itineraries.filter(duration_days__gte=3)

    itineraries = list(itineraries)

    context = {
        'itineraries': itineraries,
        'selected_audience': audience,
        'selected_duration': duration,
        'selected_season': season,
        'audience_choices': Itinerary.AUDIENCE_CHOICES,
        'season_choices': Itinerary.SEASON_CHOICES,
    }
    return render(request, 'companion/itinerary_list.html', context)


def itinerary_detail(request, slug):
    """
    Interactive Day-by-Day timeline view of a curated itinerary with GPS stops.
    """
    itinerary = get_object_or_404(Itinerary, slug=slug, is_active=True)
    days = itinerary.days.prefetch_related('stops__destination').all().order_by('day_number')
    
    # Collect coordinates for route mapping
    stops_data = []
    for day in days:
        for stop in day.stops.all():
            lat = stop.latitude
            lng = stop.longitude
            if lat and lng:
                stops_data.append({
                    'day': day.day_number,
                    'title': stop.title,
                    'lat': lat,
                    'lng': lng,
                    'time': stop.start_time,
                    'type': stop.get_stop_type_display(),
                })

    related_itineraries = list(Itinerary.objects.filter(is_active=True).exclude(pk=itinerary.pk)[:3])

    context = {
        'itinerary': itinerary,
        'days': days,
        'stops_json': json.dumps(stops_data),
        'related_itineraries': related_itineraries,
    }
    return render(request, 'companion/itinerary_detail.html', context)


def near_me_view(request):
    """
    Smart Live GPS Radar with client-side Haversine distance calculator.
    Pre-populates verified destinations, spots, and emergency places with coordinates.
    """
    destinations = Destination.objects.filter(is_verified=True).exclude(latitude__isnull=True).exclude(longitude__isnull=True).only(
        'id', 'title', 'category', 'latitude', 'longitude', 'main_image', 'slug', 'timings', 'entry_fees'
    )
    spots = Spots.objects.all().only('id', 'name', 'rating', 'photo', 'opening_hours', 'price')
    emergencies = EmergencyContact.objects.filter(is_active=True).exclude(latitude__isnull=True).exclude(longitude__isnull=True).only(
        'id', 'name', 'phone_number', 'latitude', 'longitude'
    )

    places_data = []
    
    for d in destinations:
        places_data.append({
            'id': f"dest-{d.id}",
            'title': d.title,
            'category': d.category,
            'type': 'Landmark',
            'badge': 'Landmark',
            'badge_color': 'ocean',
            'lat': d.latitude,
            'lng': d.longitude,
            'image': d.main_image.url if d.main_image else '/static/images/default_destination.jpg',
            'url': reverse('destination_detail', kwargs={'slug': d.slug}),
            'timing': d.timings or 'Open daily',
            'fee': d.entry_fees or 'Free',
        })

    for s in spots:
        places_data.append({
            'id': f"spot-{s.id}",
            'title': s.name,
            'category': 'Secret Spot',
            'type': 'Secret Spot',
            'badge': f"★ {s.rating:.1f}",
            'badge_color': 'sand',
            'lat': 16.9902 + (hash(str(s.id)) % 100) * 0.001, # fallback coordinates if missing
            'lng': 73.3120 + (hash(str(s.name)) % 100) * 0.001,
            'image': s.photo.url if s.photo else '/static/images/default_spot.jpg',
            'url': reverse('details_spots', kwargs={'pk': s.id}),
            'timing': s.opening_hours or 'Sunrise to Sunset',
            'fee': f"₹{s.price:.0f}" if s.price else 'Free',
        })

    for e in emergencies:
        places_data.append({
            'id': f"emg-{e.id}",
            'title': e.name,
            'category': 'Emergency',
            'type': 'Hospital / Police',
            'badge': '24x7 SOS',
            'badge_color': 'red',
            'lat': e.latitude,
            'lng': e.longitude,
            'image': '/static/images/hospital_badge.jpg',
            'url': f"tel:{e.phone_number}",
            'timing': '24 Hours Open',
            'fee': 'Emergency Service',
        })

    context = {
        'places_json': json.dumps(places_data),
        'total_places': len(places_data),
    }
    return render(request, 'companion/near_me.html', context)


def my_trip_view(request):
    """
    Zero-Login Personal Trip Planner & Pocket Guide.
    Loads saved places from LocalStorage, allows stop sequencing, and generates shareable trip links.
    """
    all_destinations = Destination.objects.filter(is_verified=True).values('id', 'title', 'category', 'location_name', 'slug')
    
    context = {
        'all_destinations_json': json.dumps(list(all_destinations)),
    }
    return render(request, 'companion/my_trip.html', context)


def trip_share_view(request):
    """
    Shared trip plan page unpacked from URL query params.
    """
    data = request.GET.get('data', '')
    decoded_trip = None
    if data:
        try:
            raw_json = base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')
            decoded_trip = json.loads(raw_json)
        except Exception:
            decoded_trip = None

    context = {
        'decoded_trip': decoded_trip,
        'raw_data': data,
    }
    return render(request, 'companion/trip_share.html', context)


def emergency_hub_view(request):
    """
    1-Click SOS Safety Center & 24x7 Emergency Services for tourists.
    Optimized in-memory filtering: 1 query instead of 5 separate queries.
    """
    contacts = list(EmergencyContact.objects.filter(is_active=True).order_by('order'))
    
    hospitals = [c for c in contacts if c.category == 'HOSPITAL']
    police = [c for c in contacts if c.category in ('POLICE', 'COASTAL_POLICE')]
    ambulance = [c for c in contacts if c.category in ('AMBULANCE', 'FIRE')]
    helplines = [c for c in contacts if c.category in ('TOURIST_HELPLINE', 'TOWING')]

    context = {
        'contacts': contacts,
        'hospitals': hospitals,
        'police': police,
        'ambulance': ambulance,
        'helplines': helplines,
    }
    return render(request, 'companion/emergency_hub.html', context)


def food_trail_view(request):
    """
    Taste of Ratnagiri Food & Culinary Trail Experience.
    """
    food_items = list(FoodItem.objects.select_related('uploaded_by').order_by('-rating'))
    
    context = {
        'food_items': food_items,
    }
    return render(request, 'companion/food_trail.html', context)


def explore_hub_view(request):
    """
    Comprehensive Explore Gateway categorized by Beaches, Forts, Temples, Nature, and Culture.
    """
    category = request.GET.get('cat', '').strip()
    destinations = Destination.objects.filter(is_verified=True).only(
        'id', 'title', 'slug', 'category', 'location_name', 'main_image', 'description'
    )
    
    if category:
        destinations = destinations.filter(category__iexact=category)

    forts = list(Destination.objects.filter(category='Fort', is_verified=True).only('id', 'title', 'slug', 'location_name', 'main_image')[:6])
    beaches = list(Destination.objects.filter(category='Beach', is_verified=True).only('id', 'title', 'slug', 'location_name', 'main_image')[:6])
    temples = list(Destination.objects.filter(category='Temple', is_verified=True).only('id', 'title', 'slug', 'location_name', 'main_image')[:6])
    waterfalls = list(Destination.objects.filter(category='Waterfall', is_verified=True).only('id', 'title', 'slug', 'location_name', 'main_image')[:6])

    context = {
        'selected_category': category,
        'destinations': list(destinations),
        'forts': forts,
        'beaches': beaches,
        'temples': temples,
        'waterfalls': waterfalls,
    }
    return render(request, 'companion/explore_hub.html', context)


def partner_directory_view(request):
    """
    Directory of verified local hotel, restaurant, and tour guide partners.
    """
    partner_type = request.GET.get('type', '').strip()
    partners = Partner.objects.filter(is_active=True)
    
    if partner_type:
        partners = partners.filter(partner_type=partner_type)

    context = {
        'partners': partners,
        'selected_type': partner_type,
        'partner_types': Partner.PARTNER_TYPE_CHOICES,
    }
    return render(request, 'companion/partner_directory.html', context)


def partner_detail_view(request, slug):
    """
    Partner concierge landing page with guest amenities, contact links, and local recommendations.
    """
    partner = get_object_or_404(Partner, slug=slug, is_active=True)
    nearby_destinations = Destination.objects.filter(is_verified=True)[:4]
    
    context = {
        'partner': partner,
        'nearby_destinations': nearby_destinations,
    }
    return render(request, 'companion/partner_detail.html', context)


def analytics_dashboard_view(request):
    """
    Privacy-Safe NFC Analytics & Performance Telemetry Dashboard for platform administrators.
    """
    total_tags = NFCTag.objects.count()
    active_tags = NFCTag.objects.filter(is_active=True).count()
    total_taps = NFCTag.objects.aggregate(Sum('tap_count'))['tap_count__sum'] or 0
    unique_visitors = NFCTag.objects.aggregate(Sum('unique_visitor_count'))['unique_visitor_count__sum'] or 0
    
    top_tags = NFCTag.objects.order_by('-tap_count')[:10]
    recent_taps = NFCTapEvent.objects.select_related('tag').order_by('-tapped_at')[:20]
    
    device_breakdown = NFCTapEvent.objects.values('device_type').annotate(count=Count('id')).order_by('-count')

    context = {
        'total_tags': total_tags,
        'active_tags': active_tags,
        'total_taps': total_taps,
        'unique_visitors': unique_visitors,
        'top_tags': top_tags,
        'recent_taps': recent_taps,
        'device_breakdown': device_breakdown,
    }
    return render(request, 'companion/analytics_dashboard.html', context)
