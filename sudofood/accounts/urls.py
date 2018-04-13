from django.urls import path
from . import views


"""Create URL for the signup page"""
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
