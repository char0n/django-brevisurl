import urlparse

from django import template
from django.template.defaulttags import URLNode, url
from django.contrib.sites.models import Site

from brevisurl import shorten_url as shorten_url_util, get_connection


register = template.Library()


@register.filter
def shorten_url(original_url):
    short_url = shorten_url_util(original_url, connection=get_connection(fail_silently=True))
    return short_url.shortened_url if short_url is not None else original_url


# Modified copy of django snippet #1518 (http://djangosnippets.org/snippets/1518/)
class AbsoluteURLNode(URLNode):
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        domain = 'http://{domain:s}'.format(domain=Site.objects.get_current().domain)
        if self.asvar:
            context[self.asvar]= urlparse.urljoin(domain, context[self.asvar])
            return ''
        else:
            return urlparse.urljoin(domain, path)

def absurl(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but ads the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar)
absurl = register.tag(absurl)