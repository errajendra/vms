from django.apps import AppConfig


class VmsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vms_app'
    
    def ready(self) -> None:
        import vms_app.signals
