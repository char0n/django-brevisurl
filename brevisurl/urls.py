from django.urls import re_path

import brevisurl.settings
from brevisurl import views


urlpatterns = [
    re_path(
        brevisurl.settings.LOCAL_BACKEND_URL_PATTERN,
        views.BrevisUrlRedirectView.as_view(),
        name='brevisurl_redirect'
    ),
]
