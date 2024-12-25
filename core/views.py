from django.views.generic import TemplateView

from registry.models import Service


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_services = Service.objects.all().order_by("-created_at")[:4]
        context["recent_services"] = recent_services
        return context
