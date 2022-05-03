import os
import dj_database_url
from .common import *

HOST_NAME = 'djangokinogo.herokuapp.com'

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = [
    HOST_NAME,
    '127.0.0.1'
]

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
