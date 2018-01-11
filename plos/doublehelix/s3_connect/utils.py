""" AWS Signature v4 Key derivation functions.

See:
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photo-album.html
http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
"""

import hashlib
import hmac

from plos.doublehelix.s3_connect import config


def sign(key, message):
  return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


def get_aws_v4_signing_key(key, signing_date, region, service):
  datestamp = signing_date.strftime('%Y%m%d')
  date_key = sign(('AWS4' + key).encode('utf-8'), datestamp)
  k_region = sign(date_key, region)
  k_service = sign(k_region, service)
  k_signing = sign(k_service, 'aws4_request')
  return k_signing


def get_aws_v4_signature(key, message):
  return hmac.new(key, message.encode('utf-8'), hashlib.sha256).hexdigest()


def get_upload_params(upload_type='preprint', **kwargs):
  """Authorises user and validates given file properties."""
  dest = config.S3_DESTINATIONS.get(upload_type)

  # Validate request and destination config:
  allowed = dest.get('allowed')
  auth = dest.get('auth')
  key = dest.get('key')
  content_length_range = dest.get('content_length_range')

  if hasattr(key, '__call__'):
      object_key = key(**kwargs)
  elif key == '/':
      object_key = 'some_file.txt'
  else:
      object_key = '%s/%s' % (key.strip('/'), 'some_file.txt')

  bucket = dest.get('bucket') or config.S3_STORAGE_BUCKET_NAME
  region = dest.get('region') or config.S3_REGION
  endpoint = 's3.amazonaws.com' if region == 'us-east-1' else ('s3-%s.amazonaws.com' % region)

  # AWS credentials are not required for publicly-writable buckets
  access_key_id = config.AWS_ACCESS_KEY_ID

  bucket_url = 'https://{0}/{1}'.format(endpoint, bucket)

  upload_data = {
    'object_key': object_key,
    'access_key_id': access_key_id,
    'region': region,
    'bucket': bucket,
    'bucket_url': bucket_url,
    # 'cache_control': dest.get('cache_control'),
    # 'content_disposition': dest.get('content_disposition'),
    'acl': dest.get('acl') or 'private',
    # 'server_side_encryption': dest.get('server_side_encryption'),
  }
  return upload_data
