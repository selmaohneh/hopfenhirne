import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):

    query_params = event.get("queryStringParameters", {})
    name = query_params.get("name", None)
    id = uuid.uuid4()

    if id:
        
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("members")
        
        try:
            table.put_item(
                Item={
                    "id": str(id),
                    "name": str(name)
            }
        )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps("Error adding new user " + str(name))
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps("Added new user " + str(id))
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps('No name was provided')
    }
