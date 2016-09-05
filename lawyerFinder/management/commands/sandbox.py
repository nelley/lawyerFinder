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
import re

#python manage.py sandbox
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    def is_member(user):
        return user.groups.filter(name='Member').exists()

    
    def handle(self, *args, **options):
        sep = '========================================================================='
        logger.debug('sandbox start!')
        
        print sep
        
        # calculate std
        i = 0
        print 'row\tarea\tfield\tgender\ttype\ttotal'
        for a in xrange(1, 4): #area
            for f in xrange(1, 4): #field
                for g in xrange(0, 2): #gender
                    for t in xrange(1, 5): #type
                        print '%s\t%s\t%s\t%s\t%s\t%s' % (i,a,f,g,t, a*10000+f*1000+g*100000+t*100)
                        i += 1
        
        
        # logic of the user query
        str = '(testLawyer4) (4) (M) (GOLDEN) (13-003) (KEELUNG, TAIPEI, HSINCHU, YUNLIN, HUALIEN) (PC:96, BC:71, SA:100, LA:18)'
        userInput = []
        userInput.append('YILAN|KEELUNG|TAINAN')
        userInput.append('PC|BC|HI')

        pattern = re.compile(userInput[1])
        match = pattern.findall(str)
        print len(match) 
        print sep
        
        u = User.objects.get(username= 'doublenunchakus@gmail.com')
        print u.id
        print u.delete()
        
        #SomeModel.objects.filter(id=id).delete()
        
        #print ",".join('\"'+bar.area+'\"' for bar in l.regBarAss.all()),
        
        
        #print ",".join('\"'+bar.area_cn+'\"' for bar in l.regBarAss.all()),
        #print ",".join('\"'+spec.category_cn+'\"' for spec in l.specialty.all()),
        
        
        
        logger.debug('sandbox end!')
        