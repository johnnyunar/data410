from io import StringIO

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase

from metrics.models import RequestLog


class FlushRequestsCommandTest(TestCase):
    def setUp(self):
        self.cache_key = "test_request_counts"
        cache.delete(self.cache_key)  # Clear cache before each test

    def test_no_request_counts(self):
        """
        Test that the command handles an empty cache gracefully.
        """
        out = self._call_command()
        self.assertIn("No request counts to flush.", out)
        self.assertEqual(RequestLog.objects.count(), 0)

    def test_flush_new_request_counts(self):
        """
        Test that the command flushes new request counts from cache to the database.
        """
        # Add request counts to cache
        cache.set(
            self.cache_key,
            {
                "/": {"users": 10, "bots": 5},
                "/about": {"users": 8, "bots": 3},
            },
        )

        out = self._call_command()

        self.assertIn("Request counts flushed to the database.", out)

        logs = RequestLog.objects.all()
        self.assertEqual(logs.count(), 2)

        root_log = RequestLog.objects.get(path="/")
        self.assertEqual(root_log.user_count, 10)
        self.assertEqual(root_log.bot_count, 5)

        about_log = RequestLog.objects.get(path="/about")
        self.assertEqual(about_log.user_count, 8)
        self.assertEqual(about_log.bot_count, 3)

    def test_update_existing_request_counts(self):
        """
        Test that the command updates existing request logs in the database.
        """
        # Create an existing log in the database
        RequestLog.objects.create(path="/", user_count=5, bot_count=2)

        # Add updated request counts to cache
        cache.set(
            self.cache_key,
            {
                "/": {"users": 10, "bots": 5},
            },
        )

        out = self._call_command()

        self.assertIn("Request counts flushed to the database.", out)

        log = RequestLog.objects.get(path="/")
        self.assertEqual(log.user_count, 15)  # Existing + new
        self.assertEqual(log.bot_count, 7)  # Existing + new

    def test_flush_clears_cache(self):
        """
        Test that the cache is cleared after flushing request counts.
        """
        cache.set(
            self.cache_key,
            {
                "/": {"users": 10, "bots": 5},
            },
        )

        self._call_command()

        self.assertIsNone(cache.get(self.cache_key))

    def _call_command(self):
        """
        Helper method to call the management command and return its output.
        """

        out = StringIO()
        call_command("flushrequests", "--cache-key", self.cache_key, stdout=out)
        return out.getvalue()
