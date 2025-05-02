from django.urls import resolve
from django.http import HttpResponseNotFound
from django.conf import settings
from django.shortcuts import render,redirect
from django.urls import resolve
from django.conf import settings
from django.shortcuts import render

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow superusers to access everything
        if request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)

        try:
            resolver_match = resolve(request.path)
            url_name = resolver_match.url_name if resolver_match else None
        except:
            return self.get_response(request)  # If URL resolution fails, allow access

        # Handle anonymous users (before checking role-based access)
        if not request.user.is_authenticated:
            common_restricted_urls = getattr(settings, "COMMON_RESTRICTED_URLS", [])
            if url_name in common_restricted_urls:
                return render(request, 'error/404.html')

        # Common restricted URLs for all users
        common_restricted_urls = getattr(settings, "COMMON_RESTRICTED_URLS", [])
        if url_name in common_restricted_urls:
            return render(request, 'error/404.html')

        # Role-based restricted URLs
        role_restricted_urls = {
            "seller": getattr(settings, "SELLER_RESTRICTED_URLS", []),
            "buyer": getattr(settings, "BUYER_RESTRICTED_URLS", []),
            "agent": getattr(settings, "AGENT_RESTRICTED_URLS", []),
        }

        restricted_urls = role_restricted_urls.get(getattr(request.user, "member_type", ""), [])

        if url_name in restricted_urls:
            return render(request, 'error/404.html')

        return self.get_response(request)


# core/middleware.py
from django.http import Http404

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restrict access to Django admin
        if request.path.startswith('/admin/'):
            user = request.user
            if not user.is_authenticated or not (user.is_staff or user.is_superuser):
                raise Http404("Page not found")
        return self.get_response(request)

