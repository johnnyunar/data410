import json
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from registry.models import (
    Service,
    ServiceURL,
    ServiceInfo,
    ServiceInfoType,
    ServiceInfoCategory,
    ServiceInfoPoint,
)
from urllib.parse import urlparse
from os.path import basename


class Command(BaseCommand):
    help = "Import service data from a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Path to the JSON file to import."
        )
        parser.add_argument(
            "--rewrite",
            action="store_true",
            help="Rewrite all service infos and points for each service.",
        )

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]
        rewrite = kwargs["rewrite"]

        try:
            with open(json_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(f"File not found: {json_file}")
            return
        except json.JSONDecodeError:
            self.stderr.write(f"Invalid JSON format in file: {json_file}")
            return

        # Normalize input to always be a list
        if isinstance(data, dict):
            data = [data]

        # Import the data
        for service_data in data:
            self.import_service(service_data, rewrite)

    def import_service(self, data, rewrite):
        name = data.get("name")
        website = data.get("website")
        rating = data.get("rating")
        slug = data.get("slug")
        image_url = data.get("image")
        icon_class = data.get("icon_class")

        # Create or update the Service
        service, created = Service.objects.update_or_create(
            name=name,
            defaults={
                "website": website,
                "rating": rating,
                "slug": slug,
                "icon_class": icon_class,
            },
        )

        # Download and save the image
        if image_url:
            success = self.download_and_save_image(service, image_url)
            if not success:
                service.image = None
                service.save()

        if created:
            self.stdout.write(f"Created service: {service.name}")
        else:
            self.stdout.write(f"Updated service: {service.name}")

        # Add service URLs
        for url_data in data.get("service_urls", []):
            url_type = url_data.get("url_type")
            url = url_data.get("url")
            ServiceURL.objects.get_or_create(
                service=service, url_type=url_type, url=url
            )

        # Add or update service infos
        if rewrite:
            self.rewrite_service_infos(service, data.get("service_infos", []))
        else:
            for info_data in data.get("service_infos", []):
                self.add_or_update_service_info(service, info_data)

        self.stdout.write(f"Successfully imported data for service: {service.name}")

    def rewrite_service_infos(self, service, infos):
        """
        Delete all existing ServiceInfo and related points for the given service.
        Then add new infos from the provided data.
        """
        ServiceInfo.objects.filter(service=service).delete()
        self.stdout.write(f"Rewrote all service infos for: {service.name}")

        for info_data in infos:
            self.add_or_update_service_info(service, info_data)

    def add_or_update_service_info(self, service, info_data):
        """
        Add or update a ServiceInfo object and its related points.
        """
        description = info_data.get("description", "").strip()
        type_name = info_data.get("type", "").strip()
        category_name = info_data.get("category")
        points = info_data.get("points", [])
        icon_class = info_data.get("icon_class", None)

        if not description or not type_name:
            self.stderr.write("Skipping ServiceInfo with missing description or type.")
            return

        # Ensure related objects exist
        info_type, _ = ServiceInfoType.objects.get_or_create(
            name=type_name,
            defaults={"icon_class": icon_class},
        )
        if icon_class and info_type.icon_class != icon_class:
            info_type.icon_class = icon_class
            info_type.save()

        category = None
        if category_name:
            category_name = category_name.strip()
            category, _ = ServiceInfoCategory.objects.get_or_create(name=category_name)

        # Check for existing ServiceInfo
        service_info, created = ServiceInfo.objects.update_or_create(
            service=service,
            type=info_type,
            category=category,
            defaults={"description": description},
        )

        if created:
            self.stdout.write(f"Created new ServiceInfo: {service_info.description}")
        else:
            self.stdout.write(
                f"Updated existing ServiceInfo: {service_info.description}"
            )

        # Update ServiceInfoPoints
        existing_points = set(service_info.points.values_list("text", flat=True))
        for point_text in points:
            if point_text.strip() not in existing_points:
                ServiceInfoPoint.objects.create(
                    service_info=service_info, text=point_text.strip()
                )

    def download_and_save_image(self, service, image_url):
        """
        Download an image from a URL and save it to the Service instance.
        Set image to None if the download fails.
        """
        user_agent = settings.DEFAULT_USER_AGENT
        headers = {
            "User-Agent": user_agent,
        }

        try:
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse the filename from the URL
            parsed_url = urlparse(image_url)
            filename = basename(parsed_url.path)

            # Save the image to the service instance
            service.image.save(filename, ContentFile(response.content), save=True)
            self.stdout.write(f"Image downloaded and saved for service: {service.name}")
            return True
        except requests.RequestException as e:
            self.stderr.write(
                f"Failed to download image for service {service.name}: {e}"
            )
            return False
