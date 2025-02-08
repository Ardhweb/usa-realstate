from django.urls import resolve
from django.http import HttpResponseNotFound
from django.conf import settings

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the current view's URL name
            resolver_match = resolve(request.path)
            url_name = resolver_match.url_name if resolver_match else None

            # If the user is a patient and the URL is restricted, return 404
            if getattr(request.user, "role", None) == "patient":
                if url_name in getattr(settings, "RESTRICTED_URL_NAMES", []):
                    return HttpResponseNotFound("<h1>404 Not Found</h1>")

        return self.get_response(request)
