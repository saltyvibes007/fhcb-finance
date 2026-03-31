from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection
from django.conf import settings
from django.conf.urls.static import static


def health(request):
    db_ok = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = cursor.fetchone()[0] == 1
    except Exception:
        db_ok = False
    return JsonResponse(
        {
            "status": "ok" if db_ok else "degraded",
            "timestamp": timezone.now().isoformat(),
            "database": "connected" if db_ok else "unavailable",
            "branch": settings.GIT_BRANCH,
            "commit": settings.GIT_COMMIT[:8],
            "env": "production" if settings.IS_PRODUCTION else settings.GIT_BRANCH,
        },
        status=200 if db_ok else 503,
    )


def api_root(request):
    return JsonResponse({
        "name": "BloomFi Corp API",
        "version": "1.0",
        "branch": settings.GIT_BRANCH,
        "commit": settings.GIT_COMMIT[:8],
    })


v1 = [
    path('auth/', include('accounts.urls')),
    path('orgs/', include('accounts.org_urls')),
    path('', include('transactions.urls')),
    path('', include('reports.urls')),
    path('', include('chat.urls')),
]

urlpatterns = [
    path('', api_root),
    path('health/', health),
    path('api/health/', health),
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
