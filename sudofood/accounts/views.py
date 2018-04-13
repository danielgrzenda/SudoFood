from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

"""This creates a user view for the signup page"""


class SignUp(generic.CreateView):
    """This is the view for the sign up page.
    After a user creates an account this will send them back to the login page.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
