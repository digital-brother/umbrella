""" This file is used to include any application configuration for the app."""
from django.apps import AppConfig


class UmbrellaConfig(AppConfig):
    """This class is representing umbrella application and its configuration."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "umbrella"
