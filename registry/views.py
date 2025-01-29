from django.db.models import Q
from django.views.generic import DetailView, TemplateView, ListView

from registry.models import Service


class ServiceDetail(DetailView):
    model = Service
    template_name = "registry/service_detail.html"
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return super().get_queryset()

        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_range"] = range(1, 6)
        context["uncategorized_service_infos"] = self.object.service_infos.filter(
            category__isnull=True
        )
        context["categorized_service_infos"] = self.object.service_infos.exclude(
            category__isnull=True
        ).order_by("category__name")

        return context


class RegistryView(ListView):
    template_name = "registry/registry.html"
    model = Service
    context_object_name = "services"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return super().get_queryset()

        return super().get_queryset().filter(is_active=True)


class ServiceHtmxSearchView(TemplateView):
    template_name = "registry/components/service/_service_list.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.POST.get("search")
        if search:
            context["services"] = Service.objects.filter(
                Q(is_active=True)
                & (Q(name__icontains=search) | Q(website__icontains=search))
            )
        else:
            context["empty_search"] = True
        return context
