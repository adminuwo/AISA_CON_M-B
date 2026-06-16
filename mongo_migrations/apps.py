"""
Custom AppConfig overrides for Django built-in apps.
These override default_auto_field to use MongoDB's ObjectIdAutoField
instead of the default AutoField which MongoDB doesn't support.
"""
from django.contrib.auth.apps import AuthConfig
from django.contrib.contenttypes.apps import ContentTypesConfig


class MongoAuthConfig(AuthConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'


class MongoContentTypesConfig(ContentTypesConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'


from django.contrib.sessions.apps import SessionsConfig

class MongoSessionsConfig(SessionsConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
