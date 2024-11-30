import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region='us-east-1'):
    """Create an S3 bucket in a specified region.
    If a region is not specified, the bucket is created in us-east-1 by default.

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    try:
        if region == 'us-east-1':
            # us-east-1 does not require LocationConstraint
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=x)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(file_name, bucket, object_key=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_key: S3 object key. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    if object_key is None:
        object_key = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(
            file_name, bucket, object_key,
            ExtraArgs={'ACL': 'public-read'}  # Make file publicly accessible
        )
        print(f"File '{file_name}' uploaded to bucket '{bucket}' as '{object_key}'.")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='The name of the bucket to create.')
    parser.add_argument('--file_name', help='The name of the file to upload.')
    parser.add_argument('--object_key', help='The object key to use for the uploaded file.')
    parser.add_argument('--region', default='us-east-1', help='The region for the S3 bucket.')

    args = parser.parse_args()

    # Create bucket
    create_bucket(args.bucket_name, args.region)

    # Upload file if specified
    if args.file_name:
        upload_file(args.file_name, args.bucket_name, args.object_key)


if __name__ == '__main__':
    main()
