import json
import boto3
from datetime import datetime
import pytz

def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("members")
        
    timezone = pytz.timezone('Europe/Berlin')
    today = datetime.now(timezone).date().isoformat()
        
    response = table.scan(
        FilterExpression="lastCheckin = :today",
        ExpressionAttributeValues={
            ":today": today
        }
    )
    
    members = response.get('Items', [])
    
    if len(members) < 2:
    	return {
    		"statusCode": 400,
    		"body": json.dumps("At least two members need to checkin")
    	}
    	
    
    boardMemberCheckedIn = False
    for member in members:
        name = member['name']
        if name == "Whizzy" or name == "Cello":
            boardMemberCheckedIn = True
    
    if not boardMemberCheckedIn:
        return {
            "statusCode": 400,
            "body": json.dumps("At least one board member needs to check in")
        }
    	
    
    for member in members:
        id = member['id']
        
        participations = member.get('participations')
        
        table.update_item(
            Key={
                "id": id
            },
            UpdateExpression="SET participations = :newParticipations",
            ExpressionAttributeValues={
                ":newParticipations": participations + 1
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps("Handled daily check for event")
    }
