from django.apps import AppConfig


class BlogsConfig(AppConfig):
    """
    Configuration class for the blogs app.
    Defines app-specific settings and metadata.
    """

    # Specifies the default auto field type for primary keys
    default_auto_field = "django.db.models.BigAutoField"

    # Defines the name of the application
    name = "blogs"
