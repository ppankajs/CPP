# lambda_function.py

def lambda_handler(event, context):
    """
    A simple Lambda function handler.
    
    Args:
        event (dict): The input data that the Lambda function receives.
        context (object): Metadata and information about the function invocation.

    Returns:
        dict: The response that Lambda will return.
    """
    print("Event received:", event)  # Log the event for debugging

    # Your business logic goes here. For now, we return a simple response.
    response = {
        "statusCode": 200,
        "body": "Lambda function executed successfully!"
    }

    return response
