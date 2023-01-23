from bs4 import BeautifulSoup as bs4

from decouple import config
from loguru import logger
import requests
import typing
import sys
import json

from rest_framework import status


logger.add("logs/info.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


class Scraping:

    def __init__(self) -> None:
        self.scraping_url = config('SCRAPING_URL')
        self.base = 'https://webscraper.io'

    def get_all_product(self) -> list:
        webpage = requests.get(self.scraping_url)
        sp = bs4(webpage.content, 'html.parser')
        div_home = sp.find_all('div', 'thumbnail')
        
        products = []
        for home in div_home:
            data = dict()
            data['title'] = home.find('a', class_='title').get_text(strip=True)
            data['image'] = self.base+home.find('img', class_='img-responsive').get('src')
            data['price']= home.find('h4', class_='price').get_text(strip=True)
            data['description'] = home.find('p', class_='description').get_text(strip=True)
            data['reviews'] = home.find('p', class_='pull-right').get_text(strip=True)
            products.append(data)

        return products

    def get_product(self, *args, **kwargs) -> list:
        webpage = requests.get(self.scraping_url)
        sp = bs4(webpage.content, 'html.parser')
        div_home = sp.find_all('div', 'thumbnail')
        
        product = args[0].get('product')
        price =  args[0].get('price')

        products = []
        for home in div_home:
            data = dict()
            data['title'] = home.find('a', class_='title').get_text(strip=True)
            data['image'] = self.base+home.find('img', class_='img-responsive').get('src')
            data['price']= home.find('h4', class_='price').get_text(strip=True)
            data['description'] = home.find('p', class_='description').get_text(strip=True)
            data['reviews'] = home.find('p', class_='pull-right').get_text(strip=True)
            
            try:
                if product is not None and product.capitalize() in data['title']:
                    products.append(data)
                elif price is not None and price.isnumeric() and str(price) in data['price']:
                    products.append(data)

            except Exception as e:
                raise Exception('Houve o seguinte erro:', e)

        return products
