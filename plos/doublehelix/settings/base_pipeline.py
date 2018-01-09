"""Asset pipeline settings."""

PIPELINE = {
  'STYLESHEETS': {},
  'JAVASCRIPT': {},
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
