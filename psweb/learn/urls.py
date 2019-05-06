from django.conf.urls import url

from .views import *

app_name='learn'
urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^$', DashBoardView.as_view(), name='dashboard'),
    url(r'^history/$', UserHistoryView.as_view(), name='user-history'),
    url(r'^okr/$', OKRSettingView.as_view(), name='okr-set'),

    url(r'^ajax/topic/autocomplete/$', CourseFilterView.as_view(), name='ajax_tpic_filter'),
    url(r'^ajax/load_courses/$', load_courses, name='ajax_load_courses'),
    url(r'^ajax/init_calendar/$', init_calendar, name='ajax_init_calendar'),
    url(r'^ajax/schedule_courses/$', schedule_courses, name='ajax_schedule_courses'),
    url(r'^ajax/rate/course/$', rate_courses, name='ajax_rate_courses'),
    url(r'^ajax/remove/event/$', remove_event, name='ajax_remove_event'),
    url(r'^ajax/complete/event/$', complete_event, name='ajax_complete_event'),
    url(r'^ajax/load/history/$', load_history, name='ajax_load_history'),
    url(r'^ajax/save/okr/$', save_okr, name='ajax_save_okr'),
    url(r'^ajax/list/myokr/$', list_okr, name='ajax_list_my_okr'),
]