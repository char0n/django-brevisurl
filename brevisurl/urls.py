from django.conf.urls import url

import brevisurl.settings
from brevisurl import views


urlpatterns = [
    url(brevisurl.settings.LOCAL_BACKEND_URL_PATTERN, views.BrevisUrlRedirectView.as_view(), name='brevisurl_redirect'),
]
