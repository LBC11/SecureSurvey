from django.apps import AppConfig
import threading


class ServerappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serverapp'

    def ready(self):
        # Import the function here to avoid any import issues
        from .server import start_server
        thread = threading.Thread(target=start_server)
        thread.start()
