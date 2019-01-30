from django.conf.urls import include, url

from .views import *

app_name='auth'
urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
]