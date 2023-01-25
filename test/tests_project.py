import pytest
import typing
import requests
from loguru import logger

from apps.scraping.scraping import Scraping


"""Rodar teste: pytest test/tests_project.py -v"""

base_url = 'https:127.0.0.1:8000/api/v1'

headers = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json" ,
    "Authorization": 'token d4f5f6231166b31721513210a962bf706c1d5a76' # Token de autenticação
}


class TestDevnology:

    def _make_request(self, method: str, endpoints: str, data: typing.Dict) -> None:
        if method:
            try:
                response = requests.request(method.upper(), base_url + endpoints, params=data, headers=headers)
            except Exception as e:
                logger.error(f'Erro de conexão ao fazer {method} request para {endpoints}: {e}')
                raise Exception(f'Erro de conexão ao fazer {method} request para {endpoints}: {e}')
        else:
            ValueError()
        
        if response.status_code >= 200 and response.status_code <= 204:
            return response
        else:
            logger.error(f"Erro ao fazer {method} pedido para {endpoints}: {response.json()} (Erro de codigo {response.status_code})")
            raise Exception(f"Erro ao fazer {method} pedido para {endpoints}: {response.json()} (Erro de codigo {response.status_code})")
    
    @pytest.mark.asyncio
    async def test_products(self):
        data = {}
        response = self._make_request('GET', '/product', data)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_product(self, product='lenovo'):
        data = {}
        response = self._make_request('GET', f'/product?product={product}', data)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_scraping_products(self):
        scrapy = Scraping()
        result = scrapy.get_all_product(prod=None)
        assert result != ['']

    @pytest.mark.asyncio
    async def test_scraping_product(self, product='asus'):
        scrapy = Scraping()
        result = scrapy.get_product(prod=product)
        assert result != ['']
