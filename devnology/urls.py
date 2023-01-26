from decouple import config

from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path

from rest_framework import routers
from rest_framework.authtoken import views

from apps.accounts.api.viewsets import UserViewSet, UsersListViewSet
from apps.products.api.viewsets import (ProductViewSet, CategoryViewSet, 
                                         ProductScrapy, 
                                        AllProductScrapy)


API_VERSION = config('API_VERSION')


class Devnology(routers.APIRootView):
    """
    Api Devnology - WebScraping
    """
    pass
class DocumentedRouter(routers.DefaultRouter):
    APIRootView = Devnology


router = DocumentedRouter()

# router.register(r'usuario', UserViewSet, basename='Usuário')
# router.register(r'produtos', ProductViewSet, basename='Produtos')
# router.register(r'usuarios', UsersListViewSet, basename='Usuários')
# router.register(r'categorias', CategoryViewSet, basename='Categorias')


urlpatterns = [
    path('admin/', admin.site.urls),
    #path(API_VERSION, include(router.urls)),
    path(f'{API_VERSION}api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path(f'{API_VERSION}product', ProductScrapy.as_view()), #/products?produto=lenovo
    path(f'{API_VERSION}products/', AllProductScrapy.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)