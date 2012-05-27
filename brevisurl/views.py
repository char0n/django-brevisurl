import logging

from django.http import Http404
from django.contrib.sites.models import Site
from django.views.generic.base import RedirectView
from django.core.exceptions import ImproperlyConfigured

from brevisurl import get_connection
from brevisurl.models import ShortUrl


log = logging.getLogger(__name__)


class BrevisUrlRedirectView(RedirectView):

    def get_redirect_url(self, **kwargs):
        try:
            token = kwargs.pop('token')
        except KeyError:
            log.exception('Token not found in keyword arguments')
            raise Http404
        connection = get_connection('brevisurl.backends.local.BrevisUrlBackend')
        protocol = connection.PROTOCOL
        try:
            site = Site.objects.get_current()
        except ImproperlyConfigured:
            log.exception('No site object configured for this django project')
            raise Http404
        try:
            short_url = '{0}://{1}/{2}'.format(protocol, site.domain, token)
            short_url_obj = ShortUrl.objects.get(backend=connection.class_path, shortened_url=short_url)
        except ShortUrl.DoesNotExist:
            log.exception('No shortened url found for backend: "%s" and token: "%s"', connection.class_path, token)
            raise Http404
        return short_url_obj.original_url