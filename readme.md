# Story Generator with OpenAI, DALL-E, and Amazon Polly
This project generates a story based on two inputs: a name and a scene. The inputs are sent to OpenAI, which generates a story and saves it in a DynamoDB table. The DynamoDB stream then triggers two Lambda functions for image generation (using DALL-E) and voice generation (using Amazon Polly). This project is based on Implementing an event-driven, serverless story generation application with ChatGPT and DALL-E.

## Features

- Event-driven architecture using AWS Lambda, DynamoDB, and Amazon EventBridge.
- Story generation using OpenAI's GPT-3.
- Image generation using OpenAI's DALL-E.
- Voice generation using Amazon Polly.


## Architecture
1. An Amazon EventBridge scheduled event triggers the story generation Lambda function once a day.
2. The story generation Lambda function takes a name and a scene from dynamodb table, sends them to OpenAI's GPT-3, and saves the generated story in a DynamoDB table.
3. The insertion of a new story into the DynamoDB table triggers two Lambda functions: one for image generation using DALL-E, and one for voice generation using Amazon Polly.
4. The image and audio files are stored in an Amazon S3 bucket.


## Prerequisites
- AWS account with access to Lambda, DynamoDB, EventBridge, S3, and Amazon Polly.
- AWS CLI installed and configured.
- Node.js installed.
- Serverless Framework installed.

## Deployment

# Still to finish

- fix voice generator
- fix Front end
- to add lamday layers
- deployment commands
- Tests


