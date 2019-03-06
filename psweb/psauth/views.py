from django.views.generic import TemplateView, FormView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

class SignupView(TemplateView):
    template_name = 'signup.html'
    form_class = SignUpForm

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
            login(request, user)
            return redirect('dashboard')

class ProfileView (LoginRequiredMixin, FormView):
    template_name = "profile.html"
    form_class = ProfileForm

    # def get_form_kwargs( self ):
    #     kwargs = super( ProfileView, self ).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs
    # def get_context_data(self, **kwargs):
    #     context = super(ProfileView, self).get_context_data(**kwargs)
    #
    #     return context
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, user=self.request.user)
        form.save()
        return self.render_to_response(self.get_context_data(form=form))
