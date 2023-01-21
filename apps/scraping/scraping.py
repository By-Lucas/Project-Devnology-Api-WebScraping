from bs4 import BeautifulSoup as bs
import typing
import sys
import requests
from decouple import config

from loguru import logger

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


    def _make_request(self, method: str, endpoints: str, data: typing.Dict):
        if method:
            try:
                response = requests.request(method, self.base_url + endpoints, params=data, headers=self._headers)
            except Exception as e:
                logger.error('Erro de conexão ao fazer %s request para %s: %s', method, endpoints, e)
                return None
        else:
            ValueError()
        
        if response.status_code >= 200 and response.status_code <= 204:
            return response
        
        else:
            logger.error("Erro ao fazer %s pedido para %s: %s (Erro de codigo %s)",
                        method, endpoints, response.json(), response.status_code)
            
            return None

if __name__ == "__main__":
    _bs = Scraping()
