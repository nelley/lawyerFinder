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
from django.core import serializers
import json
import re
import operator

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
        '''
        allLawyer = Lawyer.objects.all()
        for l in allLawyer:
            print l
        print sep
        '''
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
        
        SCORE = { 'area':10000,
                  'caseNum':1000,
                  'gender':100000,
                  'premiumType':100,
                 }
        start = datetime.datetime.now()
        
        area_selected = ['YILAN', 'KEELUNG', 'TAINAN']
        areas = Barassociation.objects.filter(area__in = area_selected)
        
        field_selected = ['PC', 'BC', 'BD']
        
        print 'area keys = %s, field keys = %s '% (area_selected, field_selected)
        
        fields = LitigationType.objects.filter(category__in=field_selected)
        
        lawyers = Lawyer.objects.select_related('user').filter(
                              models.Q(lawyermembership__barAssociation=areas) & 
                              models.Q(lawyerspecialty__litigations=fields)).distinct()

        results = []
        #-- generate regex
        areaInput = '('+ "|".join(a for a in area_selected) +')'
        fieldInput = '(\"+[' + "|".join(f for f in field_selected) + ']+\":\"\d+\")'
        genderInput = '\"F\"'
        for l in lawyers:
            #-- parse json to dict 
            d = json.loads(str(l))
            #print d['caseNum']['BC']
            
            #-- area regex match for replacing the hit rate 
            pattern = re.compile(areaInput)
            match = pattern.findall(str(l))
            logger.debug('area hitted:%s' % len(match))
            d['area'] = len(match)
            
            #--field regex match for replacing the hit rate 
            pattern = re.compile(fieldInput)
            match = pattern.findall(str(l))
            logger.debug('field hitted:%s' % len(match))
            d['caseNum']=len(match)
            
            #--gender regex match for replacing the value of hitted or not
            pattern = re.compile(genderInput)
            match = pattern.findall(str(l))
            logger.debug('gender hitted:%s' % len(match))
            d['gender']=len(match)
            
            #--calculate total score for ranking
            
            d['rank'] = d['area']*SCORE['area'] + d['caseNum']*SCORE['caseNum'] + d['gender']*SCORE['gender'] + int(d['premiumType'])*SCORE['premiumType']
            # add to the list
            results.append(d)

        #--sort
        newlist = sorted(results, key=operator.itemgetter('rank'), reverse=True)
        
        #--display
        for i, val in enumerate(newlist):
            print 'i=%s, val=%s' % (i,val)
            
        end = datetime.datetime.now()
        timeDelta = end-start
        print timeDelta
        
        
        
        
        print sep
        logger.info('query End!')