import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.utils.text import slugify

from destinations.models import Destination, Gallery
from companion.models import (
    Itinerary, ItineraryDay, ItineraryStop,
    NFCTag, NFCTapEvent, Partner, EmergencyContact,
    FAQ, TravelTip, Announcement, AdminAuditLog
)
from .forms import (
    DestinationForm, ItineraryForm, ItineraryDayForm, ItineraryStopForm,
    NFCTagForm, BulkNFCTagForm, PartnerForm, EmergencyContactForm,
    FAQForm, TravelTipForm, AnnouncementForm
)
from .services import (
    log_audit_action, get_operations_stats, get_chart_analytics,
    generate_bulk_tags, export_nfc_csv
)


def staff_required(view_func):
    """Decorator requiring authenticated staff user."""
    decorated = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated


# ==============================================================================
# 1. OPERATIONS DASHBOARD
# ==============================================================================

@staff_required
def ops_dashboard(request):
    stats = get_operations_stats()
    charts = get_chart_analytics(days=14)
    recent_logs = AdminAuditLog.objects.select_related('user')[:10]
    recent_taps = NFCTapEvent.objects.select_related('tag')[:8]

    context = {
        'page_title': 'Operations Dashboard',
        'active_nav': 'dashboard',
        'stats': stats,
        'charts': charts,
        'recent_logs': recent_logs,
        'recent_taps': recent_taps,
    }
    return render(request, 'ops/dashboard.html', context)


# ==============================================================================
# 2. PLACES & DESTINATIONS CMS
# ==============================================================================

@staff_required
def places_list(request):
    category = request.GET.get('category')
    verified = request.GET.get('verified')
    search_q = request.GET.get('q', '').strip()

    places = Destination.objects.all().order_by('-created_at')

    if category:
        places = places.filter(category=category)
    if verified == 'true':
        places = places.filter(is_verified=True)
    elif verified == 'false':
        places = places.filter(is_verified=False)
    if search_q:
        places = places.filter(Q(title__icontains=search_q) | Q(location_name__icontains=search_q))

    context = {
        'page_title': 'Places & Destinations',
        'active_nav': 'places',
        'places': places,
        'category_choices': Destination.CATEGORY_CHOICES,
        'current_category': category,
        'current_verified': verified,
        'search_q': search_q,
    }
    return render(request, 'ops/places_list.html', context)


@staff_required
def place_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                place = form.save(commit=False)
                place.submitted_by = request.user
                place.save()

                # Handle multiple gallery moments upload
                gallery_files = request.FILES.getlist('gallery_images')
                gallery_errors = 0
                for f in gallery_files:
                    try:
                        Gallery.objects.create(destination=place, image=f)
                    except Exception as ge:
                        gallery_errors += 1

                log_audit_action(request.user, 'CREATE', 'Place', place.title, {'slug': place.slug, 'gallery_count': len(gallery_files)})
                if gallery_errors > 0:
                    messages.warning(request, f'Destination "{place.title}" created, but {gallery_errors} gallery photo(s) failed to save. Please check image format/storage.')
                else:
                    messages.success(request, f'Destination "{place.title}" successfully created with {len(gallery_files)} gallery photos!')
                return redirect('ops_places_list')
            except Exception as e:
                messages.error(request, f'Error saving destination: {str(e)}')
    else:
        form = DestinationForm()

    context = {
        'page_title': 'Add New Destination',
        'active_nav': 'places',
        'form': form,
        'is_edit': False,
    }
    return render(request, 'ops/place_form.html', context)


@staff_required
def place_edit(request, pk):
    place = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            try:
                form.save()

                # Handle multiple gallery moments upload
                gallery_files = request.FILES.getlist('gallery_images')
                gallery_errors = 0
                for f in gallery_files:
                    try:
                        Gallery.objects.create(destination=place, image=f)
                    except Exception as ge:
                        gallery_errors += 1

                log_audit_action(request.user, 'UPDATE', 'Place', place.title, {'id': place.pk, 'new_gallery_uploaded': len(gallery_files)})
                if gallery_errors > 0:
                    messages.warning(request, f'Destination "{place.title}" updated, but {gallery_errors} gallery photo(s) failed to save. Please check image format/storage.')
                else:
                    messages.success(request, f'Destination "{place.title}" updated successfully.')
                return redirect('ops_place_edit', pk=place.pk)
            except Exception as e:
                messages.error(request, f'Error saving destination: {str(e)}')
    else:
        form = DestinationForm(instance=place)

    context = {
        'page_title': f'Edit: {place.title}',
        'active_nav': 'places',
        'form': form,
        'place': place,
        'gallery_photos': place.gallery.all(),
        'is_edit': True,
    }
    return render(request, 'ops/place_form.html', context)


@staff_required
def place_gallery_delete(request, place_pk, gallery_pk):
    place = get_object_or_404(Destination, pk=place_pk)
    gallery_item = get_object_or_404(Gallery, pk=gallery_pk, destination=place)
    gallery_item.delete()
    messages.success(request, 'Gallery photo removed successfully.')
    return redirect('ops_place_edit', pk=place_pk)


@staff_required
def place_toggle_verify(request, pk):
    place = get_object_or_404(Destination, pk=pk)
    place.is_verified = not place.is_verified
    place.save()
    log_audit_action(
        request.user, 'VERIFY', 'Place', place.title,
        {'is_verified': place.is_verified}
    )
    status_str = "Verified" if place.is_verified else "Unverified"
    messages.success(request, f'"{place.title}" is now marked as {status_str}.')
    return redirect('ops_places_list')


@staff_required
def place_delete(request, pk):
    place = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        title = place.title
        place.delete()
        log_audit_action(request.user, 'DELETE', 'Place', title, {'id': pk})
        messages.success(request, f'Destination "{title}" deleted.')
        return redirect('ops_places_list')
    return render(request, 'ops/confirm_delete.html', {'object': place, 'type': 'Destination', 'cancel_url': reverse('ops_places_list')})


# ==============================================================================
# 3. ITINERARY BUILDER & JOURNEY STUDIO
# ==============================================================================

@staff_required
def itineraries_list(request):
    itineraries = Itinerary.objects.prefetch_related('days__stops').all().order_by('order', 'title')
    context = {
        'page_title': 'Itinerary Management',
        'active_nav': 'itineraries',
        'itineraries': itineraries,
    }
    return render(request, 'ops/itineraries_list.html', context)


@staff_required
def itinerary_create(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                itin = form.save()
                # Create default Day 1
                ItineraryDay.objects.create(
                    itinerary=itin,
                    day_number=1,
                    title=f"Day 1: Exploring {itin.title}"
                )
                log_audit_action(request.user, 'CREATE', 'Itinerary', itin.title, {'id': itin.pk})
                messages.success(request, f'Itinerary "{itin.title}" created. Now build your days and stops!')
                return redirect('ops_itinerary_builder', pk=itin.pk)
            except Exception as e:
                messages.error(request, f'Error creating itinerary: {str(e)}')
    else:
        form = ItineraryForm()

    return render(request, 'ops/itinerary_form.html', {
        'page_title': 'Create New Itinerary',
        'active_nav': 'itineraries',
        'form': form,
        'is_edit': False,
    })


@staff_required
def itinerary_edit(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    if request.method == 'POST':
        form = ItineraryForm(request.POST, request.FILES, instance=itinerary)
        if form.is_valid():
            try:
                itin = form.save()
                log_audit_action(request.user, 'UPDATE', 'Itinerary', itin.title, {'id': itin.pk})
                messages.success(request, f'Itinerary "{itin.title}" updated successfully.')
                return redirect('ops_itineraries_list')
            except Exception as e:
                messages.error(request, f'Error updating itinerary: {str(e)}')
    else:
        form = ItineraryForm(instance=itinerary)

    return render(request, 'ops/itinerary_form.html', {
        'page_title': f'Edit Itinerary: {itinerary.title}',
        'active_nav': 'itineraries',
        'form': form,
        'itinerary': itinerary,
        'is_edit': True,
    })


@staff_required
def itinerary_delete(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    if request.method == 'POST':
        title = itinerary.title
        itinerary.delete()
        log_audit_action(request.user, 'DELETE', 'Itinerary', title, {'id': pk})
        messages.success(request, f'Itinerary "{title}" deleted successfully.')
        return redirect('ops_itineraries_list')
    return render(request, 'ops/confirm_delete.html', {
        'object': itinerary.title,
        'type': 'Itinerary',
        'cancel_url': reverse('ops_itineraries_list')
    })


@staff_required
def itinerary_builder(request, pk):
    itinerary = get_object_or_404(
        Itinerary.objects.prefetch_related('days__stops__destination'),
        pk=pk
    )
    destinations = Destination.objects.all().order_by('title')
    days = itinerary.days.all().order_by('day_number')

    stop_form = ItineraryStopForm()
    day_form = ItineraryDayForm()

    context = {
        'page_title': f'Builder: {itinerary.title}',
        'active_nav': 'itineraries',
        'itinerary': itinerary,
        'days': days,
        'destinations': destinations,
        'stop_form': stop_form,
        'day_form': day_form,
    }
    return render(request, 'ops/itinerary_builder.html', context)


@staff_required
def itinerary_add_day(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    if request.method == 'POST':
        next_day_num = itinerary.days.count() + 1
        day = ItineraryDay.objects.create(
            itinerary=itinerary,
            day_number=next_day_num,
            title=request.POST.get('title', f"Day {next_day_num} Discoveries")
        )
        itinerary.duration_days = max(itinerary.duration_days, next_day_num)
        itinerary.save()
        log_audit_action(request.user, 'UPDATE', 'Itinerary', itinerary.title, {'action': 'added_day', 'day': next_day_num})
        messages.success(request, f'Added Day {day.day_number} to {itinerary.title}!')
    return redirect('ops_itinerary_builder', pk=pk)


@staff_required
def itinerary_delete_day(request, pk, day_id):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    day = get_object_or_404(ItineraryDay, pk=day_id, itinerary=itinerary)
    day.delete()
    # Reindex remaining days
    for idx, d in enumerate(itinerary.days.all().order_by('day_number'), start=1):
        d.day_number = idx
        d.save()
    itinerary.duration_days = max(1, itinerary.days.count())
    itinerary.save()
    messages.success(request, 'Day removed.')
    return redirect('ops_itinerary_builder', pk=pk)


@staff_required
def itinerary_add_stop(request, pk, day_id):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    day = get_object_or_404(ItineraryDay, pk=day_id, itinerary=itinerary)

    if request.method == 'POST':
        form = ItineraryStopForm(request.POST)
        if form.is_valid():
            stop = form.save(commit=False)
            stop.day = day
            stop.order_index = day.stops.count() + 1
            stop.save()
            log_audit_action(request.user, 'UPDATE', 'Itinerary', itinerary.title, {'action': 'added_stop', 'stop': stop.title})
            messages.success(request, f'Stop "{stop.title}" added to Day {day.day_number}!')
    return redirect('ops_itinerary_builder', pk=pk)


@staff_required
def itinerary_delete_stop(request, pk, stop_id):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    stop = get_object_or_404(ItineraryStop, pk=stop_id, day__itinerary=itinerary)
    day = stop.day
    stop.delete()
    # Reindex remaining stops
    for idx, s in enumerate(day.stops.all().order_by('order_index'), start=1):
        s.order_index = idx
        s.save()
    messages.success(request, 'Stop removed.')
    return redirect('ops_itinerary_builder', pk=pk)


@staff_required
def itinerary_reorder_stop(request, pk, stop_id, direction):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    stop = get_object_or_404(ItineraryStop, pk=stop_id, day__itinerary=itinerary)
    day = stop.day
    stops = list(day.stops.all().order_by('order_index'))

    idx = stops.index(stop)
    if direction == 'up' and idx > 0:
        stops[idx], stops[idx - 1] = stops[idx - 1], stops[idx]
    elif direction == 'down' and idx < len(stops) - 1:
        stops[idx], stops[idx + 1] = stops[idx + 1], stops[idx]

    for i, s in enumerate(stops, start=1):
        s.order_index = i
        s.save()

    messages.success(request, 'Stop order updated.')
    return redirect('ops_itinerary_builder', pk=pk)


# ==============================================================================
# 4. NFC OPERATIONS & BULK GENERATOR
# ==============================================================================

@staff_required
def nfc_list(request):
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    search_q = request.GET.get('q', '').strip()

    tags = NFCTag.objects.select_related('assigned_partner', 'assigned_itinerary', 'assigned_destination').all()

    if status_filter == 'active':
        tags = tags.filter(is_active=True)
    elif status_filter == 'inactive':
        tags = tags.filter(is_active=False)

    if type_filter:
        tags = tags.filter(tag_type=type_filter)

    if search_q:
        tags = tags.filter(Q(tag_uid__icontains=search_q) | Q(title__icontains=search_q))

    context = {
        'page_title': 'NFC Tag Operations',
        'active_nav': 'nfc',
        'tags': tags,
        'tag_types': NFCTag.TAG_TYPE_CHOICES,
        'current_status': status_filter,
        'current_type': type_filter,
        'search_q': search_q,
    }
    return render(request, 'ops/nfc_list.html', context)


@staff_required
def nfc_create(request):
    if request.method == 'POST':
        form = NFCTagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            log_audit_action(request.user, 'CREATE', 'NFC Tag', tag.tag_uid, {'title': tag.title})
            messages.success(request, f'NFC Tag [{tag.tag_uid}] created successfully!')
            return redirect('ops_nfc_detail', pk=tag.pk)
    else:
        form = NFCTagForm()

    return render(request, 'ops/nfc_form.html', {
        'page_title': 'Create NFC Tag',
        'active_nav': 'nfc',
        'form': form,
    })


@staff_required
def nfc_detail(request, pk):
    tag = get_object_or_404(
        NFCTag.objects.select_related('assigned_partner', 'assigned_itinerary', 'assigned_destination'),
        pk=pk
    )
    if request.method == 'POST':
        form = NFCTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            log_audit_action(request.user, 'UPDATE', 'NFC Tag', tag.tag_uid)
            messages.success(request, f'Tag [{tag.tag_uid}] updated.')
            return redirect('ops_nfc_detail', pk=tag.pk)
    else:
        form = NFCTagForm(instance=tag)

    recent_events = tag.tap_events.all()[:15]

    context = {
        'page_title': f'NFC Tag: {tag.tag_uid}',
        'active_nav': 'nfc',
        'tag': tag,
        'form': form,
        'recent_events': recent_events,
    }
    return render(request, 'ops/nfc_detail.html', context)


@staff_required
def nfc_delete(request, pk):
    tag = get_object_or_404(NFCTag, pk=pk)
    if request.method == 'POST':
        uid = tag.tag_uid
        tag.delete()
        log_audit_action(request.user, 'DELETE', 'NFC Tag', uid, {'id': pk})
        messages.success(request, f'NFC Tag [{uid}] deleted successfully.')
        return redirect('ops_nfc_list')
    return render(request, 'ops/confirm_delete.html', {
        'object': f'[{tag.tag_uid}] {tag.title}',
        'type': 'NFC Tag',
        'cancel_url': reverse('ops_nfc_list')
    })


@staff_required
def nfc_toggle_status(request, pk):
    tag = get_object_or_404(NFCTag, pk=pk)
    tag.is_active = not tag.is_active
    tag.save()
    log_audit_action(request.user, 'STATUS_CHANGE', 'NFC Tag', tag.tag_uid, {'is_active': tag.is_active})
    status_str = "Active" if tag.is_active else "Paused"
    messages.success(request, f'Tag [{tag.tag_uid}] status changed to {status_str}.')
    return redirect('ops_nfc_list')


@staff_required
def nfc_bulk_generate(request):
    if request.method == 'POST':
        form = BulkNFCTagForm(request.POST)
        if form.is_valid():
            created_tags = generate_bulk_tags(form.cleaned_data, user=request.user)
            messages.success(request, f'Successfully generated batch of {len(created_tags)} physical NFC tags!')
            return redirect(f'/ops/nfc/print/?prefix={form.cleaned_data["prefix"]}')
    else:
        form = BulkNFCTagForm()

    return render(request, 'ops/nfc_bulk.html', {
        'page_title': 'Bulk NFC Generator',
        'active_nav': 'nfc',
        'form': form,
    })


@staff_required
def nfc_print_sheet(request):
    prefix = request.GET.get('prefix')
    tags = NFCTag.objects.filter(is_active=True)
    if prefix:
        tags = tags.filter(tag_uid__startswith=prefix)

    tags = tags[:48]  # Grid for print sheets

    context = {
        'page_title': 'Printable NFC & QR Sticker Sheets',
        'tags': tags,
    }
    return render(request, 'ops/nfc_print_sheet.html', context)


@staff_required
def nfc_export_csv(request):
    csv_data = export_nfc_csv()
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ratnagiri_nfc_tags.csv"'
    return response


# ==============================================================================
# 5. PARTNER DIRECTORY & CONCIERGE
# ==============================================================================

def _create_or_ensure_partner_nfc(partner, user=None):
    """Ensure partner has an active NFC Tag & QR gateway configured."""
    tag = partner.nfc_tags.filter(is_active=True).first()
    if tag:
        return tag, False

    # Generate clean token UID
    base_slug = slugify(partner.business_name)[:14].upper() if partner.business_name else "PARTNER"
    base_token = f"PARTNER-{base_slug}"
    token = base_token
    counter = 1
    while NFCTag.objects.filter(tag_uid__iexact=token).exists():
        token = f"{base_token}-{counter:02d}"
        counter += 1

    tag_type = 'HOTEL' if partner.partner_type in ('HOTEL', 'HOMESTAY') else (
        'RESTAURANT' if partner.partner_type == 'RESTAURANT' else 'GENERAL'
    )

    tag = NFCTag.objects.create(
        tag_uid=token,
        title=f"{partner.business_name} Guest Welcome NFC",
        tag_type=tag_type,
        target_experience='PARTNER_PAGE',
        assigned_partner=partner,
        custom_welcome_title=f"Welcome to {partner.business_name}!",
        custom_welcome_message=f"We're glad to host you. Explore our local concierge, nearby attractions, and recommendations.",
        is_active=True
    )
    if user:
        log_audit_action(user, 'CREATE', 'NFC Tag', tag.tag_uid, {'partner': partner.business_name})
    return tag, True


@staff_required
def partners_list(request):
    partners = Partner.objects.prefetch_related('nfc_tags').all().order_by('-is_featured', 'business_name')
    return render(request, 'ops/partners_list.html', {
        'page_title': 'Partner Directory',
        'active_nav': 'partners',
        'partners': partners,
    })


@staff_required
def partner_create(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                partner = form.save()
                log_audit_action(request.user, 'CREATE', 'Partner', partner.business_name)

                # Auto-generate NFC tag if requested
                if form.cleaned_data.get('generate_nfc', True):
                    tag, created = _create_or_ensure_partner_nfc(partner, request.user)
                    if created:
                        messages.success(request, f'Partner "{partner.business_name}" created & Smart NFC Tag [{tag.tag_uid}] generated!')
                    else:
                        messages.success(request, f'Partner "{partner.business_name}" added successfully.')
                else:
                    messages.success(request, f'Partner "{partner.business_name}" added.')
                return redirect('ops_partner_edit', pk=partner.pk)
            except Exception as e:
                messages.error(request, f'Error adding partner: {str(e)}')
    else:
        form = PartnerForm(initial={'generate_nfc': True})

    return render(request, 'ops/partner_form.html', {
        'page_title': 'Add New Partner Business',
        'active_nav': 'partners',
        'form': form,
        'is_edit': False,
    })


@staff_required
def partner_edit(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    nfc_tags = partner.nfc_tags.all()
    primary_tag = partner.primary_nfc_tag()

    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            try:
                form.save()
                log_audit_action(request.user, 'UPDATE', 'Partner', partner.business_name)

                if form.cleaned_data.get('generate_nfc') and not primary_tag:
                    tag, created = _create_or_ensure_partner_nfc(partner, request.user)
                    if created:
                        messages.success(request, f'Partner updated & Smart NFC Tag [{tag.tag_uid}] generated!')
                else:
                    messages.success(request, f'Partner "{partner.business_name}" updated successfully.')
                return redirect('ops_partner_edit', pk=partner.pk)
            except Exception as e:
                messages.error(request, f'Error updating partner: {str(e)}')
    else:
        form = PartnerForm(instance=partner, initial={'generate_nfc': bool(primary_tag)})

    return render(request, 'ops/partner_form.html', {
        'page_title': f'Edit: {partner.business_name}',
        'active_nav': 'partners',
        'form': form,
        'partner': partner,
        'nfc_tags': nfc_tags,
        'primary_tag': primary_tag,
        'is_edit': True,
    })


@staff_required
def partner_generate_nfc(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    tag, created = _create_or_ensure_partner_nfc(partner, request.user)
    if created:
        messages.success(request, f'Generated new NFC Tag [{tag.tag_uid}] and QR Code for {partner.business_name}!')
    else:
        messages.info(request, f'Partner already has active NFC Tag [{tag.tag_uid}].')
    
    next_url = request.POST.get('next') or request.GET.get('next') or reverse('ops_partner_edit', kwargs={'pk': partner.pk})
    return redirect(next_url)


@staff_required
def partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    if request.method == 'POST':
        name = partner.business_name
        partner.delete()
        log_audit_action(request.user, 'DELETE', 'Partner', name)
        messages.success(request, f'Partner "{name}" deleted.')
        return redirect('ops_partners_list')
    return render(request, 'ops/confirm_delete.html', {'object': partner, 'type': 'Partner', 'cancel_url': reverse('ops_partners_list')})


# ==============================================================================
# 6. CONTENT & SAFETY CMS (FAQs, TIPS, ANNOUNCEMENTS, SOS)
# ==============================================================================

@staff_required
def content_hub(request):
    faqs = FAQ.objects.all()
    tips = TravelTip.objects.all()
    announcements = Announcement.objects.all()
    emergency_contacts = EmergencyContact.objects.all()

    context = {
        'page_title': 'Content & Safety CMS',
        'active_nav': 'content',
        'faqs': faqs,
        'tips': tips,
        'announcements': announcements,
        'emergency_contacts': emergency_contacts,
    }
    return render(request, 'ops/content_hub.html', context)


@staff_required
def faq_create(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save()
            log_audit_action(request.user, 'CREATE', 'FAQ', faq.question[:40])
            messages.success(request, 'FAQ saved.')
            return redirect('ops_content_hub')
    else:
        form = FAQForm()
    return render(request, 'ops/generic_form.html', {'page_title': 'Create FAQ', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def faq_edit(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            log_audit_action(request.user, 'UPDATE', 'FAQ', faq.question[:40])
            messages.success(request, 'FAQ updated.')
            return redirect('ops_content_hub')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'ops/generic_form.html', {'page_title': 'Edit FAQ', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, 'FAQ deleted.')
    return redirect('ops_content_hub')


@staff_required
def tip_create(request):
    if request.method == 'POST':
        form = TravelTipForm(request.POST)
        if form.is_valid():
            tip = form.save()
            log_audit_action(request.user, 'CREATE', 'Travel Tip', tip.title)
            messages.success(request, 'Travel Tip saved.')
            return redirect('ops_content_hub')
    else:
        form = TravelTipForm()
    return render(request, 'ops/generic_form.html', {'page_title': 'Create Travel Tip', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def tip_edit(request, pk):
    tip = get_object_or_404(TravelTip, pk=pk)
    if request.method == 'POST':
        form = TravelTipForm(request.POST, instance=tip)
        if form.is_valid():
            form.save()
            log_audit_action(request.user, 'UPDATE', 'Travel Tip', tip.title)
            messages.success(request, 'Travel Tip updated.')
            return redirect('ops_content_hub')
    else:
        form = TravelTipForm(instance=tip)
    return render(request, 'ops/generic_form.html', {'page_title': f'Edit Tip: {tip.title}', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def tip_delete(request, pk):
    tip = get_object_or_404(TravelTip, pk=pk)
    if request.method == 'POST':
        title = tip.title
        tip.delete()
        log_audit_action(request.user, 'DELETE', 'Travel Tip', title)
        messages.success(request, f'Travel Tip "{title}" deleted.')
        return redirect('ops_content_hub')
    return render(request, 'ops/confirm_delete.html', {'object': tip.title, 'type': 'Travel Tip', 'cancel_url': reverse('ops_content_hub')})


@staff_required
def emergency_create(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            log_audit_action(request.user, 'CREATE', 'Emergency Contact', contact.name)
            messages.success(request, f'Emergency contact "{contact.name}" added.')
            return redirect('ops_content_hub')
    else:
        form = EmergencyContactForm()
    return render(request, 'ops/generic_form.html', {'page_title': 'Add Emergency Contact', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def emergency_edit(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            log_audit_action(request.user, 'UPDATE', 'Emergency Contact', contact.name)
            messages.success(request, f'Emergency contact "{contact.name}" updated.')
            return redirect('ops_content_hub')
    else:
        form = EmergencyContactForm(instance=contact)
    return render(request, 'ops/generic_form.html', {'page_title': f'Edit Contact: {contact.name}', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def emergency_delete(request, pk):
    contact = get_object_or_404(EmergencyContact, pk=pk)
    if request.method == 'POST':
        name = contact.name
        contact.delete()
        log_audit_action(request.user, 'DELETE', 'Emergency Contact', name)
        messages.success(request, f'Emergency contact "{name}" deleted.')
        return redirect('ops_content_hub')
    return render(request, 'ops/confirm_delete.html', {'object': f'{contact.name} ({contact.phone_number})', 'type': 'Emergency Contact', 'cancel_url': reverse('ops_content_hub')})


@staff_required
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save()
            log_audit_action(request.user, 'CREATE', 'Announcement', ann.title)
            messages.success(request, 'Announcement broadcast live.')
            return redirect('ops_content_hub')
    else:
        form = AnnouncementForm()
    return render(request, 'ops/generic_form.html', {'page_title': 'Create Alert / Announcement', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def announcement_edit(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=ann)
        if form.is_valid():
            form.save()
            log_audit_action(request.user, 'UPDATE', 'Announcement', ann.title)
            messages.success(request, 'Announcement updated.')
            return redirect('ops_content_hub')
    else:
        form = AnnouncementForm(instance=ann)
    return render(request, 'ops/generic_form.html', {'page_title': f'Edit Announcement: {ann.title}', 'active_nav': 'content', 'form': form, 'back_url': reverse('ops_content_hub')})


@staff_required
def announcement_delete(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        title = ann.title
        ann.delete()
        log_audit_action(request.user, 'DELETE', 'Announcement', title)
        messages.success(request, f'Announcement "{title}" deleted.')
        return redirect('ops_content_hub')
    return render(request, 'ops/confirm_delete.html', {'object': ann.title, 'type': 'Announcement', 'cancel_url': reverse('ops_content_hub')})


# ==============================================================================
# 7. MEDIA & ASSET HUB
# ==============================================================================

@staff_required
def media_hub(request):
    destinations = Destination.objects.exclude(main_image='').order_by('-created_at')[:24]
    itineraries = Itinerary.objects.exclude(cover_image='').order_by('-created_at')[:12]
    partners = Partner.objects.exclude(logo='').order_by('-created_at')[:12]

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        try:
            file_path = default_storage.save(f'uploads/{uploaded_file.name}', uploaded_file)
            file_url = default_storage.url(file_path)
            log_audit_action(request.user, 'CREATE', 'Media Asset', uploaded_file.name, {'url': file_url})
            messages.success(request, f'Image uploaded successfully to Cloud CDN: {file_url}')
        except Exception as e:
            messages.error(request, f'Image upload failed: {str(e)}')
        return redirect('ops_media_hub')

    context = {
        'page_title': 'Media & Asset Hub',
        'active_nav': 'media',
        'destinations': destinations,
        'itineraries': itineraries,
        'partners': partners,
    }
    return render(request, 'ops/media_hub.html', context)


# ==============================================================================
# 8. ANALYTICS INTELLIGENCE CENTER
# ==============================================================================

@staff_required
def analytics_center(request):
    days = int(request.GET.get('days', 30))
    charts = get_chart_analytics(days=days)
    stats = get_operations_stats()
    top_tags = NFCTag.objects.order_by('-tap_count')[:15]
    top_partners = Partner.objects.filter(is_active=True)[:10]

    context = {
        'page_title': 'Analytics Intelligence',
        'active_nav': 'analytics',
        'charts': charts,
        'stats': stats,
        'top_tags': top_tags,
        'top_partners': top_partners,
        'selected_days': days,
    }
    return render(request, 'ops/analytics_center.html', context)


# ==============================================================================
# 9. SYSTEM, AUDIT LOG & ROLES
# ==============================================================================

@staff_required
def system_hub(request):
    users = User.objects.all().order_by('-date_joined')
    audit_logs = AdminAuditLog.objects.select_related('user').all()[:50]

    context = {
        'page_title': 'System & Audit Trail',
        'active_nav': 'system',
        'users': users,
        'audit_logs': audit_logs,
    }
    return render(request, 'ops/system_audit.html', context)


# ==============================================================================
# 10. GLOBAL SEARCH
# ==============================================================================

@staff_required
def global_search(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return redirect('ops_dashboard')

    places = Destination.objects.filter(Q(title__icontains=q) | Q(location_name__icontains=q))[:10]
    itineraries = Itinerary.objects.filter(Q(title__icontains=q) | Q(tagline__icontains=q))[:10]
    tags = NFCTag.objects.filter(Q(tag_uid__icontains=q) | Q(title__icontains=q))[:15]
    partners = Partner.objects.filter(Q(business_name__icontains=q) | Q(short_tagline__icontains=q))[:10]

    context = {
        'page_title': f'Search: "{q}"',
        'active_nav': 'dashboard',
        'query': q,
        'places': places,
        'itineraries': itineraries,
        'tags': tags,
        'partners': partners,
    }
    return render(request, 'ops/search_results.html', context)
