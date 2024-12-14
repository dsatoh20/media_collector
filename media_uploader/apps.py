from django.apps import AppConfig


class MediaUploaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_uploader'

    def ready(self):
        import media_uploader.signals  # シグナルを登録