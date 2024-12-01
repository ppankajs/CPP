def s3_image_url(request):
    # Return the S3 image URL as part of the context
    return {
        's3_image_url': "https://elasticbeanstalk-us-east-1-779777417450.s3.amazonaws.com/bike.jpeg"
    }