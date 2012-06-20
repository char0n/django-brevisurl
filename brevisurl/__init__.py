import traceback
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import brevisurl.settings
from brevisurl.utils import load_object


def get_connection(backend=None, fail_silently=False, **kwargs):
    """Load a brevisurl backend and return an instance of it.

    If backend is None (default) settings.BREVISURL_BACKEND is used.
    Both fail_silently and other keyword arguments are used in the
    constructor of the backend.

    :param backend: path to brevisurl backend
    :type backend: string
    :param fail_silently: whether to fail silently when error intercepted or not
    :type fail_silently: bool
    :returns: instance os BaseBrevisUrlBackend
    :rtype: brevisurl.backends.base.BaseBrevisUrlBackend

    """
    path = backend or brevisurl.settings.DEFAULT_BACKEND
    klass = load_object(path)
    return klass(fail_silently=fail_silently, **kwargs)


def shorten_url(original_url, fail_silently=False, connection=None):
    """Shortcut util for shortening urls using default brevisurl backend if none supplied.

    :param original_url: url that will be shortened
    :type original_url: string
    :param backend: one of brevisurl backends
    :type backend: brevisurl.backends.BaseBrevisUrlBackend
    :returns: shortened url from original url
    :rtype: brevisurl.models.ShortUrl

    """
    connection = connection or get_connection(fail_silently=fail_silently)
    return connection.shorten_url(original_url)


class Error(Exception):
    """Base django-brevisurl Error."""

    def __init__(self, value):
        s = StringIO()
        traceback.print_exc(file=s)
        self.value = (value, s.getvalue())
        s.close()

    def __str__(self):
        return repr(self.value)