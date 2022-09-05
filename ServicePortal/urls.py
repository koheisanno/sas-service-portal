from django.contrib import admin
from django.urls import path, include, re_path
from portal.views import IndexTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include("portal.api.urls")),
    path('api-auth/', include("rest_framework.urls")),
    re_path(r"^(?!media).*$", IndexTemplateView.as_view(), name='entry-point')
]