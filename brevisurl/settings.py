from django.conf import settings

DEFAULT_BACKEND = getattr(settings, 'BREVISURL_BACKEND', 'brevisurl.backends.local.BrevisUrlBackend')
LOCAL_BACKEND_DOMAIN = getattr(settings, 'BREVISURL_BACKEND_LOCAL_DOMAIN', None)