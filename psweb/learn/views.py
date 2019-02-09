from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, render
from .models import *
from .forms import *
import datetime
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from schedule.models import Calendar, Event, Rule
from schedule.settings import USE_FULLCALENDAR
from django.http import HttpResponse
import math
import logging

def load_subcats(request):
    catid = request.GET.get('category')
    subcats = CourseSubCategory.objects.filter(category__id=catid).order_by('name')
    return render(request, 'subcat_dropdown_options.html', {'subcats': subcats})

def load_courses(request):
    catid = request.GET.get('category')
    subcatid = request.GET.get('subcategory')
    provider = request.GET.get('provider')
    courses = Course.objects.filter(status=True).order_by('title')
    if catid != "":
        courses = courses.filter(category__id=catid).order_by('title')
        if subcatid != "":
            courses = courses.filter(subcategory__id=subcatid).order_by('title')
    if provider != "":
        courses = courses.filter(provider__id=provider).order_by('title')

    return render(request, 'course_list_component.html', {'courses': courses})


def init_calendar(request):
    user = request.user
    calendar_name = "scheduled_cal_" + str(user.id)
    calendar = Calendar.objects.get_or_create_calendar_for_object(obj=user, name=calendar_name)
    return HttpResponse(calendar_name)
    # return "{'calendar':calendar_name}"

def schedule_courses(request):
    try:
        courseid = request.GET.get('courseid')
        duration = int(request.GET.get('duration'))
        startdatestr = request.GET.get('startdate')
        course = Course.objects.get(pk=courseid)
        start = datetime.datetime.strptime(startdatestr, "%Y-%m-%d")
        end = start + timedelta(hours=duration)
        no_of_days_required = math.ceil(course.duration.seconds / 3600) / duration
        until = start + timedelta(days=no_of_days_required)
        rule = Rule.objects.create(frequency="DAILY")
        calendar_slug = 'scheduled_cal_' + str(request.user.id)
        calendar = Calendar.objects.get(slug=calendar_slug)
        event = Event.objects.create(
            title='Training: ' + course.title,
            start=start,
            end=end,
            rule=rule,
            calendar=calendar,
            end_recurring_period=until,
            creator=request.user
        )
        CourseUserRelation.objects.create(user=request.user, course=course, event=event)
        return HttpResponse("Success")
    except Exception as e:
        logging.getLogger('purpleskills').exception(msg="Course failed to schedule: " + "Course=" + str(course.id) + ";user=" + str(request.user.id) + "; msg=" + e.message)
        return HttpResponse("Failed")


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def rate_courses(request):
    eventid = request.POST.get('event')
    score = int(request.POST.get('score'))
    cur = CourseUserRelation.objects.get(event_id=eventid, user=request.user)
    cur.rating = score
    cur.save()
    return HttpResponse("Success")

class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    form_class = CourseFilterForm


    # def get_context_data(self, **kwargs):
    #     context = super(DashBoardView, self).get_context_data(**kwargs)
    #
    #     courses = Course.objects.filter(status=1)
    #     context["courses"] = courses
    #     return context

    def get(self, request, *args, **kwargs):
        form = CourseFilterForm()
        return self.render_to_response(self.get_context_data(form=form))


class  UserHistoryView(LoginRequiredMixin, ListView):
    template_name = 'course_history.html'
    model = Event
    paginate_by = 30
    raise_exception = True

    def get_queryset(self):
        return Event.objects.all().order_by('-end_recurring_period')
