from django.contrib.auth import logout
from django.urls import reverse

class AdminLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path == reverse('admin:logout'):
            # Если пользователь на странице выхода из админ панели, выполнить выход
            logout(request)

        return response