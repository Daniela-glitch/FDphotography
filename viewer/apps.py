from django.apps import AppConfig

class ViewerConfig(AppConfig):
    name = 'viewer'

    def ready(self):
        import viewer.signals
