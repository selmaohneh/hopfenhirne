import json
import boto3
from datetime import datetime
import pytz

def lambda_handler(event, context):

    query_params = event.get("queryStringParameters", {})
    id = query_params.get("id", None)

    if not id:
        return {
            "statusCode": 400,
            "body": json.dumps('No id was provided.')
        }

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("members")
        
    timezone = pytz.timezone('Europe/Berlin')
    lastCheckin = datetime.now(timezone).date().isoformat()
        
    getResponse = table.get_item(Key={"id": str(id)})

    if 'Item' not in getResponse:
        return {
            "statusCode": 404,
            "body": json.dumps(f"Member with id {id} does not exist.")
        }

    table.update_item(
        Key={
            "id": str(id)
        },
        UpdateExpression="SET lastCheckin = :lastCheckin",
        ExpressionAttributeValues={
            ":lastCheckin": lastCheckin
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Checked-in member with id " + str(id))
    }
