# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.core.handlers.wsgi import logger
from accounts.models import User
from lawyerFinder.models import *
from random import randint
from django.db import IntegrityError, transaction




#python manage.py dbcmd
#k=verbosity v=3
#k=base_url v=56
#k=days v=12
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    #def add_arguments(self, parser):
        # must input argl
        #parser.add_argument('base_url', help='Specify the base url without trailing slash.')
        # option
        #parser.add_argument('--days', default=45, help='days prior to an expiration of services.')
        
        # x necessary arg
        # -x not necessary arg
        # --x option(no input is OK)
 
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    @transaction.atomic
    def handle(self, *args, **options):
        logger.debug('db cmd start!')
        DEFAULT_INFOS = '<h4>Your Service</h4><p>Please Edit Your Service</p>'
        RANDOM_LAWYER_LIST = []
        
        try:
            with transaction.atomic():
                superUser_name = ['dragonbrucelee']
                superUser_users = ['dragonbrucelee@gmail.com']
                superUser_pw = ['123456']
                
                formerUser_name = ['formerUser']
                formerUser_users = ['formerUser@gmail.com']
                formerUser_pw = ['123456']
                
                lawyer_forTestName = ['doublenunchakus', 'Patricklin']
                lawyer_forTestEmail = ['doublenunchakus@gmail.com', 
                                       'Patricklin3@gmail.com']
                lawyer_forTestPW = ['123456', '123456']
                
                # create users
                
                u = User.objects
                # create superuser
                for i, val in enumerate(superUser_name):
                    u.create_superuser(username=superUser_users[i],
                                       first_name=superUser_name[i],
                                       email=superUser_users[i],
                                       password=superUser_pw[i])
                
                #create former user
                for i, val in enumerate(formerUser_name):
                    u.create_user(username=formerUser_users[i],
                                  first_name=formerUser_name[i],
                                  email=formerUser_users[i],
                                  password=formerUser_pw[i],
                                  active_flag = True)
                    
                # create former user(lawyers with real email)
                for i, val in enumerate(lawyer_forTestName):
                    u.create_user(username=lawyer_forTestEmail[i],
                                  first_name=lawyer_forTestName[i],
                                  email=lawyer_forTestEmail[i],
                                  password=lawyer_forTestPW[i],
                                  active_flag = True)
                
                # create former user(lawyers with sequence)
                for i in range(1,100):
                    u.create_user(username='testLawyer'+str(i)+'@gmail.com',
                                  first_name = 'testLawyer'+str(i),
                                  email='testLawyer'+str(i)+'@gmail.com',
                                  password='123456',
                                  active_flag = True)
                    RANDOM_LAWYER_LIST.append('testLawyer'+str(i)+'@gmail.com')
                    
                
                # create groups
                Group.objects.create(name = 'ORDINARYUSER')
                Group.objects.create(name = 'LAWYER')
                Group.objects.create(name = 'STAFF')
                
                g_staff = Group.objects.get(name = 'STAFF')
                Group.objects.create(name = 'WRITER', parent_id = g_staff.id)
                Group.objects.create(name = 'VIEWER', parent_id = g_staff.id)
                Group.objects.create(name = 'MANAGER', parent_id = g_staff.id)
                
                #relate membership to users
                tmpUser = User.objects.get(username='formerUser@gmail.com')
                tmpG = Group.objects.get(name = 'ORDINARYUSER')
                tmpUser.groups.add(tmpG)
                
                tmpUser = User.objects.get(username='dragonbrucelee@gmail.com')
                tmpG = Group.objects.get(name = 'STAFF')
                tmpG.user_set.add(tmpUser)
                
                # relate membership to lawyers
                new_lawyer_array = lawyer_forTestEmail + RANDOM_LAWYER_LIST
                tmpG = Group.objects.get(name = 'LAWYER')
                for i, val in enumerate(new_lawyer_array):
                    u = User.objects.get(username = val)
                    u.groups.add(tmpG)
                #allu = User.objects.all()
                #for users in allu:
                #     if not users.is_admin:
                #        users.groups.add(tmpG)
                
                # init area info
                for a in Barassociation.AREAS:
                    Barassociation.objects.create(area=a[0], area_cn=a[1])
                    
                # init field info
                for sf in LitigationType.CATEGORYS:
                    LitigationType.objects.create(category=sf[0], category_cn=sf[1])
        
                i=0
                #allu = User.objects.all()
                #for user in allu:
                #    if not user.is_admin:
                for i, val in enumerate(new_lawyer_array):
                    # relate user to lawyerl
                    u = User.objects.get(username = val)
                    g = Lawyer.GENDER[randint(0,1)][0]
                    grade = Lawyer.PREMIUM[randint(0,3)][0]
                    cy = randint(0,20)
                    l = Lawyer(user=u, lawyerNo='1300' + str(i), 
                               gender=g, premiumType=grade, careerYear=cy)
                    i += 1
                    l.save()
                    
                    # add default data to lawyer_info table
                    l_infos =Lawyer_infos(lawyer_id=l.user_id,
                                         basic=DEFAULT_INFOS,
                                         strongFields=DEFAULT_INFOS,
                                         finishedCases=DEFAULT_INFOS,
                                         feeStd=DEFAULT_INFOS,
                                         companyInfos=DEFAULT_INFOS)
                    l_infos.save()
                    
                    # relate lawyer to its registered area in random
                    to = len(Barassociation.AREAS)-1
                    tmpArea = (Barassociation.AREAS[randint(0,to)][0] for r in xrange(5))
                    # duplicate removal
                    area_selected = list(set(tmpArea))
                    areas = Barassociation.objects.filter(area__in = area_selected)
                    LawyerMembership.objects.create_in_bulk(l, areas)
                    
                    # relate lawyer to its strong field
                    toto = len(LitigationType.CATEGORYS)-1
                    tmpField = (LitigationType.CATEGORYS[randint(0,toto)][0] for r in xrange(5))
                    # duplicate removal
                    field_selected = list(set(tmpField))
                    fields = LitigationType.objects.filter(category__in = field_selected)
                    LawyerSpecialty.objects.create_in_bulk(l, fields)
                        
                tContent = 'test'
                tKey = 'SERVICE_RULE'
                ws = WebStaticContents(key= tKey, contents=tContent)
                ws.save()
                        
                logger.debug('db cmd end!')
                
                '''
                # relate user to lawyer
                test003Lawyer = User.objects.get(username='testLawyer003@gmail.com')
                l = Lawyer(userId=test003Lawyer, lawyerId='13-0003')
                l.save()
                # relate bar association with lawyer
                taichung = Barassociation.objects.create(area='TAICHUNG')
                m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taichung)
                m1.save()
                '''
        except IntegrityError:
            handle_exception()
