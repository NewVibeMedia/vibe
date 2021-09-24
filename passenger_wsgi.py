import sys
import os

PROJECT_ROOT = os.path.dirname(__file__)

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'vibe'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'post'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'mode'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'vibe.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()