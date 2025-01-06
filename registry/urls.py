from django.urls import path

from core.views import HomeView
from registry.views import ServiceDetail

urlpatterns = [
    path("<slug:slug>/", ServiceDetail.as_view(), name="service-detail"),
]
