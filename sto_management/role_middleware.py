from django.shortcuts import redirect
from django.contrib import messages


class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if not request.user.is_authenticated:
            return self.get_response(request)

        is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
        is_manager = request.user.groups.filter(name='Manager').exists()
        is_master = request.user.groups.filter(name='Master').exists()

        if path.startswith('/admin/') and not is_admin:
            messages.error(request, 'У вас немає доступу до адмін-панелі.')
            return redirect('home')

        if is_master and not is_admin and not is_manager:
            allowed_exact_paths = [
                '/',
                '/login/',
                '/logout/',
            ]

            allowed_prefixes = [
                '/repairs/',
                '/repair/',
            ]

            is_allowed = (
                path in allowed_exact_paths
                or any(path.startswith(prefix) for prefix in allowed_prefixes)
            )

            if not is_allowed:
                messages.error(request, 'Майстер має доступ тільки до своїх ремонтів.')
                return redirect('home')

        return self.get_response(request)