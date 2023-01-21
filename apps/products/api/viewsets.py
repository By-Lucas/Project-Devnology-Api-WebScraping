from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions, authentication
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

from scraping.scraping import Scraping
from products.api.serializers import CategorySerializer, ProductSerializer
from products.models import Products, Category
import typing

import json


class AllProductScrapy(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_object(self):
        try:
            product = Scraping()
            return product.scrapy()
        except Exception as e:
            raise Exception(f'Houve o seguinte erro na consulta: {e}')

    def get(self, request, *args, **kwargs):
        prod = self.get_object()
        return Response(prod, status=status.HTTP_200_OK)


class ProductScrapy(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_object(self, prod:str=None):

        if isinstance(prod, str):
            prod = str(prod)
        if prod.isnumeric():
            prod = int(prod)
       
        try:
            product = Scraping()
            return product.scrapy(prod)
        except Exception as e:
            raise Exception(f'Houve o seguinte erro na consulta: {e}')
    
    def get(self, request, prod:typing.Union[str, int, float], *args, **kwargs):
        prods = self.get_object(prod)
        return Response(prods, status=status.HTTP_200_OK)


class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_object(self, product_id):
        try:
            return Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return None

    def get(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)

        serializer_context = {
                    'request': request,
                }
        
        if not product_instance:
            return Response(
                {"res": "Produto não existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(instance=product_instance, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(instance=product_instance, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        product_instance.delete()
        return Response(
            {"res": "Produto dedeletado!"},
            status=status.HTTP_200_OK
        )

class ProductDetailViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_object(self, product_id):
        try:
            return Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return None

    def get(self, request, product_id, *args, **kwargs):
        
        product_instance = self.get_object(product_id)

        serializer_context = {
                    'request': request,
                }
        
        if not product_instance:
            return Response(
                {"res": "Produto não existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(instance=product_instance, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(instance=product_instance, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, *args, **kwargs):
        product_instance = self.get_object(product_id)
        if not product_instance:
            return Response(
                {"res": "Produto não existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        product_instance.delete()
        return Response(
            {"res": "Produto dedeletado!"},
            status=status.HTTP_200_OK
        )



class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication] 
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = Products.objects.all()
        return query


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication] 
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            query = Category.objects.all()
            return query
        else :
            raise Response(status=status.HTTP_400_BAD_REQUEST)

    



