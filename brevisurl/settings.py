import string

from django.conf import settings


# Default backend used to for get_connection() function.
DEFAULT_BACKEND = getattr(settings, 'BREVISURL_BACKEND', 'brevisurl.backends.local.BrevisUrlBackend')

# Domain that is used to create shortened urls.
LOCAL_BACKEND_DOMAIN = getattr(settings, 'BREVISURL_BACKEND_LOCAL_DOMAIN', None) or getattr(settings, 'BREVISURL_LOCAL_BACKEND_DOMAIN', None)

# Characters that are used to generate tokens for local backend.
LOCAL_BACKEND_TOKEN_CHARS = getattr(settings, 'BREVISURL_LOCAL_BACKEND_TOKEN_CHARS', list(string.ascii_letters + string.digits))

# Settings for token length.
LOCAL_BACKEND_TOKEN_LENGTH = getattr(settings, 'BREVISURL_LOCAL_BACKEND_TOKEN_LENGTH', 5)

# Settings for url pattern.
LOCAL_BACKEND_URL_PATTERN = getattr(settings, 'BREVISURL_LOCAL_BACKEND_URL_PATTERN',
                                    r'^(?P<token>[a-zA-Z0-9]{' + str(LOCAL_BACKEND_TOKEN_LENGTH) + r'})$')
# Protocol for local backend.
LOCAL_BACKEND_DOMAIN_PROTOCOL = getattr(settings, 'BREVISURL_LOCAL_BACKEND_DOMAIN_PROTOCOL', 'http')