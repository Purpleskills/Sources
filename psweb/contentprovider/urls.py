from django.conf.urls import include, url

from .views import *

app_name='contentprovider'
urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),
    url(r'^udemy/$', UdemyImport.as_view(), name='udemy'),
    url(r'^pluralsight/$', PluralSightImport.as_view(), name='ps'),
    url(r'^coursera/$', CourseraImport.as_view(), name='ce'),
    url(r'^lynda/$', LyndaImport.as_view(), name='lynda'),
]