from django import template

from brevisurl import shorten_url as shorten_url_util, get_connection

register = template.Library()


@register.filter
def shorten_url(original_url):
    short_url = shorten_url_util(original_url, connection=get_connection(fail_silently=True))
    return short_url.shortened_url if short_url is not None else original_url