import json

def lambda_handler(event, context):

    query_params = event.get('queryStringParameters', {})
    userId = query_params.get('guid', None)

    if userId:
        statusCode = 200
        responseMessage = "Received userId " + str(userId) + "."
    else:
        statusCode = 400
        responseMessage = 'No userId was provided.'

    return {
        "statusCode": statusCode,
        "body": json.dumps(responseMessage)
    }
