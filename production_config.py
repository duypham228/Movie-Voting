"""Production config for movie voting on Heroku."""

import os
from .config import *

DEBUG = False
SECRET_KEY = 'production key'  # keep secret 
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
# CELERY_BROKER = os.getenv('RABBIT_BIGWIG_RX_URL')