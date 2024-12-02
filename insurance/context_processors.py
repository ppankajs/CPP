def s3_image_url(request):
    # Return the S3 image URL as part of the context
    return {
        's3_image_url': "https://elasticbeanstalk-us-east-1-779777417450.s3.amazonaws.com/bike.jpeg"
        # 's3_image_url': "https://prasannacpp.s3.us-east-1.amazonaws.com/bike.jpeg"
        # 's3_image_url' :  generate_presigned_url(bucket_name, image_name)
    }
