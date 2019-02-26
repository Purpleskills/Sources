from django.conf.urls import include, url

from .views import *

app_name='mgmt'
urlpatterns = [
    url(r'', include('django.contrib.auth.urls')),
    url(r'^dash/$', ManagerDashboardView.as_view(), name='mgmt-dash'),
]