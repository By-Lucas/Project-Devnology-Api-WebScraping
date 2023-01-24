from redis import Redis
import datetime
import json

class RedisCache:
    def __init__(self):
        """Iniciar a Classe Cache Redis"""
        self.redis = Redis(
            host='localhost',
            port='6379',
            db=0)

    def add_cache(self, product, list_products):
        """ Função adicionar dados de registro no Redis e definir o tempo de expiração para chave """
        days = datetime.timedelta(minutes=1)
        seconds = days.total_seconds()
        try:
            json_data = json.dumps(list_products)
            bytes_data = json_data.encode()

            self.redis.set(product, bytes_data)
            self.redis.expire(product, time=int(seconds))
            print('Registro adicionado a cache redis')
        except Exception as e:
            raise Exception('Obteve os seguinte erro:', e)

    def get_cache(self, product):
        """ Função obter dados de registro no Redis."""
        prod = self.redis.get(product)
        json_data = json.loads(prod)
        return json_data

    def registry_exists(self, product):
        """ Função para verificar se existem dados de registro no Redis."""
        prod_exist = self.redis.exists(product)
        return prod_exist

    def delete_registry(self, product):
        """ Função para excluir dados do registro no Redis."""
        self.redis.delete(product)
        print('Registro em cache deletado')