from django.conf.urls import url
from . import views
import django.contrib.auth.views

urlpatterns = [
    url(r'^list/$', views.key_list, name='key_list'),
    url(r'^token/$', views.user_form, name='user_form'),
    url(r'^$', django.contrib.auth.views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
]
