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
        days = datetime.timedelta(minutes=10)
        seconds = days.total_seconds()

        #self.redis.lrange(json.dumps(list_products, indent=2), 0, -1)
        self.redis.set(product, 'list_products')
        self.redis.expire(product, time=int(seconds))
        print('Registro adicionado a cache redis')

    def get_cache(self, product):
        """ Função obter dados de registro no Redis."""
        return self.redis.get(product)

    def registry_exists(self, product):
        """ Função para verificar se existem dados de registro no Redis."""
        return self.redis.exists(product)

    def delete_registry(self, product):
        """ Função para excluir dados do registro no Redis."""
        self.redis.delete(product)
        print('Registro em cache deletado')