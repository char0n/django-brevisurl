import logging

from django.http import Http404
from django.contrib.sites.models import Site
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

import brevisurl.settings
from brevisurl import get_connection
from brevisurl.models import ShortUrl
from brevisurl.utils import absurl


log = logging.getLogger(__name__)


class BrevisUrlRedirectView(RedirectView):

    def get_redirect_url(self, **kwargs):
        # No token present
        try:
            token = kwargs.pop('token')
        except KeyError:
            log.exception('Token not found in keyword arguments')
            raise Http404

        connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
        short_url_obj = None

        # Seeking domain in settings.
        if brevisurl.settings.LOCAL_BACKEND_DOMAIN is not None:
            domain = brevisurl.settings.LOCAL_BACKEND_DOMAIN.rstrip('/')
            short_url = absurl(domain=domain, path=reverse('brevisurl_redirect', kwargs={'token': token}))
            try:
                short_url_obj = ShortUrl.objects.get(backend=connection.class_path, shortened_url=short_url)
            except ShortUrl.DoesNotExist:
                pass

        # Seeking domain in django site framework and current site.
        if short_url_obj is None:
            try:
                site = Site.objects.get_current()
                short_url = absurl(site=site, path=reverse('brevisurl_redirect', kwargs={'token': token}))
                short_url_obj = ShortUrl.objects.get(backend=connection.class_path, shortened_url=short_url)
            except ImproperlyConfigured:
                log.exception('No site object configured for this django project')
            except ShortUrl.DoesNotExist:
                pass

        # Seeking domain from current request.
        if short_url_obj is None:
            try:
                short_url = absurl(domain=self.request.get_host(), path=reverse('brevisurl_redirect', kwargs={'token': token}))
                short_url_obj = ShortUrl.objects.get(backend=connection.class_path, shortened_url=short_url)
            except ShortUrl.DoesNotExist:
                log.exception('No shortened url found for backend: "%s" and token: "%s"', connection.class_path, token)
                raise Http404

        return short_url_obj.original_url