from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.handlers.wsgi import logger
from types import MemberDescriptorType
from django.apps import apps


#python manage.py [filename.py]
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    def handle(self, *args, **options):
        logger.debug('permission start!')
        
        # 
        content_type = ContentType.objects.get(app_label='accounts',
                                               model='user')

        #
        Permission.objects.create(content_type_id=content_type.id, 
                                  name='Can view logged in page', 
                                  codename='can_view')
        
        
        logger.debug('permission end!')
        
        
        
        