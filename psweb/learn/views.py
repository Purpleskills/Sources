from django.views.generic import TemplateView
from django.shortcuts import redirect
from .models import *

class DashBoardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        context["courses"] = Course.objects.filter(status=1)
        return context

    # def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect('home')