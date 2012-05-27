from django.conf.urls import patterns, url

from brevisurl import views


urlpatterns = patterns('brevisurl.views',
    url(r'^(?P<token>[a-zA-Z0-9]{5})$', views.BrevisUrlRedirectView.as_view(), name='brevisurl_redirect'),
)