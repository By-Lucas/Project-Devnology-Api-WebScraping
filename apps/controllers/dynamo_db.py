import os
import uuid
from decouple import config
from botocore.exceptions import ClientError

import boto3


class DynamoDB:

    def __init__(self):
        """Iniciar classe DynamoDB """

        self.ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
        self.KEY_ID = config('AWS_ACCESS_KEY_ID')
        self.REGION = config('AWS_REGION')

        self.dynamodb = boto3.resource(service_name='dynamodb',
                                        region_name=self.REGION,
                                        aws_access_key_id=self.KEY_ID,
                                        aws_secret_access_key=self.ACCESS_KEY)
        self.key = str(uuid.uuid4())

    def create_table_products(self):
        """ Verifique se as tabelas existem, caso contrário a tabela é criada."""
        tables = list(self.dynamodb.tables.all())
        tables_name = [table.name for table in tables]

        if 'Products' not in tables_name:
            table = self.dynamodb.create_table(
                TableName='Products',
                KeySchema=[
                    {
                        'AttributeName': 'id_transaction',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'product',
                        'KeyType': 'RANGE'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id_transaction',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'product',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
        else:
            print('Tabela existente')

    # insert item
    def insert_products(self, product_name, detail):
        """ Lista de produtos no Dynamo"""
        table = self.dynamodb.Table('Products')
        try:
            response = table.put_item(Item={'id_transaction': self.key, 'product': product_name, 'detail': detail})
            print('Registro inserido no DynamoDB com sucesso')
            # return self.key
            
        except:
            print('Erro ao inserir registro na tabela')

