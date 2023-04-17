import boto3
from boto3.dynamodb.types import TypeDeserializer
from datetime import datetime, timedelta
import os
from uuid import uuid4
import random
import json
import openai

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Retrieve the OpenAI API key from Secrets Manager
    secret_name = "dev/openai/api"
    region_name = "ap-southeast-2"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
   
   # Initialize the OpenAI API key
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    api_key = get_secret_value_response['SecretString']
    secret_dict = json.loads(api_key)
    openai_api_key = secret_dict['OPENAI_API']
    openai.api_key = openai_api_key.strip()
    

    # Get all characters from the characters DynamoDB table
    characters_response = dynamodb_client.scan(TableName=os.environ['names_table'])
    deserializer = TypeDeserializer()
    characters = [deserializer.deserialize(item['name']) for item in characters_response['Items']]
    selected_Characters = random.sample(characters, 2)


    # Get all scenes from the scenes DynamoDB table
    scenes_response = dynamodb_client.scan(TableName=os.environ['scenes_table'])
    deserializer = TypeDeserializer()
    descriptions = [deserializer.deserialize(item['description']) for item in scenes_response['Items']]
    selected_descriptions = random.sample(descriptions, 1)


    prompt = f"""
        Write a title and a rhyming story on {len(characters)} main characters called {', '.join(selected_Characters)}.
        The story needs to be set within the scene {selected_descriptions[0]}  and be at least 300 words long
    """
    
    # Use OpenAI to generate a story
    response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,)
   
    story = response.choices[0].text.strip()
 
    story_parts = story.split('\n')
    

    # Get the title and description of the story
    title = story_parts[0]
    description = '\n'.join(story_parts[1:])

    # Insert the new story into the stories DynamoDB table
    two_days_from_now = datetime.now() + timedelta(days=2)
    story_ttl = int(two_days_from_now.timestamp())

    
    dynamodb_client.put_item(
        TableName=os.environ['STORIES_TABLE'],
        Item={
            'id': {'S': str(uuid4())},
            'title': {'S': title},
            #'characters': {'L': [TypeDeserializer().serialize(character) for character in characters]},
            'description': {'S': description},
            'ttl': {'N': str(story_ttl)},
            'scene': {'S': selected_descriptions[0]},
            'createdAt': {'S': datetime.now().isoformat()},
        }
    )



#selected_scene['description']