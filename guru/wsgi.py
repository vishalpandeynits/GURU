import os
import guru
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guru.settings')

application = get_wsgi_application()