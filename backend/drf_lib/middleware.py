from django.http import JsonResponse

from drf_lib.errors.error_format import format_error_response
from src.apps.core.constants import ErrorType

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # this method will be called every time when a middleware is called
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        
        formatted_response, status_code = format_error_response(
            exception_instance=exception, error_type=ErrorType.SERVER_ERROR
        )
        return JsonResponse(formatted_response, status=status_code) 
