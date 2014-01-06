import os


MODE = os.environ.get('NSAPI_MODE', 'development')

if MODE == 'development':
    from .development import *
elif MODE == 'production':
    from .production import *
