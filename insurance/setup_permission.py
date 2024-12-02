import boto3

lambda_client = boto3.client('lambda')

response = lambda_client.add_permission(
    Action='lambda:InvokeFunction',
    FunctionName='Prasanna',  # Replace with your Lambda function name
    Principal='apigateway.amazonaws.com',  # Allows API Gateway to invoke the Lambda function
    StatementId='UniqueStatementIdForApiGateway',  # A unique statement ID to avoid conflicts
    SourceArn='arn:aws:execute-api:us-east-1:779777417450:oodof2x3xg/*/POST/'  # The ARN of the API Gateway POST method
)

print(response)