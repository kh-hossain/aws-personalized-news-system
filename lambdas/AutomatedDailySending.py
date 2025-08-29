import json
import requests

def lambda_handler(event, context):
    try:
        url = 'https://xxxxxxx.execute-api.us-east-1.amazonaws.com/stage1'
        params = {'action': "readEntireTable"}
        # Make the POST request
        response = requests.post(url + "/UserProfileManagement", json=params)
        data = response.json()
        listOfEntiries = data["response"]["Items"]
        for entry in listOfEntiries:
            if entry['frequency'] == "daily":
                params = {'category': entry['preference']}
                # Make the POST request
                response = requests.post(url + "/ContentFetching", json=params)
                data = response.json()
                personalNewsList = data["body"]
                entireMessageBody = "Here are your personalized news:<br />"
                # Note <br /> = \n functionality in HTML
                for article in personalNewsList:
                    # the format of 'publishedAt': '2024-12-14T11:42:36Z', so we will use split to take just the date
                    messageBody = f"""<br />{article['title']}. <br /> To check the source, Press: {article['url']} <br />
                    published At {article['publishedAt'].split("T")[0]}. <br />"""
                    entireMessageBody = entireMessageBody + messageBody
                params = {
                    "source_email": "xxxxxxxxxxxx@gmail.com",
                    "recepient_email": entry["email"],
                    "subject": f"{entry['name']}, Your Personalized News in {entry['preference']}",
                    "body": entireMessageBody
                }
                response = requests.post(url + "/SendEmail", json=params)
                output = response.json()
        return {
                "message": "Daily email successfully sent. ",
                'statusCode': 200
            }
    except:
        raise
