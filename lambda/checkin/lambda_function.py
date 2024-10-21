import json
import boto3
from datetime import datetime

def lambda_handler(event, context):

    query_params = event.get("queryStringParameters", {})
    id = query_params.get("id", None)

    if id:
        
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("members")
        
        try:
            table.put_item(
                Item={
                    "id": str(id),
                    "last-checkin": datetime.utcnow().isoformat()
            }
        )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error persisting check-in!" + str(e))
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps("Received id " + str(id) + ".")
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps('No id was provided.')
    }
