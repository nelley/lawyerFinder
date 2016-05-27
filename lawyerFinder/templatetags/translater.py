from django import template
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.core.handlers.wsgi import logger

register = template.Library()

@register.filter(name='get_translate')
def get_translate(dict):

    sortedDict = OrderedDict(sorted(dict.items(), key=lambda t: t[0]))
    for k in sortedDict.keys(): #if not use keys(), it will cause runtime error
        k_output = _(k)
        sortedDict[k_output] = sortedDict.pop(k)
        
    return sortedDict