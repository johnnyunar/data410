from django.urls import path

from core.views import HomeView, PrivacyNoticeView, AboutView, APIHomeView, RoadmapView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("api/", APIHomeView.as_view(), name="api-home"),
    path("roadmap/", RoadmapView.as_view(), name="roadmap"),
    path("priacy-notice/", PrivacyNoticeView.as_view(), name="privacy-notice"),
]
