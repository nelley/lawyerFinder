from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from accounts.models import (User, Membership)
from django.db import models
from django.core.handlers.wsgi import logger
from types import MemberDescriptorType
from django.apps import apps

#python manage.py sandbox
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    def handle(self, *args, **options):
        logger.debug('sandbox start!')
        
        tmpu = User.objects.all()[0] # get all info from User table
        #logger.debug(tmpu.has_perm('MANAGER'))
        
        #logger.debug(tmpu.groups)
        #logger.debug(tmpu.group)
        
        
        #
        #tmpu = User.objects.get(username='dragonbrucelee@gmail.com')
        #tmpu = User.objects.filter(membership__group='3')
        #g = Group.objects.get(name='MANAGER')
        #logger.debug(g)
        #tmpu.group.add(g)
        '''
        tmpu.first_name = 'chen'
        tmpu.save()
        '''
        
        #logger.debug(tmpu)
        
        # add user to a new group
        
        g = Group.objects.get(name='lawyer') 
        g.user_set.add(tmpu)
        
        logger.debug('sandbox end!')
        
        
        
        