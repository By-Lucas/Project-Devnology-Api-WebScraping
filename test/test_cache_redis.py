import pytest
from redis import Redis
from decouple import config
from apps.controllers.rediscache import RedisCache

@pytest.fixture
def redis_cache():
    return RedisCache()

def test_add_cache(redis_cache):
    product = "product1"
    list_products = [{"name": "product1", "price": 10.0}, {"name": "product2", "price": 20.0}]
    redis_cache.add_cache(product, list_products)
    assert redis_cache.registry_exists(product) == True

def test_get_cache(redis_cache):
    product = "product1"
    list_products = [{"name": "product1", "price": 10.0}, {"name": "product2", "price": 20.0}]
    redis_cache.add_cache(product, list_products)
    result = redis_cache.get_cache(product)
    assert result == list_products

def test_delete_registry(redis_cache):
    product = "product1"
    list_products = [{"name": "product1", "price": 10.0}, {"name": "product2", "price": 20.0}]
    redis_cache.add_cache(product, list_products)
    redis_cache.delete_registry(product)
    assert redis_cache.registry_exists(product) == False
