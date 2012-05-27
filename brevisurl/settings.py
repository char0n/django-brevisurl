from django.conf import settings

DEFAULT_BACKEND = getattr(settings, 'BREVISURL_BACKEND', 'brevisurl.backends.local.BrevisUrlBackend')