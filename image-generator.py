import json
from typing import TypedDict
from aws_lambda_powertools import Logger
import boto3
from botocore.exceptions import ClientError
import requests
import os

eventbridge = boto3.client('events')
secrets_manager = boto3.client('secretsmanager')
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

logger = Logger()

class EventBridgeEvent(TypedDict):
    version: str
    id: str
    detail_type: str
    source: str
    account: str
    time: str
    region: str
    resources: list
    detail: dict

def get_secret_value(secret_id):
    secret_id = "dev/openai/api"
    secret = secrets_manager.get_secret_value(SecretId=secret_id)
    
    if 'SecretString' in secret:
        return json.loads(secret['SecretString'])
    else:
        return json.loads(secret['SecretBinary'])

def create_image(event):
    api_key = get_secret_value('dev/openai/api')['OPENAI_API']
    new_image = event['Records'][0]['dynamodb']['NewImage']

    prompt = new_image['scene']['S']
    print("prompt:  ", prompt)
    #prompt = event['NewImage']['scene']

    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json={
            'prompt': prompt,
            'n': 1,
            'size': '256x256'
        }
    )

    response.raise_for_status()

    data = response.json()
    images = [item['url'] for item in data['data']]
    image_url = images[0]
    bucket = os.environ.get('story_bucket')
    response = requests.get(image_url)
    response.raise_for_status()
    image_data = response.content
    tableName = os.environ.get('stories')

    s3.put_object(
    Bucket=bucket,
    Key=f"stories/{new_image['id']['S']}/image.png",
    Body=image_data,
    ContentType='image/png',
    Metadata={
        'Content-Type': 'image/png'})


    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': f"stories/{new_image['id']['S']}/image.png",
        },
        ExpiresIn=172800
    )

    dynamodb.update_item(
        TableName=tableName,
        Key={
            'id': {'S': new_image['id']['S']}
        },
        UpdateExpression='SET thumbnail = :thumbnail',
        ExpressionAttributeValues={
            ':thumbnail': {'S': url}
        }
    )

    logger.info('Thumbnail created')

def lambda_handler(event, context):
    print ("event:", event)
    try:
        create_image(event)
    except ClientError as e:
        logger.exception(f"Failed to create thumbnail: {str(e)}")
        raise






