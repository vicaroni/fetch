from django.http import HttpRequest
from django.contrib.auth.models import User
import pytest

from fetch.views import user_form, register
from fetch.models import Token

pytestmark = pytest.mark.django_db

def test_user_form(client):
    user = User.objects.create(username='prova')
    user.set_password('123456')
    user.save()
    client.login(username='prova', password='123456')
    request = HttpRequest()
    request.user = user
    request.method = 'POST'
    request.POST = {'description': 'token prova', 'token': 'token prova'}
    user_form(request)
    assert Token.objects.get(description='token prova').description == 'token prova'

def test_register():
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'username': 'prova', 'password1': '8characters', 'password2': '8characters'}
    register(request)
    assert User.objects.get(username='prova').username == 'prova'
