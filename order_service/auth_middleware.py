import os

import requests
from django.http.response import JsonResponse


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = requests.get(f'{os.environ.get('AUTH_SERVICE_URL')}/api/token/verify/',
                                headers={'Authorization': request.headers.get('Authorization')})
        if response.status_code != 200:
            return JsonResponse({'message': 'Unauthenticated'}, status=403)

        request.authenticated_user = response.json()

        response = get_response(request)
        return response

    return middleware
