import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name="prasannacpp", region="us-east-1"):
    """Create an S3 bucket in the specified region."""
    s3_client = boto3.client('s3', region_name=region)
    try:
        # Check if the bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Bucket does not exist, so create it
            print(f"Bucket {bucket_name} does not exist. Creating...")
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
            print(f"Bucket {bucket_name} created successfully.")
        else:
            print(f"Error checking bucket existence: {e}")

def upload_image_to_s3(bucket_name= "prasannacpp" , region = "us-east-1", image_path = "/home/ec2-user/environment/CPP/insurance/static/images/bike.jpeg", image_name = "bike.jpeg"):
    """Upload an image to S3 and return a pre-signed URL."""
    s3_client = boto3.client("s3", region_name=region)
    try:
        # Upload the image to the specified S3 bucket
        s3_client.upload_file(image_path, bucket_name, image_name)
        print(f"Image {image_path} uploaded to {bucket_name}/{image_name}.")
        
        # Generate a pre-signed URL for accessing the image
        pre_signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': image_name},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        print(f"Pre-signed URL: {pre_signed_url}")
        return pre_signed_url
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

# Main function
if __name__ == "__main__":
    bucket_name = "prasannacpp"  # Replace with your bucket name
    region = "us-east-1"  # Replace with your region
    image_path = "/home/ec2-user/environment/CPP/insurance/static/images/bike.jpeg"  # Replace with your image path
    image_name = "bike.jpeg"  # Replace with your desired object name in S3

    # Check if the bucket exists or create it
    create_bucket(bucket_name, region)

    # Upload the image to S3 and generate a pre-signed URL
    pre_signed_url = upload_image_to_s3(bucket_name, region, image_path, image_name)

    if pre_signed_url:
        print(f"Access the uploaded image using the following URL:\n{pre_signed_url}")
