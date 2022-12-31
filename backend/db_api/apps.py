from django.apps import AppConfig


class DbApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db_api'

    def ready(self):
        from db_api.lib import scheduler
        scheduler.start()
