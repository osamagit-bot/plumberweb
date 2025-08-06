"""
Custom middleware for handling separate admin and customer sessions
"""
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


class SeparateSessionMiddleware(SessionMiddleware):
    """
    Custom session middleware that uses different session cookies
    for admin and customer areas to prevent session conflicts.
    """
    
    def process_request(self, request):
        # Store original session cookie name
        original_cookie_name = getattr(settings, 'SESSION_COOKIE_NAME', 'sessionid')
        
        # Determine which session cookie to use based on the URL path
        if request.path.startswith('/admin/'):
            # Use admin session cookie for admin area
            settings.SESSION_COOKIE_NAME = getattr(settings, 'ADMIN_SESSION_COOKIE_NAME', 'admin_sessionid')
        elif request.path.startswith('/portal/'):
            # Use customer session cookie for customer portal
            settings.SESSION_COOKIE_NAME = getattr(settings, 'CUSTOMER_SESSION_COOKIE_NAME', 'customer_sessionid')
        else:
            # Use default session cookie for main website
            settings.SESSION_COOKIE_NAME = 'sessionid'
        
        # Call the parent process_request method
        super().process_request(request)
        
        # Restore original cookie name
        settings.SESSION_COOKIE_NAME = original_cookie_name
    
    def process_response(self, request, response):
        # Store original session cookie name
        original_cookie_name = getattr(settings, 'SESSION_COOKIE_NAME', 'sessionid')
        
        # Ensure the correct session cookie name is used in the response
        if request.path.startswith('/admin/'):
            settings.SESSION_COOKIE_NAME = getattr(settings, 'ADMIN_SESSION_COOKIE_NAME', 'admin_sessionid')
        elif request.path.startswith('/portal/'):
            settings.SESSION_COOKIE_NAME = getattr(settings, 'CUSTOMER_SESSION_COOKIE_NAME', 'customer_sessionid')
        else:
            settings.SESSION_COOKIE_NAME = 'sessionid'
        
        # Call the parent process_response method
        response = super().process_response(request, response)
        
        # Restore original cookie name
        settings.SESSION_COOKIE_NAME = original_cookie_name
        
        return response