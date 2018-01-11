"""The router swagger application configuration."""
from django.apps import AppConfig


# pylint: disable=too-few-public-methods
class S3Connect(AppConfig):
  """The application configuration."""
  name = 'plos.doublehelix.s3_connect'

  def ready(self):
    """Initializes the settings during app start up."""
    import os
    from django.conf import settings as django_settings
    from plos.doublehelix.s3_connect import config

    super(S3Connect, self).ready()

    # Update the app config from Django's global settings.
    for setting_name in dir(config):
      if setting_name.startswith('S3_') or setting_name.startswith('AWS_'):
        s3_value = getattr(django_settings, setting_name, None)
        if s3_value:
          setattr(config, setting_name, s3_value)

    if not os.path.exists(config.S3_DOWNLOAD_DESTINATION):
      os.makedirs(config.S3_DOWNLOAD_DESTINATION)
# pylint: enable=too-few-public-methods
