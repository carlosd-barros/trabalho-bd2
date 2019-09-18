from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from .forms import *


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        if self.request.method == "POST":
            form = UserCreationForm(self.request.POST)
            if form.is_valid():
                username = self.request.user.username
                messages.success(self.request, f'{username}, sua conta foi criada com sucesso!')
        else:
            form = UserCreationForm()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('queryzitas:home')
