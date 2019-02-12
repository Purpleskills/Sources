from django.conf.urls import include, url

from .views import *

app_name='contentprovider'
urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),
    url(r'^udemy/$', UdemyImport.as_view(), name='signup'),
]