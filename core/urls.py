from django.urls import path

from core.views import (
    HomeView,
    PrivacyNoticeView,
    AboutView,
    APIHomeView,
    RoadmapView,
    AcknowledgementsView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("api-home/", APIHomeView.as_view(), name="api-home"),
    path("roadmap/", RoadmapView.as_view(), name="roadmap"),
    path("privacy-notice/", PrivacyNoticeView.as_view(), name="privacy-notice"),
    path("acknowledgements/", AcknowledgementsView.as_view(), name="acknowledgements"),
]
