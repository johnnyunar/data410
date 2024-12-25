from django.views.generic import DetailView

from registry.models import Service


class ServiceDetail(DetailView):
    model = Service
    template_name = "registry/service_detail.html"
    context_object_name = "service"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
