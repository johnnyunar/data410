from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from registry.models import Service


class ServiceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            "home",
            "about",
            "api-home",
            "roadmap",
            "privacy-notice",
            "acknowledgements",
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {"services": ServiceSitemap, "static": StaticViewSitemap}
