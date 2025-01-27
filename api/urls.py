from django.urls import path, include
from rest_framework import routers

from api.views import ServiceViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"services", ServiceViewSet, basename="service")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
