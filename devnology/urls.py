from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from decouple import config, Csv

from apps.products.api.viewsets import (ProductViewSet, CategoryViewSet, 
                                        ProductDetailViewSet, ProductScrapy, 
                                        AllProductScrapy)
from apps.accounts.api.viewsets import UserViewSet, UsersListViewSet

API_VERSION = config('API_VERSION')

class Devnology(routers.APIRootView):
    """
    Api Devnology - WebScraping
    """
    pass
class DocumentedRouter(routers.DefaultRouter):
    APIRootView = Devnology

router = DocumentedRouter()

router.register(r'usuario', UserViewSet, basename='Usuário')
router.register(r'usuarios', UsersListViewSet, basename='Usuários')
router.register(r'produtos', ProductViewSet, basename='Produtos')
router.register(r'categorias', CategoryViewSet, basename='Categorias')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_VERSION, include(router.urls)),
    path(f'{API_VERSION}product/<int:product_id>/', ProductDetailViewSet.as_view()),
    re_path(r'^api/v1/prod/(?P<prod>\w+)/$', ProductScrapy.as_view()),
    re_path(r'^api/v1/prod/', AllProductScrapy.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)