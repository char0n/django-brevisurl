import math
import random
import logging

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

import brevisurl.settings
from brevisurl import Error
from brevisurl.backends.base import BaseBrevisUrlBackend
from brevisurl.models import ShortUrl
from brevisurl.utils import absurl


log = logging.getLogger(__name__)


class TokensExhaustedError(Error):
    """Exception is raised when tokens are exhausted."""


class BrevisUrlBackend(BaseBrevisUrlBackend):

    def shorten_url(self, original_url):
        """
        :raises: ImproperlyConfigured, django.core.exceptions.ValidationError
        :raises: brevisurl.backends.local.TokensExhaustedError
        """
        try:
            short_url = ShortUrl.objects.get(backend=self.class_path, original_url=original_url)
            log.info('Url "%s" already shortened to "%s"', original_url, short_url.shortened_url)
            return short_url
        except ShortUrl.DoesNotExist:
            pass

        try:
            short_url = ShortUrl()
            if self.kwargs.get('domain') is not None:
                # Domain is present in keyword arguments supplied by constructor.
                domain = self.kwargs.get('domain')
            elif brevisurl.settings.LOCAL_BACKEND_DOMAIN is not None:
                # Domain is defined in settings.
                domain = brevisurl.settings.LOCAL_BACKEND_DOMAIN
            else:
                # Domain is taken from django site framework.
                domain = Site.objects.get_current().domain
            # Saving newly generated shortened url.
            short_url.original_url = original_url
            short_url.shortened_url = absurl(domain=domain, path=reverse('brevisurl_redirect',
                                                                         kwargs={'token': self.__generate_token()}))
            short_url.backend = self.class_path
            short_url.save()
            log.info('Url "%s" shortened to "%s"', original_url, short_url.shortened_url)
            return short_url
        except Exception:
            if self.fail_silently:
                return None
            else:
                log.exception('Unknown exception raised while shortening url "%s"', original_url)
                raise

    def __generate_token(self):
        chars = brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS
        size = brevisurl.settings.LOCAL_BACKEND_TOKEN_LENGTH
        if ShortUrl.objects.count() >= math.pow(len(chars), size):
            raise TokensExhaustedError('Consider incrementing the token length or change the char list')
        random.shuffle(chars)
        while True:
            token = ''.join([random.choice(chars) for x in range(size)])
            if not ShortUrl.objects.filter(backend=self.class_path, shortened_url__endswith=token).count():
                break
        return token