"""Manages the S3 connection settings."""

import os

AWS_ACCESS_KEY_ID = 'AKIAICTERXFTIFIVFPTA'
AWS_SECRET_ACCESS_KEY = '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'

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 's3.bt.doublehelix.com')
S3_REGION = os.environ.get('S3_REGION', 'us-east-1')

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
