from .models import VisitedLink
from django.http import HttpResponseNotFound
from django.urls import resolve


class VisitedLinksMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated :

            url = request.path
            if url.startswith('/case_detail/'):
                VisitedLink.objects.create(user=request.user, url=url)

        return response
    

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_superuser and resolve(request.path_info).app_name == 'admin':
            return HttpResponseNotFound()

        response = self.get_response(request)
        return response
    
