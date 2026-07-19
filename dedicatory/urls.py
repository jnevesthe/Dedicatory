from django.urls import path
from .views import UpdateDedicatory, DeleteDedicatory
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import Home, About, Privacy, Contact, Terms



urlpatterns = [
    path('', Home.as_view(),  name='home'),
    path('about/', About.as_view(),  name='about'),
    path('faq/', views.faq_list, name='faq'),
    path('faq/<slug:slug>/', views.faq_detail, name='faq_detail'),    
    path('privacy/', Privacy.as_view(),  name='privacy'),
    path('contact/', Contact.as_view(),  name='contact'),
    path('terms/', Terms.as_view(),  name='terms'),
    path('dedicatory/<str:codigo>/', views.ver_dedicatoria, name='screen_dedicatory'),
    path('dedicatory/public/<slug:slug>/', views.ver_dedicatoria_publica, name='public'),
    path('search/', views.search, name='search'),
    path('create/', views.criar_dedicatoria, name='create_dedicatory'),
    path('confirm_edit/<str:codigo>/', views.confirmar_pin_edit, name='confirm_edit'),
    path('confirm_delete/<str:codigo>/', views.confirmar_pin_delete, name='confirm_delete'),
    path('update/<str:codigo>/', UpdateDedicatory.as_view(), name='edit'),
    path('delete/<str:codigo>/', DeleteDedicatory.as_view(), name='delete'),
    #path('sitemap.xml/', views.sitemap_view, name='sitemap'),    
    path("robots.txt", views.robots_txt, name='robots'),
    path('ads.txt', views.ads_txt_view, name='ads'),
    #path('ads.txt', views.ezoic_ads_txt, name='ezoic_ads_txt'),
    path('examples/', views.dedicatories, name='examples'),
    path('dedications/', views.v, name='listar_publicas'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'dedicatory.views.custom_404_redirect'  # Opcional, se quiser custom handler
