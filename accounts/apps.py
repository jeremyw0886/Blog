from django.apps import AppConfig


def ready(self):
    import accounts.signals

class AccountsConfig(AppConfig):
    """
    Configuration class for the accounts app.
    Defines app-specific settings and metadata.
    """

    # Specifies the default auto field type for primary keys
    default_auto_field = "django.db.models.BigAutoField"

    # Defines the name of the application
    name = "accounts"
