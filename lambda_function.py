import boto3
import uuid
import json

def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    sqs_client = boto3.client('sqs')

    try:
        # Get data from event
        topic_name = event['topic_name']
        user_email = event['user_email']
        admin_email = event['admin_email']
        queue_url = event['queue_url']

        # Create SNS Topic
        sns_response = sns_client.create_topic(Name=topic_name)
        topic_arn = sns_response['TopicArn']

        # Subscribe admin email to SNS Topic
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=admin_email
        )

        # Publish user creation notification to SNS
        message = f"A new user with email {user_email} has been successfully created!"
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="New User Registration Notification"
        )

        # Send message to SQS (FIFO)
        deduplication_id = str(uuid.uuid4())  # Generate unique deduplication ID for FIFO
        sqs_response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=f"New user registered with email: {user_email}",
            MessageGroupId='user-registration',  # FIFO Group ID
            MessageDeduplicationId=deduplication_id  # Deduplication ID
        )

        return {
            "status": "success",
            "sns_message_id": sns_response.get('MessageId'),
            "sqs_message_id": sqs_response.get('MessageId')
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            "status": "error",
            "message": str(e)
        }