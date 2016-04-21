from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.core.handlers.wsgi import logger
from accounts.models import User

#python manage.py dbcmd
#k=verbosity v=3
#k=base_url v=56
#k=days v=12
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    #def add_arguments(self, parser):
        # must input arg
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
        
        # create users
        User.objects.create_superuser(username='dragonbrucelee@gmail.com', 
                                      email='dragonbrucelee@gmail.com', 
                                      password='123456')
        
        User.objects.create_superuser(username='test001@gmail.com', 
                                      email='test001@gmail.com', 
                                      password='123456')
        
        User.objects.create_superuser(username='testLawyer@gmail.com', 
                                      email='testLawyer@gmail.com', 
                                      password='123456')
        
        # create groups
        Group.objects.create(name = 'ORDINARYUSER')
        Group.objects.create(name = 'LAWYER')
        Group.objects.create(name = 'STAFF')
        Group.objects.create(name = 'WRITER', parent_id = 3)
        Group.objects.create(name = 'VIEWER', parent_id = 3)
        Group.objects.create(name = 'MANAGER', parent_id = 3)
        
        #create membership from Group
        tmpUser = User.objects.get(username='dragonbrucelee@gmail.com')
        tmpG = Group.objects.get(name = 'STAFF')
        tmpG.user_set.add(tmpUser)
        
        #create membership from User
        tmpUser = User.objects.get(username='test001@gmail.com')
        tmpG = Group.objects.get(name = 'STAFF')
        tmpUser.groups.add(tmpG)
        
        #create membership from Group
        tmpUser = User.objects.get(username='testLawyer@gmail.com')
        tmpG = Group.objects.get(name = 'LAWYER')
        tmpG.user_set.add(tmpUser)
        
        
        #-------------------------------------------------------------------------------
        # relate user to lawyer
        testLawyer = User.objects.get(username='testLawyer@gmail.com')
        l = Lawyer(userId=testLawyer, lawyerId='13-0001')
        l.save()
        
        # relate user to lawyer & get the lawyer_id
        print testLawyer.lawyer.lawyerId
        
        # relate bar association with lawyer
        taipei = Barassociation.objects.create(area='TAIPEI')
        m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taipei)
        m1.save()
        
        # relate user to lawyer
        dragonLawyer = User.objects.get(username='dragonbrucelee@gmail.com')
        l = Lawyer(userId=dragonLawyer, lawyerId='13-0002')
        l.save()
        # relate bar association with lawyer
        m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taipei)
        m1.save()
        
        
        # relate user to lawyer
        test001Lawyer = User.objects.get(username='test001@gmail.com')
        l = Lawyer(userId=test001Lawyer, lawyerId='13-0003')
        l.save()
        # relate bar association with lawyer
        taichung = Barassociation.objects.create(area='TAICHUNG')
        m1 = LawyerMembership.objects.create(lawyerId=l, barAssociation=taichung)
        m1.save()
        
        
        logger.debug('db cmd end!')