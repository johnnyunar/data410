from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META["HTTP_HOST"] in settings.HOST_ALIASES:
            # Redirect to the same path on the bare domain
            return HttpResponsePermanentRedirect(
                request.build_absolute_uri()
                .replace("www.", "", 1)
                .replace(request.META["HTTP_HOST"], settings.PRIMARY_HOST, 1)
            )
        elif request.META["HTTP_HOST"].startswith("www."):
            # Redirect to the same path on the bare domain
            return HttpResponsePermanentRedirect(
                request.build_absolute_uri().replace("www.", "", 1)
            )
        return self.get_response(request)
