from django.utils.deprecation import MiddlewareMixin


# middleware.py
class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Set the CORS headers
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        # If it's a preflight request, add additional headers
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response['Access-Control-Max-Age'] = '86400'
            response.status_code = 200

        return response
