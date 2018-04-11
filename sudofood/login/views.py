from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import User

# Create your views here.
def index(request):
    template = loader.get_template('login/index.html')
    context = {}
    return render(request, 'login/index.html', context) 
    # return HttpResponse(template.render(context,request))

def user(request, user_id):
    return HttpResponse("This is the profile page for user %s!"%(user_id))


