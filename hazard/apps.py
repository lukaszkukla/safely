from django.apps import AppConfig


class HazardConfig(AppConfig):
    """
    Class sets default auto field to BigAutoField
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hazard'
