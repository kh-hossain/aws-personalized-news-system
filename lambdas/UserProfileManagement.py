import json
import boto3

ses_client = boto3.client('ses')
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('UserProfile')

def lambda_handler(event, context):
    try:
        action = event.get('action')
        if action == 'add':
            email = event.get('email')
            name = event.get('name')
            preference = event.get('preference')
            frequency = event.get('frequency')
            response=table.put_item(Item={'email':email,
                                          'name': name,
                                          'preference': preference,
                                          'frequency' :frequency})
            verifyMessage = ""
            if(not verifyEmail(email)): 
                verifyMessage = ", check your email for verification"
            return {"message": "added/modified entry" + verifyMessage, "response": response}
        elif action == "remove":
            email = event.get('email') # get key
            if not email:
                raise ValueError("Key information is missing from the event.")
            # Check if the item exists in the table
            get_response = table.get_item(Key= {"email": email})
            ses_client.delete_identity(Identity=email)
            if 'Item' not in get_response:
                return {
                    "message": "Item not found in the table",
                    "statusCode": 500
                }
            response = table.delete_item(Key= {"email": email})
            return {"message": email + " deleted", "response": response}
        elif action == 'readEntireTable':
            return  {"message": "entire table fetched", "response": table.scan()}
        elif action == 'readOneEntry':
            email = event.get('email')
            response = table.get_item(Key= {"email":email})
            return {"message": email + " entry fetched", "response": response}
        else:
            return  {"message": "undefined action", "data": event}
    except:
        raise

def verifyEmail(email):
    try:
        # List verified email addresses
        response = ses_client.list_verified_email_addresses()
        verified_emails = response.get('VerifiedEmailAddresses', [])
        if email in verified_emails:
            return True
        # If not verified, request email verification
        ses_client.verify_email_identity(EmailAddress=email)
        return False
    except:
        raise
