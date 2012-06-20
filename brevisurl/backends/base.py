from abc import ABCMeta


class BaseBrevisUrlBackend(object):
    """Base class for brevisurl backend implementations. Subclasses must at least overwrite shorten_url()."""

    __metaclass__ = ABCMeta


    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently
        self.class_path = '{0}.{1}'.format(self.__module__, self.__class__.__name__)
        self.kwargs = kwargs

    def open(self):
        """Open a network connection.

        This method can be overwritten by backend implementations to
        open a network connection.

        It's up to the backend implementation to track the status of
        a network connection if it's needed by the backend.

        The default implementation does nothing.

        """
        pass

    def close(self):
        """Close a network connection."""
        pass

    def shorten_url(self, original_url):
        """Shortens url into more compact form.

        :param original_url: url that will be shortened
        :type original_url: string
        :returns: shortened url from original url
        :rtype: brevisurl.models.ShortUrl

        """
        raise NotImplementedError