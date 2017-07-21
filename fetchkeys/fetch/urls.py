from django.conf.urls import url
from . import views
import django.contrib.auth.views

urlpatterns = [
    url(r'^list/(?P<response>(update)*)$', views.key_list, name='key_list'),
    url(r'^token/$', views.user_form, name='user_form'),
    url(r'^$', django.contrib.auth.views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^delete/(?P<thing>token|repo|key)/(?P<obj>[\s\S]*)/$', views.delete, name='delete')
]
