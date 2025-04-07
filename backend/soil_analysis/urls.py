"""
URL configuration for soil_analysis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Simple view to handle the root URL
def home_view(request):
    return JsonResponse({
        "status": "success",
        "message": "Soil Analysis API is running",
        "endpoints": {
            "predict": "/api/predict/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
