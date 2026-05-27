from django.urls import path
from . import views
from .views import loadsignup, loaddashboard, loadstarttest
from .views import loadlogin

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', loadsignup, name='signup'),
    path('login/', loadlogin, name='login'),
    path('dashboard/', loaddashboard, name='dashboard'),
    path('starttest/', loadstarttest, name='starttest'),
    path('signup_action/', views.signup_action, name='signupaction'),
    path('login_action/', views.login_action, name='loginaction'),
    path('examination/', views.loadexamination, name='examination'),
    path('logout_action/', views.logout_action, name='logout'),
]
