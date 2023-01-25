from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication

from scraping.scraping import Scraping
from products.models import Products, Category
from products.api.serializers import CategorySerializer, ProductSerializer

#from controllers.dynamo_db import DynamoDB
from controllers.rediscache import RedisCache


class AllProductScrapy(APIView):
    """
    WebScrapin de produtos: https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops 
    Faça busca de todos os produtos ou de um produto específico (Nome ou Modelo) ou pelo preço (Número inteiro)
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    
    def get_object(self, request):
        try:
            product = Scraping()
            return product.get_all_product()
        except Exception as e:
            raise Exception(f'Houve o seguinte erro na consulta: {e}')

    def get(self, request, *args, **kwargs):

        prod = self.get_object(request)
        return Response(prod, status=status.HTTP_200_OK)


class ProductScrapy(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_object(self, prod:str=None):
        try:
            product = Scraping()
            return product.get_product(prod)
        except Exception as e:
            raise Exception(f'Houve o seguinte erro na consulta: {e}')
        
    def get(self, request, *args, **kwargs):
        #self.db = DynamoDB()
        self.cache = RedisCache()
        #self.db.create_table_products()

        product = request.GET.get('product')
        
        if self.request.GET.get('cache') is None:
            cache_query_string = True
        else:
            cache_query_string = eval(self.request.GET.get('cache'))

        if self.cache.registry_exists(product):
            product_list = self.cache.get_cache(product)

            response = {'product': product,
                        'cache': cache_query_string,
                        'product_list': product_list}
           
        else:
            prods = self.get_object(request.GET)
            #self.db.insert_products(product, prods) # Salvar no Dynamodb aws
            self.cache.add_cache(product, prods)
            
            response = {f'Products': product,
                        'cache': cache_query_string,
                        'product_list': prods
                        }
       
        if not cache_query_string:
            self.cache.delete_registry(product)
            #self.db.insert_products(product, prods)
        else:
            print('cache=True, Utilizando os dados em cache')
            self.cache.get_cache(product)
            
        return Response(response, status=status.HTTP_200_OK)


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
        else:
            raise Response(status=status.HTTP_400_BAD_REQUEST)

    



