"""Manages the S3 connection settings."""

import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_IDENTITY_POOL_ID = os.environ.get('AWS_IDENTITY_POOL_ID')

S3_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
S3_REGION = os.environ.get('S3_REGION', 'us-east-1')
S3_DOWNLOAD_DESTINATION = '/tmp/plos_s3'

S3_DESTINATIONS = {
  'preprint': {
    'key': 'preprint/',
    'auth': True,
    'acl': 'authenticated-read',
    'allowed': [
        'image/jpeg',
        'image/png'
    ],
    'content_length_range': (1, 10000000),
  },
}
