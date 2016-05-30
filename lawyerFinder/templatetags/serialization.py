from django import template
from django.utils.translation import ugettext_lazy as _
from django.core.handlers.wsgi import logger

register = template.Library()

@register.filter(name='get_trans_string')
def get_trans_string(list):
    translated = ''
    for x in list:
        tmp = _(x)
        translated = translated + str(tmp) + "\t"
    return translated