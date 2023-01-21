from bs4 import BeautifulSoup as bs4
from decouple import config
from loguru import logger
import pandas as pd
import requests
import typing
import sys
import json


logger.add("logs/info.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


class Scraping:

    def __init__(self) -> None:
        self.base_url = config('BASE_URL')
        self.scraping_url = config('SCRAPING_URL')

        self._headers = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "Content-Type": "application/json" 
        }

    def _make_request(self, method: str, endpoints: str, data: typing.Dict) -> None:
        if method:
            try:
                response = requests.request(method.upper(), self.base_url + endpoints, params=data, headers=self._headers)
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

    def scrapy(self, prod:typing.Union[str, int, float]=None) -> list:
        
        webpage = requests.get(self.scraping_url)
        sp = bs4(webpage.content, 'html.parser')

        base = 'https://webscraper.io/'
        
        div_home = sp.find_all('div', 'thumbnail')

        data = dict()
        products = []

        for home in div_home:
            data['title'] = home.find('a', class_='title').get_text(strip=True)
            data['image'] = base+home.find('img', class_='img-responsive').get('src')
            data['price']= home.find('h4', class_='price').get_text(strip=True)
            data['description'] = home.find('p', class_='description').get_text(strip=True)
            data['reviews'] = home.find('p', class_='pull-right').get_text(strip=True)
            
            if prod is not None:

                if isinstance(prod, str) and prod.capitalize() in data['title']:
                    products.append(json.dumps(data))

                elif isinstance(prod, int) and str(prod) in data['price']:
                    products.append(json.dumps(data))
                
                elif isinstance(prod, float) and str(prod) in data['price']:
                    products.append(json.dumps(data))
            else:
                products.append(json.dumps(data))

        return products

# if __name__ == "__main__":
#     _bs = Scraping()
#     print(_bs.scrapy('lenovo'))
