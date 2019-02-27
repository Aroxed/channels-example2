import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notifier.settings")
django.setup()
application =git -v get_default_application()