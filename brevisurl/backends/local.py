import string
import random
import logging

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

import brevisurl.settings
from brevisurl.backends.base import BaseBrevisUrlBackend
from brevisurl.models import ShortUrl


log = logging.getLogger(__name__)


class BrevisUrlBackend(BaseBrevisUrlBackend):

    PROTOCOL = 'http'

    def shorten_url(self, original_url):
        """
        :raises: ImproperlyConfigured, django.core.exceptions.ValidationError
        """
        try:
            short_url = ShortUrl.objects.get(backend=self.class_path, original_url=original_url)
            log.info('Url "%s" already shortened to "%s"', original_url, short_url.shortened_url)
            return short_url
        except ShortUrl.DoesNotExist:
            pass

        try:
            short_url = ShortUrl()
            if brevisurl.settings.LOCAL_BACKEND_DOMAIN is not None:
                short_url.shortened_url = '{0}{1}'.format(brevisurl.settings.LOCAL_BACKEND_DOMAIN.rstrip('/'),
                                                          reverse('brevisurl_redirect',
                                                                  kwargs={'token': self.__generate_token()}))
            else:
                current_site = Site.objects.get_current()
                short_url.shortened_url = '{0}://{1}{2}'.format(self.PROTOCOL, current_site.domain,
                                                                reverse('brevisurl_redirect',
                                                                        kwargs={'token': self.__generate_token()}))
            short_url.original_url = original_url
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

    def __generate_token(self, size=5):
        chars = list(string.ascii_letters + string.digits)
        random.shuffle(chars)
        while True:
            token = ''.join([random.choice(chars) for x in range(size)])
            if not ShortUrl.objects.filter(backend=self.class_path, shortened_url__endswith=token).count():
                break
        return token