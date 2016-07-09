from django import template
from django.core.handlers.wsgi import logger
from lawyerFinder.models import *

register = template.Library()

@register.filter(name='is_mypage')
def is_mypage(res):
    logger.debug('is_mypage')
    
    # check logged in or not
    if res.user.is_authenticated():
        g = res.user.groups.all()[0].name
        
        if g=='LAWYER':
            tmpL = Lawyer.objects.get(user=res.user)
            if tmpL and tmpL.lawyerNo == res.path.split('/')[2]:
                #avoid duplication when clicking mypage button in multi-times
                return True
            else:
                return False;
        
        elif g=='STAFF':
            logger.debug('STAFF')
            return '/'
        elif g=='ORDINARYUSER':
            logger.debug('ORDINARYUSER')
            return '/'
        else:
            logger.debug('No matching')
            return ''
    
    return False
