from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connection


def healthcheck(request):
    """Lightweight Docker / Load Balancer probe with DB connectivity check."""
    status = {"status": "ok", "app": "konkan_guide"}
    try:
        connection.ensure_connection()
        status["database"] = "connected"
        return JsonResponse(status, status=200)
    except Exception as e:
        status["status"] = "degraded"
        status["database"] = str(e)
        return JsonResponse(status, status=503)


urlpatterns = [
    # Health Probe
    path('healthz/', healthcheck, name='healthcheck'),

    # Operations Control Center & Tourism CMS
    path('ops/', include('ops.urls')),

    # Standard Django Admin
    path('admin/', admin.site.urls),

    # HTML views
    path('', include('core.urls')),
    path('', include('companion.urls')),
    path('spots/', include('spots.urls')),
    path('destinations/', include('destinations.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('food/', include('food.urls')),
    path('users/', include('users.urls')),

    # REST API
    path('api/v1/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
