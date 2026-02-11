"""
URL configuration for Art_Nouveau project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .models import Product
from .sitemaps import StaticViewSitemap, CategorySitemap
from .views import InfoView, LogsView, ProductsView, ProductView, ContactView, AddProductView, RegisterUserView, \
    LoginUserView, IndexView, AboutView, ProfileView, ConfirmEmailView, CreateDiscountView, Custom403View

handler403 = 'Art_Nouveau.views.custom_403_handler'

# Configurare GenericSitemap pentru Produse
# Deoarece Product nu are un câmp 'updated_at' sau 'date', nu setăm date_field.
products_info_dict = {
    'queryset': Product.objects.all(),
}

sitemaps = {
    'static': StaticViewSitemap,        # Paginile statice
    'categories': CategorySitemap,      # Modelul Category (Custom Sitemap)
    'products': GenericSitemap(         # Modelul Product (Generic Sitemap)
        products_info_dict,
        priority=0.9,
        changefreq='daily'
    ),
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", IndexView.as_view(), name='index'),
    path("about/", AboutView.as_view(), name="about"),
    path("info/", InfoView.as_view(), name="info"),
    path("logs/", LogsView.as_view(), name="logs"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("products/", ProductsView.as_view(), name="products"),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('category/<slug:category_slug>/', ProductsView.as_view(), name='category_products'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/',
         PasswordChangeView.as_view(template_name='Art_Nouveau/password_change.html',
                                               success_url='/password_change/done/'),
         name='password_change'),

    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='Art_Nouveau/password_change_done.html'),
         name='password_change_done'),
    path('confirm_mail/<str:code>/', ConfirmEmailView.as_view(), name='confirm_mail'),
    path('create_discount/', CreateDiscountView.as_view(), name='create_discount'),
    path('forbidden/', Custom403View.as_view(), name='forbidden'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
