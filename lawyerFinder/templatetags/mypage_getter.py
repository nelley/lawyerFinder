from django import template
from django.core.handlers.wsgi import logger
from lawyerFinder.models import *
from lawyerFinder.settings import SITE_URL

register = template.Library()

@register.filter(name='mypage_getter')
def mypage_getter(userObj):
    logger.debug('mypage_getter')
    #print userObj
    g = userObj.groups.all()[0].name

    if g=='LAWYER':
        tmpL = Lawyer.objects.get(user=userObj)
        if tmpL:
            #print tmpL.lawyerNo
            #avoid duplication when clicking mypage button in multi-times
            return SITE_URL + 'lawyerHome/'+tmpL.lawyerNo
    
    elif g=='STAFF':
        logger.debug('STAFF')
        return '/'
    elif g=='ORDINARYUSER':
        logger.debug('ORDINARYUSER')
        return '/'
    else:
        logger.debug('No matching')
        return ''