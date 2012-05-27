import string
import random
import logging

from django.contrib.sites.models import Site

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
            current_site = Site.objects.get_current()
            short_url = ShortUrl()
            short_url.original_url = original_url
            short_url.shortened_url = '{0}://{1}/{2}'.format(self.PROTOCOL, current_site.domain,
                                                             self.__generate_token())
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