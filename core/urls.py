"""
URL configuration for core project.
"""
from django.urls import path, include
from api.views import root_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', root_view, name='root'),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
