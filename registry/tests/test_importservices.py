import json
import os
from io import StringIO
from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.test import TestCase
from requests import RequestException

from registry.models import (
    Service,
    ServiceURL,
    ServiceInfo,
    ServiceInfoType,
    ServiceInfoCategory,
)


class ImportServicesCommandTest(TestCase):
    def setUp(self):
        self.json_data = [
            {
                "name": "Test Service",
                "website": "https://example.com",
                "rating": 4.5,
                "slug": "test-service",
                "image": "https://example.com/logo.png",
                "icon_class": "fas fa-test",
                "service_urls": [
                    {"url_type": "Privacy Policy", "url": "https://example.com/privacy"}
                ],
                "service_infos": [
                    {
                        "description": "Test description",
                        "type": "Test Type",
                        "category": "Test Category",
                        "points": ["Point 1", "Point 2"],
                        "icon_class": "fas fa-info-circle",
                    }
                ],
            }
        ]
        self.invalid_file_path = "invalid.json"
        self.json_file_path = "test_services.json"
        with open(self.json_file_path, "w") as f:
            json.dump(self.json_data, f)

    def tearDown(self):
        # Clean up the test JSON file
        os.remove(self.json_file_path)
        if os.path.exists(self.invalid_file_path):
            os.remove(self.invalid_file_path)

    def test_import_new_service(self):
        out = StringIO()
        call_command("importservices", self.json_file_path, stdout=out)
        self.assertIn("Created service: Test Service", out.getvalue())

        service = Service.objects.get(name="Test Service")
        self.assertEqual(service.website, "https://example.com")
        self.assertEqual(service.rating, 4.5)
        self.assertEqual(service.slug, "test-service")

        service_urls = ServiceURL.objects.filter(service=service)
        self.assertEqual(service_urls.count(), 1)
        self.assertEqual(service_urls.first().url, "https://example.com/privacy")

        service_info = ServiceInfo.objects.filter(service=service).first()
        self.assertEqual(service_info.description, "Test description")
        self.assertEqual(service_info.type.name, "Test Type")
        self.assertEqual(service_info.category.name, "Test Category")

        points = service_info.points.all()
        self.assertEqual(points.count(), 2)
        self.assertEqual(points[0].text, "Point 1")

    def test_update_existing_service(self):
        # Create the service first
        Service.objects.create(
            name="Test Service",
            website="https://example.com",
            rating=3.0,
            slug="test-service",
        )
        out = StringIO()
        call_command("importservices", self.json_file_path, stdout=out)
        self.assertIn("Updated service: Test Service", out.getvalue())

        service = Service.objects.get(name="Test Service")
        self.assertEqual(service.rating, 4.5)  # Updated rating

    def test_skip_existing_service(self):
        Service.objects.create(name="Test Service", slug="test-service")
        out = StringIO()
        call_command(
            "importservices", self.json_file_path, "--skip-existing", stdout=out
        )
        self.assertIn("Skipped existing service: Test Service", out.getvalue())

        # Verify no duplicates were created
        self.assertEqual(Service.objects.filter(name="Test Service").count(), 1)

    def test_rewrite_service_infos(self):
        service = Service.objects.create(name="Test Service", slug="test-service")
        info_type = ServiceInfoType.objects.create(name="Test Type")
        category = ServiceInfoCategory.objects.create(name="Test Category")
        ServiceInfo.objects.create(
            service=service,
            type=info_type,
            category=category,
            description="Old description",
        )
        out = StringIO()
        call_command("importservices", self.json_file_path, "--rewrite", stdout=out)
        self.assertIn("Rewrote all service infos for: Test Service", out.getvalue())

        service_info = ServiceInfo.objects.get(service=service)
        self.assertEqual(
            service_info.description, "Test description"
        )  # Updated description

    def test_invalid_json_file(self):
        with open(self.invalid_file_path, "w") as f:
            f.write("{invalid_json}")
        out = StringIO()
        call_command("importservices", self.invalid_file_path, stdout=out, stderr=out)
        self.assertIn("Invalid JSON format in file", out.getvalue())

    def test_image_download(self):
        # Mock requests to simulate an image download
        mock_response = MagicMock()
        mock_response.content = b"fake_image_data"
        with patch("requests.get", return_value=mock_response):
            out = StringIO()
            call_command("importservices", self.json_file_path, stdout=out)
            self.assertIn(
                "Image downloaded and saved for service: Test Service", out.getvalue()
            )

        service = Service.objects.get(name="Test Service")
        self.assertTrue(service.image)

    def test_failed_image_download(self):
        # Mock requests to simulate a failed image download
        with patch("requests.get", side_effect=RequestException("Download failed")):
            out = StringIO()
            call_command("importservices", self.json_file_path, stderr=out)
            self.assertIn(
                "Failed to download image for service Test Service: Download failed",
                out.getvalue(),
            )

        service = Service.objects.get(name="Test Service")
        self.assertFalse(service.image)
