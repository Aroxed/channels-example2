import redis
from django.apps import AppConfig


class NotifierConfig(AppConfig):
    name = 'notifier'

    def ready(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.delete("users")

        from . import signals
