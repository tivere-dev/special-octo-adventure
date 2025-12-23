from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta


class InactivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.last_activity:
                inactivity_limit = timedelta(minutes=settings.INACTIVITY_TIMEOUT)
                time_since_last_activity = timezone.now() - request.user.last_activity
                
                if time_since_last_activity > inactivity_limit:
                    from .models import RefreshToken
                    RefreshToken.invalidate_all_for_user(request.user)
                    
                    return Response(
                        {
                            'error': True,
                            'message': 'Your session has expired due to inactivity. Please login again.',
                            'code': 'session_expired'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            
            request.user.update_activity()

        response = self.get_response(request)
        return response
