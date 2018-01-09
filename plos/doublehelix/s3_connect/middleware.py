import logging

from django.utils.deprecation import MiddlewareMixin

_LOGGER = logging.getLogger(__name__)


class S3PreFlightMiddleware(MiddlewareMixin):

  def process_response(self, unused_request, response):
    _LOGGER.info('process_response: BEGIN')
    response['Access-Control-Allow-Origin'] = '*'
    return response
