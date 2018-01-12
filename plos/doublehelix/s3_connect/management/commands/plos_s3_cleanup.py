"""Download objects from the S3 bucket."""

import logging

from django.core.management.base import BaseCommand

from plos.doublehelix.s3_connect import s3_utils

_LOGGER = logging.getLogger(__name__)


class Command(s3_utils.DeleteObjectMixin, BaseCommand):
  """Management command to download the files from a given directory."""
  help = 'Download files in a directory.'

  def add_arguments(self, parser):
    parser.add_argument('directory', nargs='+', type=str, help='Directory name.')

  def handle(self, *unused_args, **options):
    for dir_name in options['directory']:
      count_downloaded = self.s3_delete_contents(dir_name)
      self.write_msg('%s file(s) deleted from [%s]', count_downloaded, dir_name)

  def write_msg(self, msg_template, *args, style=None):
    """Write the message to `stdout` and to the log."""
    msg = msg_template.replace('%s', '{}').format(*args)
    style = style or 'success'
    if style == 'error':
      self.stdout.write(self.style.ERROR(msg))
    else:
      self.stdout.write(self.style.SUCCESS(msg))
    _LOGGER.info(msg_template, *args)
