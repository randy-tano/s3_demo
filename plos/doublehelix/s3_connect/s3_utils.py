"""S3 utilities.

See:
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photo-album.html
http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
"""

import boto3
import botocore
import logging
import os

from plos.doublehelix.s3_connect import config

_LOGGER = logging.getLogger(__name__)

S3_RESOURCE = boto3.resource('s3')

S3_BUCKET = S3_RESOURCE.Bucket(config.S3_STORAGE_BUCKET_NAME)

S3_CLIENT = boto3.client('s3')

STYLE_ERROR = 'error'

STYLE_SUCCESS = 'success'


class _BaseS3Util(object):
  """Base class for S3 operations."""

  @classmethod
  def s3_dir_contents(cls, dir_name):
    """Query S3 bucket for the contents of the given directory."""
    _LOGGER.debug('Getting [%s/%s]', config.S3_STORAGE_BUCKET_NAME, dir_name)
    prefix = '%s/' % dir_name
    response = S3_CLIENT.list_objects_v2(Bucket=config.S3_STORAGE_BUCKET_NAME,
                                         Prefix=prefix)
    if response and 'Contents' in response:
      dir_contents = (bucket['Key'] for bucket in response['Contents'])
      return dir_contents

  def write_msg(self, msg_template, *args):
    """Write the message to the log."""
    _LOGGER.info(msg_template, *args)


class DownloaderMixin(_BaseS3Util):
  """Downloads objects from S3."""

  def s3_download(self, dir_name):
    """Download files from the given directory."""
    file_count = 0
    dir_contents = self.s3_dir_contents(dir_name)
    if dir_contents:
      for file_key in dir_contents:
        dir_name, file_name = file_key.split('/')
        self.write_msg('Downloading file [%s/%s]', dir_name, file_name)
        try:
          destination_dir = '%s/%s' % (config.S3_DOWNLOAD_DESTINATION, dir_name)
          os.makedirs(destination_dir, exist_ok=True)

          destination_file = '%s/%s' % (destination_dir, file_name)
          S3_BUCKET.download_file(file_key, destination_file)
          file_count += 1
        except botocore.exceptions.ClientError as exception:
          if exception.response['Error']['Code'] == '404':
            _LOGGER.warn('The S3 object [%s] does not exist.', file_key)
          else:
            raise exception
    return file_count


class DeleteObjectMixin(_BaseS3Util):
  """Delete objects from S3."""

  def s3_delete_contents(self, dir_name):
    """Delete the given directory (and files)."""
    file_count = 0
    dir_contents = self.s3_dir_contents(dir_name)
    if dir_contents:
      for file_key in dir_contents:
        self.write_msg('Deleting file [%s]', file_key)
        try:
          S3_CLIENT.delete_object(Bucket=config.S3_STORAGE_BUCKET_NAME, Key=file_key)
          file_count += 1
        except botocore.exceptions.ClientError as exception:
          if exception.response['Error']['Code'] == '404':
            _LOGGER.warn('The S3 object [%s] does not exist.', file_key)
          else:
            raise exception
    return file_count
