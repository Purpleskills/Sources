from django.views.generic import TemplateView, ListView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *

class SignupView(TemplateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/learn'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            employee_group = Group.objects.get(name='Employee')
            employee_group.user_set.add(user)

            login(request, user)
            return redirect('learn:dashboard')

class OrgListView(LoginRequiredMixin, ListView):
    template_name = 'orgs_list.html'
    model = Organization
    paginate_by = 30
    raise_exception = True

    def get_queryset(self):
        return Organization.objects.filter(company=self.request.user.org.company)
