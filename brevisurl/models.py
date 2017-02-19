import hashlib
import logging
from django.core.exceptions import ValidationError

from django.db import models
from django.core.validators import URLValidator

from brevisurl import get_connection
import brevisurl.settings


log = logging.getLogger(__name__)


class ShortUrl(models.Model):
    """Model that represents shortened url."""
    original_url = models.URLField(max_length=brevisurl.settings.LOCAL_BACKEND_ORIGINAL_URL_MAX_LENGTH,
                                   null=False, blank=False)
    original_url_hash = models.CharField(max_length=64, null=False, blank=False)
    shortened_url = models.URLField(max_length=200, null=False, blank=False, unique=True)
    backend = models.CharField(max_length=200, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True, null=False, blank=False)

    def __unicode__(self):
        return self.shortened_url

    def get_connection(self, fail_silently=False):
        if not hasattr(self, 'brevis_connection'):
            if self.pk is not None:
                self.brevis_connection = get_connection(backend=self.backend,
                                                        fail_silently=fail_silently)
            else:
                self.brevis_connection = get_connection(fail_silently=fail_silently)
        return self.brevis_connection

    def clean(self):
        url_validator = URLValidator()
        try:
            url_validator(self.original_url)
        except ValidationError:
            log.exception('ShortUrl.original_url "%s" is not valid URL', self.original_url)
            raise
        try:
            url_validator(self.shortened_url)
        except ValidationError:
            log.exception('ShortUrl.shortened_url "%s" is not valid URL', self.shortened_url)
            raise
        return super(ShortUrl, self).clean()

    def save(self, force_insert=False, force_update=False, using=None):
        if self.pk is None and not self.original_url_hash:
            self.original_url_hash = self.url_hash(self.original_url)
        self.full_clean()
        return super(ShortUrl, self).save(force_insert, force_update, using)

    @staticmethod
    def url_hash(url):
        return hashlib.sha256(url).hexdigest()

    class Meta:
        unique_together = (('original_url_hash', 'backend'),)
        verbose_name = 'Short url'
        verbose_name_plural = 'Short urls'
        ordering = ['-created']
        get_latest_by = 'created'
