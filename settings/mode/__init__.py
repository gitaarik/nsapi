import os


MODE = None

try:
    from settings import local
except ImportError:
    pass
else:
    if 'MODE' in local:
        MODE = local.MODE

if not MODE:
    MODE = 'development'

if MODE == 'development':
    from .development import *
elif MODE == 'production':
    from .production import *
