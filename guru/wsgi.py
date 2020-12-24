"""
WSGI config for guru project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import os
# from whitenoise import WhiteNoise
import guru
from django.core.wsgi import get_wsgi_application

# application = WhiteNoise(guru, root='static')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guru.settings')

application = get_wsgi_application()
