from django.apps import AppConfig


class NtUserConfig(AppConfig):
    name = 'nt_user'

    def ready(self):
        import nt_user.signals
