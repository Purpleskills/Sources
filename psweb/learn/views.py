from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import View
from django.shortcuts import redirect, render
import datetime
from datetime import timedelta
from schedule.models import Calendar, Event, Rule
from psauth.models import Organization
from core.models import CourseTag
from core.tagmanager import generate_tags
from .forms import *
import math
import logging
import operator
from django.db.models import Q
from functools import reduce
import json
import mptt

def load_courses(request):
    topics = request.GET.get('topic').split()
    difficulty = int(request.GET.get('difficulty'))
    duration = int(request.GET.get('duration'))
    courses = Course.objects.filter(status=1)
    if len(topics) > 0:
        courses = courses.filter(reduce(operator.and_, (Q(title__icontains=x) for x in topics)))
    if difficulty != "":
        courses = courses.filter(difficulty=difficulty)
    if duration == 1:
        courses = courses.filter(duration__lte=timedelta(hours=4))
    elif duration == 2:
        courses = courses.filter(Q(duration__lt=timedelta(hours=15)), Q(duration__gt=timedelta(hours=4)))
    elif duration == 3:
        courses = courses.filter(Q(duration__gt=timedelta(hours=15)))

    return render(request, 'course_list_component.html', {'courses': courses.order_by('title')[:10]})

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
            title=course.title,
            start=start,
            end=end,
            rule=rule,
            calendar=calendar,
            end_recurring_period=until,
            creator=request.user
        )
        cur = CourseUserRelation(user=request.user, course=course, event=event, status="Active")
        cur.save()
        return HttpResponse(calendar_slug)
    except Exception as e:
        logging.getLogger('purpleskills').exception(msg="Course failed to schedule: " + "Course=" + str(course.id) + ";user=" + str(request.user.id) + "; msg=" + str(e))
        return HttpResponse("")

def load_history(request):
    user = request.user
    active_events = Event.objects.filter(creator=user)
    if 0 == active_events.count():
        return HttpResponse("")

    return render(request, 'history_list_component.html', {'events': active_events})

def remove_event(request):
    user = request.user
    try:
        eventid = int(request.GET.get('eventid'))
        try:
            cur = CourseUserRelation.objects.get(user=user, event_id=eventid)
            cur.delete()
        except CourseUserRelation.DoesNotExist:
            pass
        event = Event.objects.get(pk=eventid, creator=user)
        event.delete()

        # calendar_slug = 'scheduled_cal_' + str(request.user.id)
        active_events = Event.objects.filter ( creator=user )
        if 0 == active_events.count():
            return HttpResponse("")

        return render(request, 'history_list_component.html', {'events': active_events})

    except Exception as e:
        logging.getLogger('purpleskills').exception(
            msg="Failed to remove course schedule: " + "event=" + str(event.id) + ";user=" + str(
                request.user.id) + "; msg=" + e.message)
        return HttpResponse("fail")

def complete_event(request):
    user = request.user
    try:
        eventid = int(request.GET.get('eventid'))
        try:
            cur = CourseUserRelation.objects.get(user=user, event_id=eventid)
            cur.status="Complete"
            cur.save()
        except CourseUserRelation.DoesNotExist:
            pass

        # calendar_slug = 'scheduled_cal_' + str(request.user.id)
        active_events = Event.objects.filter ( creator=user )
        if 0 == active_events.count():
            return HttpResponse("")

        return render(request, 'history_list_component.html', {'events': active_events})

    except Exception as e:
        logging.getLogger('purpleskills').exception(
            msg="Failed to remove course schedule: " + "event=" + str(eventid) + ";user=" + str(
                request.user.id) + "; msg=" + e.message)
        return HttpResponse("fail")


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

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)

        okrs = Objective.objects.filter(user=self.request.user)
        context["okrs"] = okrs
        return context

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


class CourseFilterView (LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        results = {'success':False}
        GET = request.GET
        if 'term' in request.GET:
            term = request.GET['term']
            data = Course.objects.filter(title__icontains=term).values_list('title', flat=True)
            json = list(data)
            results = {'data': data}

        result_json = json.dumps(results)
        return HttpResponse(result_json, content_type='application/json')


class OKRSettingView (LoginRequiredMixin, CreateView):
    model = Objective
    form_class = ObjectiveForm
    template_name = 'goalsetting.html'
    success_url = None
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(OKRSettingView, self).get_context_data(**kwargs)
        # context["orgs"] = Organization.objects.filter(company=self.request.user.org.company)
        # if self.request.POST:
        #     context['formset'] = OKRFormSet(self.request.POST)
        # else:
        #     context["formset"] = OKRFormSet()
        context['formset'] = OKRFormSet()
        return context

    def get_form_kwargs(self):
        kwargs = super(OKRSettingView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        # kwargs['company'] = self.request.user.org.company
        return kwargs

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     okrs = context['formset']
    #     with transaction.atomic():
    #         form.instance.user = self.request.user
    #         form.instance.company = self.request.user.org.company
    #         self.object = form.save()
    #         if okrs.is_valid():
    #             okrs.instance = self.object
    #             okrs.save()
    #             return super(OKRSettingView, self).form_valid(form)
    #         else:
    #             return super(OKRSettingView, self).form_invalid(form)
    #
    # def get_success_url(self):
    #     return reverse_lazy('learn:okr-set')  # , kwargs={'pk': self.object.pk}

@csrf_exempt
def save_okr (request):
    user = request.user
    post = request.POST
    o_id = post.get('id')
    if o_id == "":
        errormsg = create_okr (post, user)
    else:
        errormsg = update_okr(o_id, post, user)
    if (errormsg != ""):
        return HttpResponse(errormsg, status=500)

    return render(request, 'okr_include.html', {'form': ObjectiveForm(), 'formset': OKRFormSet()})
    # return HttpResponse("")

def analyze_okr (okr):
    otags = generate_tags(okr.name)
    for kr in okr.keyresult_set.all():
        for tag in generate_tags(kr.name):
            otags.append(tag)

    for tag in otags:
        okr.tags.add(tag)
    # from nltk.corpus import stopwords
    # stop_words = set(stopwords.words('english'))
    # line = okr.name
    # for kr in okr.keyresult_set.all():
    #     line += " " + kr.name
    # words = line.split()
    # appendFile = open('filteredtext.txt', 'a')
    # stopFile = open('stoppedtext.txt', 'a')
    # for r in words:
    #     if not r in stop_words:
    #         appendFile.write(" " + r)
    #     else:
    #         stopFile.write(" " + r)
    # appendFile.close()
    # stopFile.close()

def create_okr (post, user):
    errormsg = ""
    try:
        o_name = post.get('name')
        if (o_name == ""):
            errormsg += "Objective should be filled.\n"
        kr_count = int(post.get("keyresult_set-TOTAL_FORMS"))
        objective = Objective(name=o_name, user=user, company=user.org.company)
        objective.save()
        for index in range(0, kr_count):
            kr_name = post.get("keyresult_set-" + str(index) + "-name")
            if (kr_name == None or kr_name == ""):
                errormsg += "Key result fields should be filled. You should add at least 1 key result."
                raise ValueError(errormsg)
            else:
                kr_difficulty = post.get("keyresult_set-" + str(index) + "-difficulty")
                kr = KeyResult(name=kr_name, objective=objective, difficulty=kr_difficulty)
                kr.save()
        analyze_okr(objective)
    except Exception as e:
        if (errormsg == ""):
            logging.getLogger('purpleskills').exception(
                msg="save_okr: Failed to save OKR: " + "objective=" + o_name + "; user=" + str(
                    user.id) + "; msg=" + str(e))
        errormsg = "Create failed. Pease try again."
    return errormsg

def update_okr(o_id, post, user):
    errormsg = ""
    try:
        objective = Objective.objects.get(pk=o_id)
        o_name = post.get('name')
        objective.name = o_name
        kr_count = int(post.get("keyresult_set-TOTAL_FORMS"))
        new_krs = []
        old_krs = objective.keyresult_set.filter (objective=objective)
        old_kr_ids = list(old_krs.values_list('id', flat=True))
        for index in range(0, kr_count):
            kr_name = post.get("keyresult_set-" + str(index) + "-name")
            if (kr_name != None and kr_name != ""): # ignore empty KRs
                kr_difficulty = int(post.get("keyresult_set-" + str(index) + "-difficulty"))
                id_str = post.get("keyresult_set-" + str(index) + "-id")
                kr_id = int(id_str) if id_str.isdigit() else 0
                kr_delete = post.get("keyresult_set-" + str(index) + "-DELETE")
                if kr_delete == 'on':  #marked for delete
                    continue
                if kr_id in old_kr_ids: # update
                    old_kr = old_krs.get(id=kr_id)
                    old_kr.name = kr_name
                    old_kr.difficulty = kr_difficulty
                    new_krs.append(old_kr)
                    old_kr_ids.remove(kr_id)
                else: # insert new
                    new_krs.append(KeyResult(name=kr_name, objective=objective, difficulty=kr_difficulty))
        if len (old_kr_ids) > 0:  # some old KRs that user deleted during update
            discarded_kr = old_krs.filter(id__in=old_kr_ids)
            discarded_kr.delete()
        if len(new_krs) > 0:
            for kr in new_krs:
                kr.save()
            objective.save()
        else:
            errormsg = "Key result fields should be filled. You should add at least 1 key result."
            raise ValueError(errormsg)
        analyze_okr(objective)
    except Objective.DoesNotExist:
        errormsg += "Objective is not found in the database. Please create a new one."
        pass
    except Exception as e:
        if (errormsg == ""):
            logging.getLogger('purpleskills').exception(
                msg="save_okr: Failed to update OKR: " + "objective=" + o_name + "; user=" + str(
                    user.id) + "; msg=" + str(e))
            errormsg ="Update failed. Pease try again."

    return errormsg


class OKRSettingUpdateView(LoginRequiredMixin, UpdateView):
    model = Objective
    form_class = ObjectiveForm
    template_name = 'goalsetting.html'
    success_url = None
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(OKRSettingUpdateView, self).get_context_data(**kwargs)
        # context["orgs"] = Organization.objects.filter(company=self.request.user.org.company)
        context['formset'] = OKRFormSet(instance=self.object)
        return context


def list_okr (request):
    allokrs = Objective.objects.filter(user = request.user)
    return render(request, 'okr_list_include.html', {'okrs': allokrs, 'user':request.user} )


def delete_okr (request):
    user = request.user
    oid = request.GET.get('okrid')
    errormsg = ""
    try:
        obj = Objective.objects.get(pk=oid)
        obj.keyresult_set.all().delete()
        obj.delete()
    except Objective.DoesNotExist:
        return HttpResponse("OKR object not found", status=500)

    return HttpResponse("")


def hint_objectives (request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = list(Objective.objects.filter(name__icontains = q ).values_list('name', flat=True)[:20])

        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

