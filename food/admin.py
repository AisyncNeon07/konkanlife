from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import FoodItem, Tag, Category


# ─────────────────────────────────────────────────────────────────────────────
# Reusable button helper (same pattern as spots/admin.py)
# ─────────────────────────────────────────────────────────────────────────────

def _api_button(url: str, label: str, color: str = "#10b981") -> str:
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
# Food Admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):

    # ── List view columns ──────────────────────────────────────────────────
    list_display = (
        'name',
        'price',
        'rating',
        'best_time_to_eat',
        'uploaded_by',
        'created_at',
        'api_list_link',
        'api_detail_link',
    )

    list_filter   = ('created_at',)
    search_fields = ('name', 'description')
    ordering      = ('-created_at',)
    list_per_page = 20

    # ── Detail (change) view ───────────────────────────────────────────────
    readonly_fields = ('api_detail_link_full', 'created_at', 'updated_at')

    fieldsets = (
        ('🍽️  Dish Details', {
            'fields': ('name', 'price', 'rating', 'photo')
        }),
        ('📝  Description', {
            'fields': ('description', 'best_time_to_eat')
        }),
        ('🔗  API Access', {
            'fields': ('api_detail_link_full',),
            'description': 'Use these links to view this record via the REST API.',
        }),
        ('👤  Ownership', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # ── Column: API list button (same on every row) ────────────────────────

    @admin.display(description='Food API')
    def api_list_link(self, obj):
        url = '/api/v1/food/'
        return mark_safe(_api_button(url, 'View API List', color='#0077b6'))

    # ── Column: API detail button (unique per food item) ──────────────────

    @admin.display(description='Detail API')
    def api_detail_link(self, obj):
        url = f'/api/v1/food/{obj.pk}/'
        return mark_safe(_api_button(url, 'View in API', color='#10b981'))

    # ── Readonly field inside the change form ──────────────────────────────

    @admin.display(description='API Endpoints')
    def api_detail_link_full(self, obj):
        if not obj.pk:
            return '—  Save first to generate the API link.'

        list_url   = '/api/v1/food/'
        detail_url = f'/api/v1/food/{obj.pk}/'

        return format_html(
            '<div style="display:flex;gap:10px;flex-wrap:wrap;">'
            '{}'
            '{}'
            '</div>',
            mark_safe(_api_button(list_url,   '⚡ All Food API',      '#0077b6')),
            mark_safe(_api_button(detail_url, '⚡ This Item in API',  '#10b981')),
        )


# ─────────────────────────────────────────────────────────────────────────────
# Tag & Category Admin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)