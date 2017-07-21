from django.http import HttpRequest
from django.contrib.auth.models import User
import pytest

from fetch.views import user_form, register
from fetch.models import Token

pytestmark = pytest.mark.django_db


def test_user_form(client):
    """Tests user_form is creating Token"""
    user = User.objects.create(username='prova')
    user.set_password('123456')
    user.save()
    client.login(username='prova', password='123456')
    request = HttpRequest()
    request.user = user
    request.method = 'POST'
    request.POST = {'description': 'token prova', 'token': 'token prova'}
    user_form(request)
    assert Token.objects.get(description='token prova')


def test_register():
    """Tests register is creating User"""
    request = HttpRequest()
    request.method = 'POST'
    request.POST = {'username': 'prova', 'password1': '8characters', 'password2': '8characters'}
    register(request)
    assert User.objects.get(username='prova')
