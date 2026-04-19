from decouple import config
import os

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_LOCATION = config('AWS_LOCATION')
# AWS_S3_SIGNATURE_VERSION = 's3v4',
# AWS_QUERYSTRING_EXPIRE = 86400
# AWS_QUERYSTRING_EXPIRE = 300
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "public",
}
# AWS_DEFAULT_ACL = "public-read"
DEFAULT_FILE_STORAGE = "core.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "core.cdn.backends.StaticRootS3Boto3Storage"


import boto3
from botocore.client import Config
import logging

def create_presigned_url_do(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL to share a DigitalOcean Spaces object

    :param bucket_name: Name of the DigitalOcean Space
    :param object_name: Object key name (file path within the Space)
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Configure the boto3 session with the specific DigitalOcean endpoint
    session = boto3.session.Session()
    client = session.client(
        's3',
        region_name='nyc3',  # Replace with your Space's region (e.g., 'fra1')
        endpoint_url='https://nyc3.digitaloceanspaces.com', # Replace with your Space's endpoint
        aws_access_key_id=AWS_ACCESS_KEY_ID,  # Replace with your Access Key
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,  # Replace with your Secret Key
        config=Config(signature_version='s3v4') # Use v4 signature version
    )

    try:
        response = client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The generated URL can be used in a browser or program
    return response

# Example usage:
# url = create_presigned_url_do('my-space-name', 'path/to/my/file.txt', expiration=600)
# print(url)

