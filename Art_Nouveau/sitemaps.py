from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category

class StaticViewSitemap(Sitemap):
    """
    Sitemap pentru paginile statice care nu necesită autentificare.
    """
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # Numele rutelelor definite în urls.py
        return ['index', 'about', 'contact', 'register', 'login']

    def location(self, item):
        return reverse(item)

class CategorySitemap(Sitemap):
    """
    Sitemap custom pentru modelul Category.
    Folosim metoda get_absolute_url definita in model.
    """
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.all()