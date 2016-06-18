from django import template
from django.utils.translation import ugettext_lazy as _
from django.core.handlers.wsgi import logger
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='which_group')
def which_group(u, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in u.groups.all() else False