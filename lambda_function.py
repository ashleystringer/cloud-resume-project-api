import json
import boto3
from decimal import Decimal

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('visitor-count-table')
tableName = 'visitor-count-table'


def lambda_handler(event, context):
    # TODO implement
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
        if event['httpMethod'] == "GET" and event['path'] == "/count":
            
            response = table.get_item(Key={'id': '1'})
            body = response['Item']
            
            print (response['Item'])
            
            body = {
                'msg': "GET /count reached",
                'count': int(response['Item']['count'])
            }
        elif event['httpMethod'] == "PUT" and event['path'] == "/count":
            response = table.update_item(
                Key={
                    'id': '1'
                },
                UpdateExpression='SET #count = #count + :val',
                ExpressionAttributeNames={
                    '#count': 'count'
                },
                ExpressionAttributeValues={
                    ':val': 1
                },
                ReturnValues='UPDATED_NEW'
            )
            
            body = {
                'msg': "PUT /count reached",
                'count': int(response['Attributes']['count']) # Ensure count exists            
                }

    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    
    except Exception as err:
        statusCode = 500
        body = str(err)

    body = json.dumps(body)

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'https://cdn.ash-stringer-resume-project.com',
            'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT, GET'
        },
        'body': body
    }