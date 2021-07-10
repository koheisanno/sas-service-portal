from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from core.views import IndexTemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include("portal.api.urls")),
    path('api-auth/', include("rest_framework.urls")),
    re_path(r"^(?!media).*$", IndexTemplateView.as_view(), name='entry-point')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)