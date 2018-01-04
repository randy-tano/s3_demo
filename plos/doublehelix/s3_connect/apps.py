"""The router swagger application configuration."""
from django.apps import AppConfig


# pylint: disable=too-few-public-methods
class S3Connect(AppConfig):
  """The application configuration."""
  name = 'plos.doublehelix.s3_connect'
# pylint: enable=too-few-public-methods
