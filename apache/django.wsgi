import os
import sys

sys.path.append('/srv/www/cloudstacktesting/')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/cloudstacktesting/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudstacktesting.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

