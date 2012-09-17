import urlparse

from django.utils import importlib
from django.contrib.sites.models import Site

import brevisurl.settings


def load_object(import_path):
    """Util for importing objects from import path.

    :param import_path: import path of object to be imported e.g. module.submodule.Class
    :type import_path: string
    :returns: imported object
    :rtype: object
    :raises: ValueError, ImportError, AttributeError

    """
    if not (isinstance(import_path, basestring) and '.' in import_path):
        raise ValueError('There must be at least one dot in import path: "%s"', import_path)
    module_name, object_name = import_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, object_name)


def url_has_protocol(url):
    """Util for determining whether url has protocol present or not.

    :param url: url that is being examined.
    :type url: string
    :returns: True if url has protocol, False otherwise
    :rtype: bool

    """
    url_parsed = urlparse.urlparse(url)
    return True if url_parsed.netloc != '' and url_parsed.scheme in ('http', 'https') else False


def url_has_path(url):
    """Util for determining whether url has path present or not.

    :param url: url that is being examined.
    :type url: string
    :returns: True if url has path, False otherwise
    :rtype: bool

    """
    url_parsed = urlparse.urlparse(url)
    return True if url_parsed.netloc != '' and url_parsed.path != '' else False



def absurl(protocol=None, domain=None, site=None, path='/'):
    """Util for constructing absolute urls from relative urls.

    Keyword argument domain has higher priority over site. If site not set
    domain is used. If both are not set, current site is used.

    :param protocol: domain protocol
    :type protocol: string
    :param domain: URI domain
    :type domain: string
    :param site: Site instance
    :type site: django.contrib.sites.models.Site
    :param path: URI path
    :type path: string
    :returns: absolute URI
    :rtype: string

    """
    # Searching for domain.
    protocol = protocol or brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL
    if domain is None and site is None:
        domain = Site.objects.get_current().domain
    elif domain is None and site is not None:
        domain = site.domain
    # Append protocol if not present.
    if not url_has_protocol(domain):
        domain = '{protocol:s}://{domain:s}'.format(protocol=protocol, domain=domain)
    # Always append default path if not present in domain.
    if not url_has_path(domain):
        domain = '{domain:s}/'.format(domain=domain)
    # Concatenate domain with protocol and path.
    return '{domain:s}{path:s}'.format(domain=domain, path=path.lstrip('/'))