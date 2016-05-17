"""
WSGI config for lawyerFinder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys 
import site

#site.addsitedir('/home/nelley/dev_NL/lib/python2.7/site-packages')

#activate_this = '/home/nelley/dev_NL/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lawyerFinder.settings")

#import django.core.handlers.wsgi
application = get_wsgi_application()
#application = django.core.handlers.wsgi.WSGIHandler()
