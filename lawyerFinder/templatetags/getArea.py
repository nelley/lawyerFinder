from django import template
from django.core.handlers.wsgi import logger

register = template.Library()

@register.filter(name='get_area')
def get_area(lawyerObj):
    return ",".join(bar.area_cn for bar in lawyerObj.regBarAss.all())