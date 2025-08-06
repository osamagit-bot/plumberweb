import time
import logging
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

logger = logging.getLogger(__name__)

class MonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Log slow requests
        duration = time.time() - start_time
        if duration > 2.0:  # Log requests taking more than 2 seconds
            logger.warning(f'Slow request: {request.path} took {duration:.2f}s')
        
        # Add performance headers
        response['X-Response-Time'] = f'{duration:.3f}s'
        
        return response