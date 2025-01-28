from django.urls import path, include

from health.views import HealthCheckDashboardView

urlpatterns = [
    path("", HealthCheckDashboardView.as_view(), name="health-dashboard"),
]
