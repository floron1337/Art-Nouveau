from .views import get_ip

def user_ip(request):
    ip = get_ip(request)
    return {'user_ip': ip}