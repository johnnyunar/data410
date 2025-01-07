import os

import markdown
from django.conf import settings
from django.views.generic import TemplateView

from registry.models import Service


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_services = Service.objects.all().order_by("-created_at")[:4]
        context["recent_services"] = recent_services
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class APIHomeView(TemplateView):
    template_name = "core/api-home.html"


class RoadmapView(TemplateView):
    template_name = "core/roadmap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        roadmap_path = os.path.join(settings.BASE_DIR, "ROADMAP.md")

        # Read and convert Markdown content
        with open(roadmap_path, "r", encoding="utf-8") as roadmap_file:
            md_content = roadmap_file.read()
            html_content = markdown.markdown(md_content, extensions=["extra", "toc"])

        context["roadmap_content"] = html_content
        return context


class PrivacyNoticeView(TemplateView):
    template_name = "core/privacy-notice.html"
