from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.core.handlers.wsgi import logger
from accounts.models import User
from lawyerFinder.models import *
from random import randint

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
    
    def handle(self, *args, **options):
        logger.debug('db cmd start!')

        former_users = ['dragonbrucelee@gmail.com', 'formerUser@gmail.com']
        former_pw = ['123456', '123456']
        # create users
        
        u = User.objects
        # create super user
        for i, val in enumerate(former_users):
            u.create_superuser(username=val,
                               email=val,
                               password=former_pw[i])
        # create former user(lawyer)
        for i in range(1,10):
            u.create_user(username='testLawyer'+str(i)+'@gmail.com',
                          email='testLawyer'+str(i)+'@gmail.com',
                          password='123456')
        
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
        tmpG = Group.objects.get(name = 'LAWYER')
        allu = User.objects.all()
        for users in allu:
             if not users.is_admin:
                users.groups.add(tmpG)
                 
        '''
        #-------------------------------------------------------------------------------
        # relate user to lawyer
        
        #testLawyer = User.objects.get(username='testLawyer001@gmail.com')
        #l = Lawyer(userId=testLawyer, lawyerId='13-0001')
        #l.save()
        
        # relate user to lawyer & get the lawyer_id
        #print testLawyer.lawyer.lawyerId
        
        # init area info
        '''
        for a in Barassociation.AREAS:
            Barassociation.objects.create(area=a[0])


        i=0
        allu = User.objects.all()
        for user in allu:
            if not user.is_admin:
                # relate user to lawyer
                l = Lawyer(userId=user, lawyerId='13-00' + str(i))
                i += 1
                l.save()
                
                # relate lawyer to its registered area in random
                num = randint(0, randint(0, len(Barassociation.AREAS)-1))
                area = Barassociation.objects.get(area=Barassociation.AREAS[num][0])
                m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=area)
                m1.save()
        
        logger.debug('db cmd end!')
        
        '''
        taipei = Barassociation.objects.create(area='TAIPEI')
        m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taipei)
        m1.save()
        
        # relate user to lawyer
        testLawyer002 = User.objects.get(username='testLawyer002@gmail.com')
        l = Lawyer(userId=testLawyer002, lawyerId='13-0002')
        l.save()
        # relate bar association with lawyer
        m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taipei)
        m1.save()
        
        # relate user to lawyer
        test003Lawyer = User.objects.get(username='testLawyer003@gmail.com')
        l = Lawyer(userId=test003Lawyer, lawyerId='13-0003')
        l.save()
        # relate bar association with lawyer
        taichung = Barassociation.objects.create(area='TAICHUNG')
        m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taichung)
        m1.save()
        '''
