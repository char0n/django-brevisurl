from django.conf.urls import patterns, url

import brevisurl.settings
from brevisurl import views


urlpatterns = patterns('brevisurl.views',
    url(brevisurl.settings.LOCAL_BACKEND_URL_PATTERN, views.BrevisUrlRedirectView.as_view(), name='brevisurl_redirect'),
)