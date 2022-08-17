import re

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print("request source:::", request.META['HTTP_USER_AGENT'])
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        print(path)

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        print("url is exempt: ", url_is_exempt)

        if path == reverse('logout').lstrip('/'):
            logout(request)

        if not request.user.is_authenticated:
            if not url_is_exempt:
                return redirect(settings.LOGIN_URL)
        # elif request.user.is_authenticated or url_is_exempt:
        #     return None
        
        # elif not request.user.is_authenticated:
        #     if url_is_exempt:
        #         return None
            
        # else:
        #     return redirect(settings.LOGIN_URL)
