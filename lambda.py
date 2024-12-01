import os
import zipfile
import boto3

def create_zip(zip_name="/home/ec2-user/environment/x23278480_CPP.zip", source_dir="/home/ec2-user/environment/CPP"):
    """
    Create a ZIP file from the contents of the source directory.
    """
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                print(f"Adding to ZIP: {file_path} as {arcname}")  # Debugging
                zipf.write(file_path, arcname)
    print(f"ZIP file created: {zip_name}")

# Function to deploy/update Lambda function
def deploy_lambda_function(function_name="prasannacpp", role_arn="arn:aws:iam::779777417450:role/LabRole",
                           zip_file_path="/home/ec2-user/environment/x23278480_CPP.zip", handler_name="lambda_function.lambda_handler",
                           runtime="python3.8"):
    """
    Deploy or update a Lambda function using the AWS SDK (boto3).
    Args:
        function_name (str): Name of the Lambda function.
        role_arn (str): ARN of the IAM Role for Lambda.
        zip_file_path (str): Path to the ZIP file containing the Lambda code.
        handler_name (str): Entry point for the Lambda function.
        runtime (str): Runtime environment (e.g., 'python3.8').
    """
    lambda_client = boto3.client("lambda")
    with open(zip_file_path, "rb") as f:
        zip_data = f.read()

    try:
        # Check if the function already exists
        lambda_client.get_function(FunctionName=function_name)
        # Update existing function's code
        lambda_client.update_function_code(FunctionName=function_name, ZipFile=zip_data)
        print(f"Updated Lambda function: {function_name}")
    except lambda_client.exceptions.ResourceNotFoundException:
        # Create a new Lambda function if it doesn't exist
        lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler_name,
            Code={"ZipFile": zip_data},
            Description="Automated Lambda Deployment",
            Timeout=15,
            MemorySize=128
        )
        print(f"Created new Lambda function: {function_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main script
if __name__ == "__main__":
    # Define paths and settings
    project_dir = "/home/ec2-user/environment/x23278480_CPP"  # Project folder to zip
    zip_output = "/home/ec2-user/environment/x23278480_CPP.zip"  # Output ZIP file path
    function_name = "prasannacpp"  # Lambda function name
    role_arn = "arn:aws:iam::779777417450:role/LabRole"  # IAM Role ARN
    handler_name = "lambda_function.lambda_handler"  # Entry point of the Lambda function

    # Step 1: Create ZIP file
    create_zip(zip_name=zip_output, source_dir=project_dir)

    # Step 2: Deploy Lambda function
    deploy_lambda_function(function_name, role_arn, zip_output, handler_name)