from django.views.decorators.cache import cache_page


DEBUG = False
TEMPLATE_DEBUG = False
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
CACHE_FUNC = cache_page
