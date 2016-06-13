from django import template
from django.core.handlers.wsgi import logger
from lawyerFinder.models import LitigationType

register = template.Library()

@register.filter(name='get_field')
def get_field(lawyerObj):
    matchField = LitigationType.objects.all()
    return ",".join((field.litigations.category_cn + ':' + str(field.caseNum))
                                                for field in lawyerObj.lawyerspecialty_set.filter(litigations=matchField))