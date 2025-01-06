from django.urls import path

from core.views import HomeView
from registry.views import ServiceDetail, ServiceHtmxSearchView

urlpatterns = [
    path("search/", ServiceHtmxSearchView.as_view(), name="service-search"),
    path("<slug:slug>/", ServiceDetail.as_view(), name="service-detail"),
]
