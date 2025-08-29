import json
import requests  # now available due to the layer

def lambda_handler(event, context):
    try:
        api_key = 'xxxxxxxxxxxxxxx'
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'category': event['category'],
            'language': 'en',
            'apiKey': api_key,
            'pageSize': 3
        }
        # Make the GET request
        response = requests.get(url, params=params)
        data = response.json()
        list1 = list()
        # Optionally print articles to CloudWatch logs
        for article in data.get('articles', []):
            dict1 = dict()
            dict1['title'] = article['title']
            print('Title: ' + article['title'])
            dict1['url'] = article['url']
            print('url: ' + article['url'])
            dict1['publishedAt'] = article['publishedAt']
            print('publishedAt: ' + article['publishedAt'])
            print()
            list1.append(dict1)
        # Return the data as a JSON response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': list1
        }
    except: 
        raise
