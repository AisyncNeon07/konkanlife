import csv
import io
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum
from companion.models import (
    NFCTag, NFCTapEvent, Partner, Itinerary,
    EmergencyContact, FAQ, TravelTip, Announcement, AdminAuditLog
)
from destinations.models import Destination


from django.core.cache import cache
from django.db.models.functions import TruncDate


def log_audit_action(user, action, resource_type, resource_name, details=None):
    try:
        if details is None:
            details = {}
        elif not isinstance(details, dict):
            details = {'info': str(details)}

        AdminAuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            resource_type=str(resource_type),
            resource_name=str(resource_name)[:250],
            details_json=details
        )
    except Exception as e:
        print(f"[AUDIT LOG ERROR] {e}")


def get_operations_stats():
    cache_key = 'ops_dashboard_stats'
    cached = cache.get(cache_key)
    if cached:
        return cached

    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)

    total_destinations = Destination.objects.count()
    verified_destinations = Destination.objects.filter(is_verified=True).count()
    total_itineraries = Itinerary.objects.count()
    featured_itineraries = Itinerary.objects.filter(is_featured=True).count()
    total_nfc_tags = NFCTag.objects.count()
    active_nfc_tags = NFCTag.objects.filter(is_active=True).count()
    total_partners = Partner.objects.count()
    active_partners = Partner.objects.filter(is_active=True).count()

    total_taps = NFCTapEvent.objects.count()
    taps_last_7d = NFCTapEvent.objects.filter(tapped_at__gte=seven_days_ago).count()
    taps_last_30d = NFCTapEvent.objects.filter(tapped_at__gte=thirty_days_ago).count()
    
    unique_devices_count = NFCTapEvent.objects.values('session_hash').distinct().count()

    emergency_contacts_count = EmergencyContact.objects.filter(is_active=True).count()
    faqs_count = FAQ.objects.filter(is_published=True).count()
    tips_count = TravelTip.objects.filter(is_active=True).count()
    active_announcements_count = Announcement.objects.filter(is_active=True).count()

    unverified_places = Destination.objects.filter(is_verified=False).count()
    unassigned_tags = NFCTag.objects.filter(assigned_partner__isnull=True).count()
    unassigned_destinations = Destination.objects.filter(category='').count()

    stats = {
        'total_destinations': total_destinations,
        'verified_destinations': verified_destinations,
        'total_itineraries': total_itineraries,
        'featured_itineraries': featured_itineraries,
        'total_nfc_tags': total_nfc_tags,
        'active_nfc_tags': active_nfc_tags,
        'total_partners': total_partners,
        'active_partners': active_partners,
        'total_taps': total_taps,
        'taps_last_7d': taps_last_7d,
        'taps_last_30d': taps_last_30d,
        'unique_devices_count': unique_devices_count,
        'emergency_contacts_count': emergency_contacts_count,
        'faqs_count': faqs_count,
        'tips_count': tips_count,
        'active_announcements_count': active_announcements_count,
        'unverified_places': unverified_places,
        'unassigned_tags': unassigned_tags,
        'unassigned_destinations': unassigned_destinations,
    }
    cache.set(cache_key, stats, 45)
    return stats


def get_chart_analytics(days=14):
    cache_key = f'ops_chart_analytics_{days}'
    cached = cache.get(cache_key)
    if cached:
        return cached

    now = timezone.now()
    dates = [(now - timedelta(days=i)).date() for i in range(days - 1, -1, -1)]
    start_date = dates[0]
    
    # Single SQL aggregation grouped by TruncDate instead of loop queries
    events = (
        NFCTapEvent.objects.filter(
            tapped_at__date__gte=start_date,
            tapped_at__date__lte=dates[-1]
        )
        .annotate(tap_day=TruncDate('tapped_at'))
        .values('tap_day')
        .annotate(total=Count('id'))
    )
    taps_by_day = {e['tap_day']: e['total'] for e in events}
    daily_taps = [taps_by_day.get(d, 0) for d in dates]
    daily_labels = [d.strftime('%b %d') for d in dates]

    top_tags = list(NFCTag.objects.filter(tap_count__gt=0).order_by('-tap_count')[:5])
    top_tags_labels = [t.tag_uid for t in top_tags]
    top_tags_data = [t.tap_count for t in top_tags]

    category_counts = list(Destination.objects.values('category').annotate(total=Count('id')).order_by('-total')[:6])
    category_labels = [c['category'] or 'Uncategorized' for c in category_counts]
    category_data = [c['total'] for c in category_counts]

    partner_tags = list(NFCTag.objects.values('assigned_partner__business_name').annotate(total=Count('id')).order_by('-total')[:5])
    partner_labels = [item['assigned_partner__business_name'] or 'Unassigned' for item in partner_tags]
    partner_data = [item['total'] for item in partner_tags]

    device_qs = list(NFCTapEvent.objects.values('device_type').annotate(total=Count('id')).order_by())
    device_map = {item['device_type'].capitalize(): item['total'] for item in device_qs}
    mobile_count = device_map.get('Mobile', 0)
    desktop_count = device_map.get('Desktop', 0)
    tablet_count = device_map.get('Tablet', 0)
    if mobile_count == 0 and desktop_count == 0 and tablet_count == 0:
        mobile_count = 1

    chart_data = {
        'daily_labels': daily_labels,
        'daily_taps': daily_taps,
        'top_tags_labels': top_tags_labels,
        'top_tags_data': top_tags_data,
        'category_labels': category_labels,
        'category_data': category_data,
        'partner_labels': partner_labels,
        'partner_data': partner_data,
        'device_labels': ['Mobile', 'Desktop', 'Tablet'],
        'device_data': [mobile_count, desktop_count, tablet_count],
    }
    cache.set(cache_key, chart_data, 45)
    return chart_data


def generate_bulk_tags(data_or_prefix, count=None, batch_id=None, default_landing_view="HOME", partner=None, user=None):
    if isinstance(data_or_prefix, dict):
        data = data_or_prefix
        prefix = data.get('prefix', 'HOTEL-ROOM-').upper().strip()
        start_number = data.get('start_number', 1)
        count = data.get('count', 10)
        tag_type = data.get('tag_type', 'HOTEL')
        target_experience = data.get('target_experience', 'HOME')
        partner = data.get('assigned_partner')
        welcome_title = data.get('custom_welcome_title', '')
        welcome_msg = data.get('custom_welcome_message', '')
    else:
        prefix = (data_or_prefix or "RATNAGIRI-NFC").upper().strip()
        start_number = 1
        count = count or 10
        tag_type = "HOTEL"
        target_experience = default_landing_view or "HOME"
        welcome_title = ""
        welcome_msg = ""

    created_tags = []
    for i in range(count):
        num = start_number + i
        uid = f"{prefix}{num:02d}"
        tag, created = NFCTag.objects.get_or_create(
            tag_uid=uid,
            defaults={
                'title': f"{welcome_title or prefix} #{num:02d}",
                'tag_type': tag_type,
                'target_experience': target_experience,
                'assigned_partner': partner,
                'custom_welcome_title': welcome_title,
                'custom_welcome_message': welcome_msg,
                'is_active': True,
            }
        )
        created_tags.append(tag)

    if user:
        log_audit_action(
            user=user,
            action="BULK_ACTION",
            resource_type="NFC Tag",
            resource_name=f"Batch {prefix} ({count} tags)",
            details={'prefix': prefix, 'count': count, 'start_number': start_number}
        )

    return created_tags


def export_nfc_csv(tags=None):
    if tags is None:
        tags = NFCTag.objects.select_related('assigned_partner').all().order_by('tag_uid')

    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'Tag UID',
        'Title',
        'Tag Type',
        'Target Experience',
        'Partner Name',
        'Status',
        'Tap Count',
        'NFC Tap URL',
        'Created Date'
    ])

    for tag in tags:
        writer.writerow([
            tag.tag_uid,
            tag.title,
            tag.get_tag_type_display() if hasattr(tag, 'get_tag_type_display') else tag.tag_type,
            tag.get_target_experience_display() if hasattr(tag, 'get_target_experience_display') else tag.target_experience,
            tag.assigned_partner.business_name if tag.assigned_partner else "-",
            "Active" if tag.is_active else "Inactive",
            tag.tap_count,
            f"https://konkantravel.in/t/{tag.tag_uid}/",
            tag.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(tag, 'created_at') and tag.created_at else "-"
        ])

    return output.getvalue()
