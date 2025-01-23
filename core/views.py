import os

import markdown
import requests
from django.conf import settings
from django.core.cache import cache
from django.views.defaults import page_not_found, server_error
from django.views.generic import TemplateView

from registry.models import Service


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_services = Service.objects.filter(is_active=True).order_by(
            "-created_at"
        )[:4]
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


class AcknowledgementsView(TemplateView):
    template_name = "core/acknowledgements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check cache for dependencies data
        cached_data = cache.get("dependencies_data")
        if cached_data:
            context["dependencies"] = cached_data
            return context

        # Path to requirements.txt
        requirements_path = os.path.join(settings.BASE_DIR, "requirements.txt")
        dependencies = []

        with open(requirements_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):  # Skip comments and empty lines
                    if "==" in line:
                        package, version = line.split("==")
                        metadata = self.get_package_metadata(package.strip())
                        dependencies.append(
                            {
                                "name": package.strip(),
                                "version": version.strip(),
                                "description": metadata.get("description"),
                                "url": metadata.get("url"),
                            }
                        )

        # Cache dependencies data for 7 days
        cache.set("dependencies_data", dependencies, 7 * 24 * 60 * 60)

        context["dependencies"] = dependencies
        return context

    def get_package_metadata(self, package_name):
        """Fetch metadata for a package from PyPI."""
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "description": data["info"].get(
                        "summary", "No description available."
                    ),
                    "url": data["info"].get("project_url")
                    or data["info"].get("package_url"),
                }
        except requests.RequestException:
            pass
        return {"description": "No description available.", "url": None}


class NotFoundView(TemplateView):
    template_name = "core/404.html"

    def dispatch(self, request, exception=None, *args, **kwargs):
        return page_not_found(request, exception, template_name=self.template_name)


class ServerErrorView(TemplateView):
    template_name = "core/500.html"

    def dispatch(self, request, *args, **kwargs):
        return server_error(request, template_name=self.template_name)


class RobotsView(TemplateView):
    template_name = "core/robots.txt"
    content_type = "text/plain"
