"""
URL configuration for postogram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
URL_NAMESPACE = "changepoint-api"
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import settings



API_BASE = "api/"
urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_BASE, include('src.api')),
    path(API_BASE + 'schema/', SpectacularAPIView.as_view(), name='schema'),
    path(API_BASE + 'swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(API_BASE + 'auth/', include('djoser.urls')),
    path(API_BASE + 'auth/', include('djoser.urls.jwt')),
    path(API_BASE + 'auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(API_BASE + 'auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

