import boto3
import os

polly = boto3.client('polly')

def text_to_speech(event, context):
    new_image = event['Records'][0]['dynamodb']['NewImage']
    story_text = new_image['description']['S']
    story_id = new_image['id']['S']
    output_bucket = os.environ.get('audio_bucket')

    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=story_text,
        VoiceId='Joanna', # Choose the voice you prefer
        TextType='ssml'
    )

    audio_data = response['AudioStream'].read()

    s3 = boto3.resource('s3')
    s3.Bucket(output_bucket).put_object(
        Key=f"stories/{story_id}/audio.mp3",
        Body=audio_data,
        ContentType='audio/mpeg'
    )
