import json
import boto3
import uuid

def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    name = query_params.get("name", None)
    id = uuid.uuid4()

    if name:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("members")
        
        try:
            scan = table.scan()
            members = scan.get('Items', [])
            nextNumber = -1 

            for member in members:
                number = member.get("number", -1)
                if number > nextNumber:
                    nextNumber = number
            
            
            nextNumber += 1

            table.put_item(
                Item={
                    "id": str(id),
                    "name": str(name),
                    "participations": 0,
                    "number": nextNumber
                }
            )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps("Error adding new user " + str(name) + ": " + str(e))
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps("Added new user " + str(id) + " with number " + str(nextNumber))
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('No name was provided')
        }
