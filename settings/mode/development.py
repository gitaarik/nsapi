from django.views.decorators.cache import never_cache


DEBUG = True
TEMPLATE_DEBUG = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
CACHE_FUNC = lambda seconds: never_cache
