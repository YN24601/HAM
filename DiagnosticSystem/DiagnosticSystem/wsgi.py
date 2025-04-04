"""
WSGI config for DiagnosticSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 将项目根目录加入路径
# import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DiagnosticSystem.settings')

application = get_wsgi_application()
