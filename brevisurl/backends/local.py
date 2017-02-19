import math
import random
import logging

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction

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

        if self.kwargs.get('domain') is not None:
            # Domain is present in keyword arguments supplied by constructor.
            domain = self.kwargs.get('domain')
        elif brevisurl.settings.LOCAL_BACKEND_DOMAIN is not None:
            # Domain is defined in settings.
            domain = brevisurl.settings.LOCAL_BACKEND_DOMAIN
        else:
            # Domain is taken from django site framework.
            domain = Site.objects.get_current().domain

        try:
            shortened_url = self.__generate_shortened_url(domain)
            try:
                short_url, created = ShortUrl.objects.get_or_create(backend=self.class_path,
                                                                    original_url=original_url,
                                                                    original_url_hash=ShortUrl.url_hash(original_url),
                                                                    defaults={'shortened_url': shortened_url})
                if created:
                     log.info('Url "%s" shortened to "%s"', original_url, shortened_url)
                else:
                     log.info('Url "%s" already shortened to "%s"', original_url, short_url.shortened_url)
                return short_url
            except (IntegrityError, ValidationError) as e:
                # Check if the error is an URL validation error.
                if isinstance(e, ValidationError) and e.message_dict.has_key('original_url'):
                    raise

                # Generate another token.
                self.__check_tokens_exhausted()
                while True:
                    shortened_url = self.__generate_shortened_url(domain)
                    sid = transaction.savepoint()
                    try:
                        short_url = ShortUrl.objects.create(backend=self.class_path,
                                                            original_url=original_url,
                                                            shortened_url=shortened_url)
                        log.info('Url "%s" shortened to "%s"', original_url, shortened_url)
                        transaction.savepoint_commit(sid)
                        return short_url
                    except (IntegrityError, ValidationError) as e:
                        transaction.savepoint_rollback(sid)
                        self.__check_tokens_exhausted()
        except Exception:
            if self.fail_silently:
                return None
            else:
                log.exception('Unknown exception raised while shortening url "%s"', original_url)
                raise

    def __check_tokens_exhausted(self):
        chars = brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS
        size = brevisurl.settings.LOCAL_BACKEND_TOKEN_LENGTH
        if ShortUrl.objects.count() >= math.pow(len(chars), size):
            raise TokensExhaustedError('Consider incrementing the token length or change the char list')

    def __generate_shortened_url(self, domain):
        chars = brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS
        size = brevisurl.settings.LOCAL_BACKEND_TOKEN_LENGTH
        random.shuffle(chars)
        token = ''.join([random.choice(chars) for x in range(size)])
        shortened_url = absurl(domain=domain,
                               path=reverse('brevisurl_redirect',
                                            kwargs={'token': token}))
        return shortened_url
