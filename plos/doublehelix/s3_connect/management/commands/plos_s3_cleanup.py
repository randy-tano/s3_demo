"""Download objects from the S3 bucket."""

import botocore
import logging
import os

from django.core.management.base import BaseCommand

from plos.doublehelix.s3_connect import config
from plos.doublehelix.s3_connect import s3_utils

_LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
  """Management command to download the files from a given directory."""
  help = 'Download files in a directory.'

  def add_arguments(self, parser):
    parser.add_argument('directory', nargs='+', type=str, help='Directory name.')

  def handle(self, *unused_args, **options):
    for dir_name in options['directory']:
      count_downloaded = self.s3_delete_contents(dir_name)
      self._write_msg('%s file(s) deleted from [%s]', count_downloaded, dir_name)

  def s3_dir_contents(self, dir_name):
    """Query S3 bucket for the contents of the given directory."""
    _LOGGER.debug('Getting [%s/%s]', config.S3_STORAGE_BUCKET_NAME, dir_name)
    prefix = '%s/' % dir_name
    response = s3_utils.S3_CLIENT.list_objects_v2(Bucket=config.S3_STORAGE_BUCKET_NAME,
                                                  Prefix=prefix)
    if response and 'Contents' in response:
      dir_contents = (bucket['Key'] for bucket in response['Contents'])
      return dir_contents

  def s3_delete_contents(self, dir_name):
    """Delete the given directory (and files)."""
    file_count = 0
    dir_contents = self.s3_dir_contents(dir_name)
    if dir_contents:
      for file_key in dir_contents:
        self._write_msg('Deleting file [%s]', file_key)
        try:
          s3_utils.S3_CLIENT.delete_object(Bucket=config.S3_STORAGE_BUCKET_NAME, Key=file_key)
          file_count += 1
        except botocore.exceptions.ClientError as exception:
          if exception.response['Error']['Code'] == '404':
            _LOGGER.warn('The S3 object [%s] does not exist.', file_key)
          else:
            raise exception
    return file_count

  def _write_msg(self, msg_template, *args, style=None):
    """Write the message to `stdout` and to the log."""
    msg = msg_template.replace('%s', '{}').format(*args)
    style = style or 'success'
    if style == 'error':
      self.stdout.write(self.style.ERROR(msg))
    else:
      self.stdout.write(self.style.SUCCESS(msg))
    _LOGGER.info(msg_template, *args)
