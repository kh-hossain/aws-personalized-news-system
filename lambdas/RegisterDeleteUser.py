import json
import requests

def lambda_handler(event, context):
    try:
        if (event["action"] == "add"):
            url = 'https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/stage1'
            params = {
                'action': event["action"],
                "email": event["email"],
                "name": event["name"],
                "preference": event["preference"],
                "frequency": event["frequency"]
            }
            # Make the POST request
            response = requests.post(url + '/UserProfileManagement', json=params)
            dataResponse = response.json()
            return {
                'statusCode': 200,
                'response': dataResponse
            }
        elif (event["action"] == "remove"):
            url = 'https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/stage1'
            params = {
                'action': event["action"],
                "email": event["email"],
            }
            response = requests.post(url + '/UserProfileManagement', json=params)
            dataResponse = response.json()
            return {
                'statusCode': 200,
                'response': dataResponse
            }
        else:
            return  {"message": "undefined action", "data": event}
    except:
        raise
