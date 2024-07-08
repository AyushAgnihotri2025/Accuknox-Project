from django.utils.deprecation import MiddlewareMixin

from AccuknoxProject.settings import CORS_ALLOWED_ORIGINS


# middleware.py
class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Set the CORS headers
        if request.get_host() in CORS_ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = request.get_host()
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        # If it's a preflight request, add additional headers
        if request.method == 'OPTIONS':
            print(request.get_host() in CORS_ALLOWED_ORIGINS)
            if request.get_host() in CORS_ALLOWED_ORIGINS:
                response['Access-Control-Allow-Origin'] = request.get_host()
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response['Access-Control-Max-Age'] = '86400'
            response.status_code = 200

        return response
