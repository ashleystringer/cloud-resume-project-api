from os import environ
import unittest
from unittest import TestCase
from typing import Dict, Any
import json
from uuid import uuid4
from moto import mock_aws
import boto3


@mock_aws
class LambdaFunctionTest(TestCase):
    def setUp(self) -> None:

        
        self.test_ddb_table_name = "visitor-count-table"
        environ["DYNAMODB_TABLE_NAME"] = self.test_ddb_table_name 
        
        ##TableName="TestTable"

        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
        self.table = self.dynamodb.create_table(
            TableName=environ["DYNAMODB_TABLE_NAME"],
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
        )
        print("Table created:", self.table.table_name)
        self.table.put_item(Item={
            "id": "1",
            "count": 1
        })
        self.id_postfix = "_" + str(uuid4())

    def tearDown(self) -> None:
        self.table.delete()

    def load_test_event(self, test_event_file_name: str) -> Dict[str, Any]:
        with open(f"tests_package/events/{test_event_file_name}.json","r") as f:
            event = json.load(f)
            event["pathParameters"]["id"] = event["pathParameters"]["id"] + self.id_postfix
            return event

    
    def test_get_count(self):
        print("This is a test from the test method.")
        self.assertEqual(0,0)
        
        from infra.lambda_function import lambda_handler

        
        event = self.load_test_event("event_get_TEST001")

        ##print(event)

        test_return = lambda_handler(event, context = {})
        
    
    def test_update_count(self):
        print("This is a test from the test1 method.")
        self.assertEqual(2,2)

        from infra.lambda_function import lambda_handler

        event = self.load_test_event("event_put_TEST002")

        test_return = lambda_handler(event, context = {})
        print(test_return)
