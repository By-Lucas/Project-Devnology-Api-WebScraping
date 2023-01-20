from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions, authentication
from rest_framework.response import Response

from products.api.serializers import CategorySerializer, ProductSerializer
from products.models import Products, Category

import json


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

    



