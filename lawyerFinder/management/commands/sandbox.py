from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from accounts.models import User
from lawyerFinder.models import *
from django.db import models
from django.core.handlers.wsgi import logger
from types import MemberDescriptorType
from django.apps import apps
import datetime
from lawyerFinder.management.commands import * 

#python manage.py sandbox
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    def is_member(user):
        return user.groups.filter(name='Member').exists()

    
    def handle(self, *args, **options):
        logger.debug('sandbox start!')

        # get the lawyers registered in TAIPEI
        taipei = Barassociation.objects.get(area = 'TAIPEI')
        lawyers = Lawyer.objects.filter(lawyermembership__barAssociation=taipei)
        for l in lawyers:
            print 'lawyers in TAIWAN = %s' % l.lawyerId
        
        # get the lawyers registered in TAICHUNG
        taichung = Barassociation.objects.get(area = 'TAICHUNG')
        lawyerstwo = Lawyer.objects.filter(lawyermembership__barAssociation=taichung)
        for ltwo in lawyerstwo:
            print 'lawyers in TAICHUNG = %s' % ltwo.lawyerId
        
        
        #tmpu = User.objects.all()[0] # get all info from User table
        #logger.debug(tmpu.has_perm('MANAGER'))
        
        #logger.debug(tmpu.groups)
        #logger.debug(tmpu.group)
        
        #tmpu = User.objects.get(username='testLawyer@gmail.com')
        #logger.debug(tmpu.has_perm('LAWYER')) #check permission of user
        #logger.debug(tmpu.groups.filter(name='LAWYER').exists()) #check permission of user's group
        #logger.debug(tmpu.get_group_permissions())
        
        '''
        tmpu = User.objects.get(username='dragonbrucelee@gmail.com')
        g = Group.objects.get(name='MANAGER')
        g.user_set.add(tmpu)
        '''
        '''
        tmpu.first_name = 'chen'
        tmpu.save()
        '''
        
        
        
        #tmp = taipei.members.all()
        #print tmp[0].lawyer_id
        #print tmp[1].lawyer_id
        #nelley.barassociation_set.all()
        
        #m2 = Lawyer_membership.objects.create(lawyer_id=jerry, barAssociation=taipei)#, date_joined=date(1962, 8, 1))
        #m2.save()
        
        #taipei.members.all()
        #logger.debug(tmpu)
        
        # add user to a new group
        
        #tmpu = User.objects.get(username='testLawyer@gmail.com').delete()
        
        # get all user in STAFF group
        '''
        g = Group.objects.get(name='STAFF')
        users = g.user_set.all()
        logger.debug(users)
        '''
        
        logger.debug('sandbox end!')
        
        
    
        
    
    
    
    