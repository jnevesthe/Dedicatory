from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import FAQ, Dedicatory


class FAQSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return FAQ.objects.filter(ativo=True, slug__isnull=False).exclude(slug='')

    def location(self, obj):
        return reverse('faq_detail', args=[obj.slug])


class DedicatorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Dedicatory.objects.filter(status='publico', slug__isnull=False).exclude(slug='')

    def location(self, obj):
        return reverse('public', args=[obj.slug])

    def lastmod(self, obj):
        return obj.criado_em


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['home', 'about', 'contact', 'faq', 'privacy', 'terms', 'listar_publicas', 'examples', 'search', 'create_dedicatory']

    def location(self, item):
        return reverse(item)
