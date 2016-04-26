# -*- coding: utf-8 -*-
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
from random import randint
from __builtin__ import list


#python manage.py querys
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    def is_member(user):
        return user.groups.filter(name='Member').exists()

    
    def handle(self, *args, **options):
        sep = '========================================================================='
        logger.info('query Start!')
        
        # list up all lawyers with 
        #first_name, gender, premiumType, lawyerNo, registered area, strong fields
        allLawyer = Lawyer.objects.all()
        for l in allLawyer:
            print l

        print sep
        # get the lawyers that registered in TAITUNG
        '''
        #select_related is limited to single-valued relationships - foreign key & one-to-one
        #prefetch_related : does a separate lookup for each relationship, and does the ‘joining’ in Python.
        #This allows it to prefetch many-to-many and many-to-one objects
        area_selected = ['YILAN', 'PINGTUNG']
        areas = Barassociation.objects.filter(area__in = area_selected)
        lawyers = Lawyer.objects.select_related('user').filter(lawyermembership__barAssociation=areas).distinct()
        for l in lawyers:
            print l
        
        
        print sep
        
        field_selected = ['PC', 'PE']
        fields = LitigationType.objects.filter(category__in=field_selected)
        lawyers = Lawyer.objects.all().filter(lawyerspecialty__litigations=fields).distinct()
        #.order_by('specialty')
        for l in lawyers:
            print l
        '''
        print sep
        area_selected = ['YILAN', 'PINGTUNG', 'TAINAN']
        areas = Barassociation.objects.filter(area__in = area_selected)
        
        field_selected = ['PC', 'EC']
        fields = LitigationType.objects.filter(category__in=field_selected)
        
        lawyers = Lawyer.objects.select_related('user').filter(
                              models.Q(lawyermembership__barAssociation=areas) & 
                              models.Q(lawyerspecialty__litigations=fields)).distinct()
        for l in lawyers:
            print l
        
        
        logger.info('query End!')