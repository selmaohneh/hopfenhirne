import json
import boto3
from datetime import datetime
import pytz

def lambda_handler(event, context):

    query_params = event.get("queryStringParameters", {})
    id = query_params.get("id", None)

    if id:
        
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("members")
        
        timezone = pytz.timezone('Europe/Berlin')
        lastCheckin = datetime.now(timezone).date().isoformat()
        
        try:
            table.update_item(
                Key={
                    "id": str(id)
                },
                UpdateExpression="SET lastCheckin = :lastCheckin",
                ExpressionAttributeValues={
                    ":lastCheckin": lastCheckin
                }
            )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error persisting check-in!")
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps("Checked-in member with id " + str(id))
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps('No id was provided.')
    }
