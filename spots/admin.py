from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Spots, Category, Tag


# ─────────────────────────────────────────────────────────────────────────────
# Reusable helper to produce a clean API link button
# ─────────────────────────────────────────────────────────────────────────────

def _api_button(url: str, label: str, color: str = "#10b981") -> str:
    """
    Returns safe HTML for a styled button that opens `url` in a new tab.
    Uses format_html internally via the caller — call this only inside
    format_html() or mark_safe()-wrapped contexts.
    """
    return (
        f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
        f'style="display:inline-flex;align-items:center;gap:6px;'
        f'background:{color};color:#fff;padding:5px 14px;border-radius:6px;'
        f'font-size:12px;font-weight:600;text-decoration:none;'
        f'border:none;cursor:pointer;letter-spacing:0.3px;'
        f'transition:opacity .2s;" '
        f'onmouseover="this.style.opacity=\'0.85\'" '
        f'onmouseout="this.style.opacity=\'1\'">'
        f'<span style="font-size:14px;">⚡</span> {label}'
        f'</a>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Spots Admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Spots)
class SpotsAdmin(admin.ModelAdmin):

    # ── List view columns ──────────────────────────────────────────────────
    list_display = (
        'name',
        'category',
        'uploaded_by',
        'distance',
        'rating',
        'created_at',
        'api_list_link',    # ← "View Spots API" button on every row
        'api_detail_link',  # ← "View in API" link for this specific spot
    )

    list_filter  = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering     = ('-created_at',)
    list_per_page = 20

    # ── Detail (change) view ───────────────────────────────────────────────
    readonly_fields = ('api_detail_link_full', 'created_at', 'updated_at')

    fieldsets = (
        ('🗺️  Spot Details', {
            'fields': ('name', 'category', 'tags', 'rating', 'description')
        }),
        ('📍  Location & Media', {
            'fields': ('distance', 'map_link', 'photo',
                       'opening_hours', 'closing_hours')
        }),
        ('🔗  API Access', {
            # Shows the full, styled button inside the edit form
            'fields': ('api_detail_link_full',),
            'description': 'Use these links to view this record via the REST API.',
        }),
        ('👤  Attribution', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # ── Column: "View Spots API" — same URL on every row (list endpoint) ───

    @admin.display(description='Spots API')
    def api_list_link(self, obj):
        """
        Shown in the list view table.
        Opens /api/v1/spots/ — the full list endpoint.
        """
        url = '/api/v1/spots/'
        return format_html(_api_button(url, 'View API List', color='#0077b6'))

    # ── Column: "This Spot in API" — unique UUID per row ──────────────────

    @admin.display(description='Detail API')
    def api_detail_link(self, obj):
        """
        Shown in the list view table.
        Opens /api/v1/spots/<uuid>/ for this specific spot.
        """
        url = f'/api/v1/spots/{obj.pk}/'
        return format_html(_api_button(url, 'View in API', color='#10b981'))

    # ── Readonly field: big button shown inside the change form ───────────

    @admin.display(description='API Endpoints')
    def api_detail_link_full(self, obj):
        """
        Shown in the change/detail view as a readonly field.
        Renders two buttons: one for the list, one for this specific object.
        """
        if not obj.pk:
            return '—  Save first to generate the API link.'

        list_url   = '/api/v1/spots/'
        detail_url = f'/api/v1/spots/{obj.pk}/'

        return format_html(
            '<div style="display:flex;gap:10px;flex-wrap:wrap;">'
            '{}'   # list button
            '{}'   # detail button
            '</div>',
            format_html(_api_button(list_url,   '⚡ All Spots API',    '#0077b6')),
            format_html(_api_button(detail_url, '⚡ This Spot in API', '#10b981')),
        )


# ─────────────────────────────────────────────────────────────────────────────
# Category & Tag Admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)