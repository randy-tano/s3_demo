"""Download objects from the S3 bucket."""

import boto3
import botocore
import logging
import os

from django.core.management.base import BaseCommand

from plos.doublehelix.s3_connect import config

_LOGGER = logging.getLogger(__name__)

_S3_RESOURCE = boto3.resource('s3')

_S3_BUCKET = _S3_RESOURCE.Bucket(config.S3_STORAGE_BUCKET_NAME)

_S3_CLIENT = boto3.client('s3')


class Command(BaseCommand):
  """Management command to download the files from a given directory."""
  help = 'Download files in a directory.'

  def add_arguments(self, parser):
    parser.add_argument('directory', nargs='+', type=str, help='Directory name.')

  def handle(self, *unused_args, **options):
    for dir_name in options['directory']:
      count_downloaded = self.s3_download(dir_name)
      self._write_msg('%s file(s) downloaded from [%s]', count_downloaded, dir_name)

  def s3_dir_contents(self, dir_name):
    """Query S3 bucket for the contents of the given directory."""
    _LOGGER.debug('Getting [%s/%s]', config.S3_STORAGE_BUCKET_NAME, dir_name)
    response = _S3_CLIENT.list_objects_v2(
      Bucket=config.S3_STORAGE_BUCKET_NAME,
      Prefix=dir_name)

    dir_contents = (bucket['Key'] for bucket in response['Contents'])
    return dir_contents

  def s3_download(self, dir_name):
    """Download files from the given directory."""
    dir_contents = self.s3_dir_contents(dir_name)
    file_count = 0
    for file_key in dir_contents:
      dir_name, file_name = file_key.split('/')
      self._write_msg('Downloading file [%s/%s]', dir_name, file_name)
      try:
        destination_dir = '%s/%s' % (config.S3_DOWNLOAD_DESTINATION, dir_name)
        os.makedirs(destination_dir, exist_ok=True)

        destination_file = '%s/%s' % (destination_dir, file_name)
        _S3_BUCKET.download_file(file_key, destination_file)
        file_count += 1
      except botocore.exceptions.ClientError as exception:
        if exception.response['Error']['Code'] == '404':
          _LOGGER.warn('The S3 object [%s] does not exist.', file_key)
        else:
          raise exception
    return file_count

  def _write_msg(self, msg_template, *args):
    """Write the message to `stdout` and to the log."""
    msg = msg_template.replace('%s', '{}').format(*args)
    self.stdout.write(msg)
    _LOGGER.info(msg_template, *args)
