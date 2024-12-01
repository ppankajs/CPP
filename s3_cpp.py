# import boto3
# import os

# def upload_image_to_s3(bucket_name="elasticbeanstalk-us-east-1-779777417450", 
#                       image_path="/home/ec2-user/environment/CPP/insurance/static/images/bike.jpeg", 
#                       image_name="bike.jpeg"):

#     # Initialize S3 client
#     s3_client = boto3.client("s3")
    
#     try:
#         # Upload the image to the specified S3 bucket
#         s3_client.upload_file(image_path, bucket_name, image_name)
#         print(f"Image {image_path} uploaded to {bucket_name}/{image_name}.")
        
#         # Generate a public S3 URL (if bucket policy allows public access)
#         s3_url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
#         print(f"Public URL: {s3_url}")
#         return s3_url
#     except Exception as e:
#         print(f"Error uploading image: {e}")
#         return None

# # Call the function
# if __name__ == "__main__":
#     bucket_name = "elasticbeanstalk-us-east-1-779777417450"
#     image_path = "/home/ec2-user/environment/CPP/insurance/static/images/bike.jpeg"
#     image_name = "bike.jpeg"

#     # Upload the image to S3
#     s3_url = upload_image_to_s3(bucket_name, image_path, image_name)

#     # If successful, print the image URL
#     if s3_url:
#         print(f"Image uploaded successfully. URL: {s3_url}")
import boto3
import os

def upload_image_to_s3(bucket_name="elasticbeanstalk-us-east-1-779777417450", 
                       image_path="/home/ec2-user/environment/CPP/insurance/static/images/bike.jpeg", 
                       image_name="bike.jpeg"):

    # Initialize S3 client
    s3_client = boto3.client("s3")
    
    try:
        # Upload the image to the specified S3 bucket
        s3_client.upload_file(image_path, bucket_name, image_name)
        print(f"Image {image_path} uploaded to {bucket_name}/{image_name}.")
        
        # Set the object ACL to public-read to make it publicly accessible
        s3_client.put_object_acl(ACL="public-read", Bucket=bucket_name, Key=image_name)
        print(f"ACL set to public-read for {image_name}.")

        # Generate a public S3 URL (if bucket policy allows public access)
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
        print(f"Public URL: {s3_url}")
        return s3_url
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

# Call the function
if __name__ == "__main__":
    bucket_name = "elasticbeanstalk-us-east-1-779777417450"
    image_path = "/home/ec2-user/environment/CPP/insurance/static/images/bike.jpeg"
    image_name = "bike.jpeg"

    # Upload the image to S3
    s3_url = upload_image_to_s3(bucket_name, image_path, image_name)

    # If successful, print the image URL
    if s3_url:
        print(f"Image uploaded successfully. URL: {s3_url}")
