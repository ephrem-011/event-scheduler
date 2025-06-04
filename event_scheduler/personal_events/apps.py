from django.apps import AppConfig


class PersonalEventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personal_events'

    def ready(self):
        import personal_events.signal
