"""Application context processors."""

from plos.doublehelix.s3_connect import config


def aws_credentials(unused_request):
  context = {
    'AWS_ACCESS_KEY_ID': config.AWS_ACCESS_KEY_ID,
    'AWS_SECRET_ACCESS_KEY': config.AWS_SECRET_ACCESS_KEY,
    'AWS_STORAGE_BUCKET_NAME': config.S3_STORAGE_BUCKET_NAME,
    'AWS_IDENTITY_POOL_ID': config.AWS_IDENTITY_POOL_ID,
    'S3_REGION': config.S3_REGION,
  }
  return context
