"""Download objects from the S3 bucket."""

import logging

from django.core.management.base import BaseCommand

from plos.doublehelix.s3_connect import s3_utils

_LOGGER = logging.getLogger(__name__)


class Command(s3_utils.DeleteObjectMixin, BaseCommand):
  """Management command to delete the files from a given directory."""
  help = 'Delete all the files in a directory.'

  def add_arguments(self, parser):
    parser.add_argument('directory', nargs='+', type=str, help='Directory name.')

  def handle(self, *unused_args, **options):
    for dir_name in options['directory']:
      count_deleted = self.s3_delete_contents(dir_name)
      self.write_msg('%s file(s) deleted from [%s]', count_deleted, dir_name)

  def write_msg(self, msg_template, *args, style=None):
    """Write the message to `stdout` and to the log."""
    msg = msg_template.replace('%s', '{}').format(*args)
    style = style or s3_utils.STYLE_SUCCESS
    if style == s3_utils.STYLE_ERROR:
      self.stdout.write(self.style.ERROR(msg))
    else:
      self.stdout.write(self.style.SUCCESS(msg))
    _LOGGER.info(msg_template, *args)
