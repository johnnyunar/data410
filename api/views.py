from os.path import basename
from typing import Tuple
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet

from api.serializers import ServiceSerializer
from health.registry import HealthCheckRegistry
from registry.models import (
    Service,
    ServiceURL,
    ServiceInfo,
    ServiceInfoType,
    ServiceInfoCategory,
    ServiceInfoPoint,
)


class ServiceViewSet(ModelViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating, and deleting services.
    """

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        """
        POST: Import new services only.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        created_services = []
        skipped_services = []

        for service_data in data:
            created, instance, detail = self.import_service(service_data)
            service_info = {
                "name": service_data["name"],
                "url": request.build_absolute_uri(
                    reverse(
                        "api:service-detail",
                        kwargs={"slug": instance.slug},
                    )
                ),
                "detail": detail,
            }
            if created:
                created_services.append(service_info)
            else:
                skipped_services.append(service_info)

        response_status = (
            status.HTTP_201_CREATED if created_services else status.HTTP_200_OK
        )

        return Response(
            {
                "detail": "Service import completed.",
                "created": created_services,
                "skipped": skipped_services,
            },
            status=response_status,
        )

    def import_service(self, data) -> Tuple[bool, Service, str]:
        name = data.get("name")
        is_active = data.get("is_active", True)
        website = data.get("website")
        rating = data.get("rating")
        slug = data.get("slug")
        image_url = data.get("image")
        icon_class = data.get("icon_class")

        # Check if the service already exists
        if Service.objects.filter(name=name).exists():
            return (
                False,
                Service.objects.get(name=name),
                "Service with the same name already exists.",
            )

        if Service.objects.filter(slug=slug).exists():
            return (
                False,
                Service.objects.get(slug=slug),
                "Service with the same slug already exists.",
            )

        # Create the Service
        service = Service.objects.create(
            name=name,
            website=website,
            rating=rating,
            slug=slug,
            icon_class=icon_class,
            is_active=is_active,
        )

        # Download and save the image
        if image_url:
            self.download_and_save_image(service, image_url)

        # Process service URLs
        for url_data in data.get("service_urls", []):
            ServiceURL.objects.create(
                service=service, url_type=url_data["url_type"], url=url_data["url"]
            )

        # Process service infos
        for info_data in data.get("service_infos", []):
            self.add_service_info(service, info_data)

        return True, service, "Service imported successfully."

    def add_service_info(self, service, info_data):
        description = info_data.get("description")
        type_name = info_data.get("type")
        category_name = info_data.get("category")
        points = info_data.get("points", [])

        if not description or not type_name:
            return

        info_type, _ = ServiceInfoType.objects.get_or_create(name=type_name)
        category = None
        if category_name:
            category, _ = ServiceInfoCategory.objects.get_or_create(name=category_name)

        service_info = ServiceInfo.objects.create(
            service=service,
            type=info_type,
            category=category,
            description=description,
        )

        for point in points:
            ServiceInfoPoint.objects.create(
                service_info=service_info, text=point["text"].strip()
            )

    def download_and_save_image(self, service, image_url):
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            parsed_url = urlparse(image_url)
            filename = basename(parsed_url.path)
            service.image.save(filename, ContentFile(response.content), save=True)
        except requests.RequestException:
            service.image = None
            service.save()


class HealthCheckViewSet(ViewSet):
    """
    ViewSet for health check API.
    """

    # Staff only
    permission_classes = [IsAdminUser]

    def list(self, request):
        healthchecks = HealthCheckRegistry.get_registered_healthchecks()
        results = {check.name: check.check() for check in healthchecks}
        return Response(results)


class PingViewSet(ViewSet):
    """
    ViewSet for ping API.
    """

    permission_classes = []

    def list(self, request):
        return Response({"status": "ok"})
