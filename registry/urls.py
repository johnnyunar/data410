from django.urls import path

from core.views import HomeView
from registry.views import ServiceDetail

urlpatterns = [
    path("service/<uuid:uuid>/", ServiceDetail.as_view(), name="service-detail"),
]
