# middleware.py
import logging

class GelatoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to execute for each request before
        # the view (and later middleware) are called.
        logging.info(f'Received request from Django: {request.method} {request.path}')

        response = self.get_response(request)

        # Code to execute for each response after
        # the view is called.
        return response
