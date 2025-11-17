from .models import Category
from .views import get_ip

def user_ip(request):
    ip = get_ip(request)
    return {'user_ip': ip}

def categories_menu(request):
    return {
        'menu_categories': Category.objects.all().order_by('name')
    }