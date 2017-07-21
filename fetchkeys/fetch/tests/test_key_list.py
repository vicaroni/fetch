from unittest.mock import Mock
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.management import call_command

from fetch.models import Token, UserRepository, DeployKey

pytestmark = pytest.mark.django_db


def test_key_list(client):
    """Tests key_list proper listing of tokens, repos and keys"""
    user = User.objects.create(username='prova')
    user.set_password('123456')
    user.save()
    client.login(username='prova', password='123456')
    Token.objects.create(user=user, description='Token', token='token')
    repo = UserRepository.objects.create(user=user, name='Repo')
    DeployKey.objects.create(repository=repo, title='Key', key='ssh-rsa')
    response = client.get(reverse('key_list', args=('',))).content
    assert b'Token' in response
    assert b'token' in response
    assert b'Repo' in response
    assert b'Key' in response
    assert b'ssh-rsa' in response


def test_key_download_command(mocker):
    """Tests database UserRepository and DeployKey entries after calling key_download"""
    mock_github = mocker.patch('fetch.management.commands.key_download.Github')
    grepos = [Mock() for i in range(3)]
    for grepo in grepos:
        grepo.permissions.admin = True
        grepo.full_name = 'Repo' + str(grepos.index(grepo))
        grepo.get_keys.return_value = [
            Mock(title='key1', key='ssh-rsa 1'),
            Mock(title='key2', key='ssh-rsa 2'),
            Mock(title='key3', key='ssh-rsa 3')]
    grepos[2].permissions.admin = False
    mock_github.return_value.get_user.return_value.get_repos.return_value = grepos
    user = User.objects.create(username='prova')
    token = Token.objects.create(user=user, description='Token prova', token='prova')
    result = call_command('key_download', user.username, token.token)
    assert result != 'not_found'
    repo0 = UserRepository.objects.get(name='Repo0')
    repo1 = UserRepository.objects.get(name='Repo1')
    assert repo0
    assert repo1
    assert pytest.raises(UserRepository.DoesNotExist, UserRepository.objects.get, name='Repo2')
    assert DeployKey.objects.get(repository=repo0, title='key1')
    assert DeployKey.objects.get(repository=repo0, title='key2')
    assert DeployKey.objects.get(repository=repo0, title='key3')
    assert DeployKey.objects.get(repository=repo1, title='key1')
    assert DeployKey.objects.get(repository=repo1, title='key2')
    assert DeployKey.objects.get(repository=repo1, title='key3')


def test_delete(client):
    """Tests Token, UserRepository and DeployKey deleting after calling delete view"""
    user = User.objects.create(username='prova')
    user.set_password('123456')
    user.save()
    client.login(username='prova', password='123456')
    token = Token.objects.create(user=user, description='Token', token='token')
    repo = UserRepository.objects.create(user=user, name='Repo')
    key = DeployKey.objects.create(repository=repo, title='Key', key='ssh-rsa')
    client.get(reverse('delete', args=('token', token.description)))
    client.get(reverse('delete', args=('repo', repo.name)))
    assert pytest.raises(Token.DoesNotExist, Token.objects.get, description=token.description)
    assert pytest.raises(UserRepository.DoesNotExist, UserRepository.objects.get, name=repo.name)
    assert pytest.raises(DeployKey.DoesNotExist, DeployKey.objects.get, title=key.title)
