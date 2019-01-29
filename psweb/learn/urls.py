from django.conf.urls import url

from .views import *

app_name='learn'
urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^$', DashBoardView.as_view(), name='dashboard'),
    url(r'^ajax/load_subcats/$', load_subcats, name='ajax_load_subcats'),
    url(r'^ajax/load_courses/$', load_courses, name='ajax_load_courses'),
]