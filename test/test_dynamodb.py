import pytest
from apps.controllers.dynamo_db import DynamoDB


def test_create_table_products():
    dynamodb = DynamoDB()
    dynamodb.create_table_products()
    tables = list(dynamodb.dynamodb.tables.all())
    tables_name = [table.name for table in tables]
    assert 'Products' in tables_name

def test_insert_products():
    dynamodb = DynamoDB()
    product_name = "product_name"
    detail = "detail"
    key = dynamodb.insert_products(product_name, detail)
    table = dynamodb.dynamodb.Table('Products')
    assert table
