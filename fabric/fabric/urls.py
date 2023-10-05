from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from notifications.views import *
from rest_framework import routers



router_client = routers.DefaultRouter()
router_client.register(r'client', ClientViewSet)

router_newsletter = routers.DefaultRouter()
router_newsletter.register(r'newsletter', NewsletterViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router_client.urls)),
    path("api/v1/", include(router_newsletter.urls)),
    path("api/v1/statistics/", StatisticsNewletterList.as_view(), name="statistics-list"),
    path("api/v1/statistics/<str:tag>/", StatisticsNewletterList.as_view(), name="statistics-tag"),
    path("api/v1/send_newsletter/<int:pk>/", NewsletterViewSet.as_view({"post": "send"})),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
