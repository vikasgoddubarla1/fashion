"""
WSGI config for akhila project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akhila.settings')

# --- BEGIN: Auto-run migrate and createsuperuser ---
django.setup()
from users.models import User
from django.core.management import call_command

# Run migrations
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print("Migration Error:", e)

# Create superuser only if not exists
# User = get_user_model()
if not User.objects.filter(email='admin@gmail.com').exists():
    User.objects.create('admin@example.com', 'adminpassword', 'is_admin=True')
# --- END: Auto-run ---


application = get_wsgi_application()
