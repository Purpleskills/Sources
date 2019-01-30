from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

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