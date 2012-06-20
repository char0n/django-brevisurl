import string

from django.conf import settings


# Default backend used to for get_connection() fuction
DEFAULT_BACKEND = getattr(settings, 'BREVISURL_BACKEND', 'brevisurl.backends.local.BrevisUrlBackend')

# Domain that is used to create shortened urls
LOCAL_BACKEND_DOMAIN = getattr(settings, 'BREVISURL_BACKEND_LOCAL_DOMAIN', None)

# Characters that are used to generate tokens for local backend
LOCAL_BACKEND_TOKEN_CHARS = getattr(settings, 'BREVISURL_LOCAL_BACKEND_TOKEN_CHARS', list(string.ascii_letters + string.digits))