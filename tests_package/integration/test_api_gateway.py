import os
import boto3
import unittest
from unittest import TestCase
from moto import mock_aws
import requests

'''
AWS_URL_NAME =<url-name> python3 -m unittest tests_package/ingration/test_api_gateway.py
'''

@mock_aws
class TestApiGateway(TestCase):
    def setUp(self):
        ##self.api_gw_domain = os.environ.get("AWS_URL_NAME")
        self.api_gw_domain = "cdux7s9cig.execute-api.us-east-2.amazonaws.com"
        print("Set up method")
    
    def tearDown(self):
        print("Tear down method")

    def api_gateway_domain(request):
        print("api_gateway_domain")
        ### env for aws region
        ### api-gw-domain
        ##return request.config.getoption('--api-gw-domain')

    def api_gateway_404(self):
        print("test API gateway 404")
        print(f"api_gw_domain - {self.api_gw_domain}")
        response = requests.get(f'https://cdux7s9cig.execute-api.us-east-2.amazonaws.com/count')
        print(response.headers)
        self.assertEqual(response.status_code, 404)
    