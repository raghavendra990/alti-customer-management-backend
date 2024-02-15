"""
Internal logger
"""
import logging
from django.conf import settings
from rest_framework.exceptions import ValidationError

LOGGER = logging.getLogger(settings.APPLICATION_NAME)


def raise_400(message, extra_log=None):
    """ raise_400 """
    LOGGER.info(f'[400] {message} {extra_log}')
    raise ValidationError(message)