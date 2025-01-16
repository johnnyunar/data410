from django.core.cache import cache
from django.http import HttpResponse
from django.test import TestCase, RequestFactory

from metrics.middleware import RequestLoggerMiddleware


class RequestLoggerMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestLoggerMiddleware(get_response=self.dummy_response)
        self.cache_key = self.middleware.CACHE_KEY
        cache.delete(self.cache_key)  # Clear cache before each test

    def dummy_response(self, request):
        """A dummy response for testing."""
        return HttpResponse("OK")

    def test_user_request_logging(self):
        request = self.factory.get("/")
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0"
        self.middleware(request)

        counts = cache.get(self.cache_key)
        self.assertIsNotNone(counts)
        self.assertIn("/", counts)
        self.assertEqual(counts["/"]["users"], 1)
        self.assertEqual(counts["/"]["bots"], 0)

    def test_bot_request_logging(self):
        request = self.factory.get("/")
        request.META["HTTP_USER_AGENT"] = "Googlebot"
        self.middleware(request)

        counts = cache.get(self.cache_key)
        self.assertIsNotNone(counts)
        self.assertIn("/", counts)
        self.assertEqual(counts["/"]["bots"], 1)
        self.assertEqual(counts["/"]["users"], 0)

    def test_missing_user_agent_returns_403(self):
        request = self.factory.get("/")
        request.META["HTTP_USER_AGENT"] = ""
        response = self.middleware(request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.content.decode(), "Access denied: Missing User-Agent."
        )

    def test_ignores_static_requests(self):
        request = self.factory.get("/static/somefile.css")
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0"
        self.middleware(request)

        counts = cache.get(self.cache_key)
        self.assertIsNone(counts)  # No counts should be logged for ignored paths

    def test_ignores_favicon_requests(self):
        request = self.factory.get("/favicon.ico")
        request.META["HTTP_USER_AGENT"] = "Mozilla/5.0"
        self.middleware(request)

        counts = cache.get(self.cache_key)
        self.assertIsNone(counts)  # No counts should be logged for ignored paths

    def test_multiple_requests(self):
        request1 = self.factory.get("/")
        request1.META["HTTP_USER_AGENT"] = "Mozilla/5.0"
        self.middleware(request1)

        request2 = self.factory.get("/")
        request2.META["HTTP_USER_AGENT"] = "Googlebot"
        self.middleware(request2)

        counts = cache.get(self.cache_key)
        self.assertIsNotNone(counts)
        self.assertIn("/", counts)
        self.assertEqual(counts["/"]["users"], 1)
        self.assertEqual(counts["/"]["bots"], 1)

    def test_multiple_paths(self):
        paths = ["/", "/about", "/contact"]
        for path in paths:
            request = self.factory.get(path)
            request.META["HTTP_USER_AGENT"] = "Mozilla/5.0"
            self.middleware(request)

        counts = cache.get(self.cache_key)
        self.assertIsNotNone(counts)
        for path in paths:
            self.assertIn(path, counts)
            self.assertEqual(counts[path]["users"], 1)
            self.assertEqual(counts[path]["bots"], 0)
