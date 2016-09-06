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
            tmpLOld = Lawyer.objects.get(user=res.user)
            tmpL = Lawyer.objects.get(user_id= res.session['_auth_user_id'])
            if tmpL and '/lawyerHome/' + tmpL.lawyerNo == res.path:
                #avoid duplication when clicking mypage button in multi-times
                return True
            else:
                return False;
        
        elif g=='STAFF':
            logger.debug('STAFF')
            return '/'
        elif g=='ORDINARYUSER':
            logger.debug('ORDINARYUSER')
            return False
        else:
            logger.debug('No matching')
            return ''
    
    return False
