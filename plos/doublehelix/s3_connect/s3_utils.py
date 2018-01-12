"""S3 utilities.

See:
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photo-album.html
http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
"""
import boto3

from plos.doublehelix.s3_connect import config

S3_RESOURCE = boto3.resource('s3')

S3_BUCKET = S3_RESOURCE.Bucket(config.S3_STORAGE_BUCKET_NAME)

S3_CLIENT = boto3.client('s3')
