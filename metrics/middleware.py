import logging
import re

import redis
from django.core.cache import cache
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


class RequestLoggerMiddleware:
    CACHE_KEY = "request_counts"
    BOTS = [
        "bot",
        "spider",
        "crawler",
        "slurp",
        "bing",
        "google",
        "yahoo",
        "duckduck",
        "baidu",
        "yandex",
        "sogou",
        "exabot",
        "facebot",
        "ia_archiver",
    ]
    IGNORE_PATTERNS = [
        r"^/static/",
        r"^/media/",
        r"^/admin/",
        r"^/favicon.ico$",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.process_request(request)
        if response:  # Return response if any
            return response
        return self.get_response(request)

    def process_request(self, request):
        path = request.path_info

        # Check if the path matches any ignore patterns
        if self.is_ignored(path):
            return

        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()

        # Return 403 if User-Agent is missing
        if not user_agent:
            return HttpResponseForbidden("Access denied: Missing User-Agent.")

        # Determine if the request is from a bot
        is_bot = any(bot in user_agent for bot in self.BOTS)

        try:
            counts = cache.get(self.CACHE_KEY, {})

            if path not in counts:
                counts[path] = {"users": 0, "bots": 0}

            if is_bot:
                counts[path]["bots"] += 1
            else:
                counts[path]["users"] += 1

            # Save updated counts back to cache
            cache.set(self.CACHE_KEY, counts, timeout=None)
        except redis.exceptions.ConnectionError:
            logger.error("Redis connection error", exc_info=True)

    def is_ignored(self, path) -> bool:
        """
        Check if the path matches any of the ignore patterns.
        """
        for pattern in self.IGNORE_PATTERNS:
            if re.match(pattern, path):
                return True
        return False
