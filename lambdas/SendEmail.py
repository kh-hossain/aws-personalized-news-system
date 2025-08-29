import json
import boto3

ses_client = boto3.client("ses")

def lambda_handler(event, context):
    try:
        subject = event['subject']
        source_email = event['source_email']
        recepient_email = event['recepient_email']
        body = event['body']

        if (not verifyEmail(source_email)):
            return {"message": "source mail needs verification, verification email sent", "statusCode": 500}

        if (not verifyEmail(recepient_email)):
            return {"message": "recepient mail needs verification, verification email sent", "statusCode": 500}

        message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}

        response = ses_client.send_email(Source = source_email,
                                         Destination = {"ToAddresses": [recepient_email]},
                                         Message = message)

        return {"message": "email sent successfully", "response": response}
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
