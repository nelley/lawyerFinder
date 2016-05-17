from django.core.management.base import BaseCommand, CommandError
from django.core.handlers.wsgi import logger

#python manage.py customCmdTest -v 3 56 --days 12
#k=verbosity v=3
#k=base_url v=56
#k=days v=12
class Command(BaseCommand):
    args = ''
    help = 'help cmd test'
    
    def add_arguments(self, parser):
        # must input arg
        parser.add_argument('base_url', help='Specify the base url without trailing slash.')
        # option
        parser.add_argument('--days', default=45, help='days prior to an expiration of services.')
        
        # x necessary arg
        # -x not necessary arg
        # --x option(no input is OK)
 
    
    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
    
    def handle(self, *args, **options):
        logger.debug('custom cmd succeed!')
        '''
        for target_id in options['base_url']:
            logger.debug('target_id: %s' % target_id)
        ''' 
        # loop the key & value in dict
        for k, v in options.items():
            logger.debug('k=%s v=%s' % (k, v))
            