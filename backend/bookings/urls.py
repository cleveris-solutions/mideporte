from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),


    # Docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # JSON scheme
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger 
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Redoc
]
