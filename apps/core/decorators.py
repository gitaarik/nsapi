from django.conf import settings


def cache_page(seconds):
    return settings.CACHE_FUNC(seconds)
