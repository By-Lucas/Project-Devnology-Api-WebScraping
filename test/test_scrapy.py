import pytest
from apps.scraping.scraping import Scraping

import pytest

def test_get_all_product():
    scraping = Scraping()
    products = scraping.get_all_product()
    assert products != []
    assert all(key in products[0] for key in ['title', 'image', 'price', 'description', 'reviews'])


def test_get_product():
    scraping = Scraping()
    products = scraping.get_product({'product':'Asus'})
    assert products != []
    assert all(key in products[0] for key in ['title', 'image', 'price', 'description', 'reviews'])
    assert len(products) > 0

