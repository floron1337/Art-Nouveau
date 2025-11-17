"""
URL configuration for Art_Nouveau project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from .views import IndexView, InfoView, LogsView, AboutView, ProductsView, ContactView, CartView, ProductDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("products/", ProductsView.as_view(), name="products"),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', ProductsView.as_view(), name='category_products'),
    path("contact/", ContactView.as_view(), name="contact"),
    path("cart/", CartView.as_view(), name="cart"),
    path("info/", InfoView.as_view(), name="info"),
    path("logs/", LogsView.as_view(), name="logs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)