import configparser

from .base import *
from .cipher import decrypt


current_dir = os.path.abspath(os.path.dirname(__file__))
cf = configparser.ConfigParser()
cf.read(os.path.join(current_dir, 'django_db.conf'))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': cf.get('db', 'PG_NAME'),
        'USER': cf.get('db', 'PG_USER'),
        'PASSWORD': decrypt(cf.get('db', 'PG_PASSWORD')),
        'HOST': cf.get('db', 'PG_HOST'),
        'PORT': cf.get('db', 'PG_PORT'),
        'OPTIONS': {
            'options': '-c search_path=public'
        }
    }
}
