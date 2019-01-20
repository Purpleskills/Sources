from django.conf.urls import url
from .views import *

app_name='learn'
urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^$', DashBoardView.as_view(), name='dashboard'),
]