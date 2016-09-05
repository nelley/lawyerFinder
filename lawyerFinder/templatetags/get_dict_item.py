from django import template
from django.core.handlers.wsgi import logger

register = template.Library()

@register.filter(name='get_dict_item')
def get_dict_item(dictionary, key):
    logger.debug('key=%s' % key)
    return dictionary.get(key)