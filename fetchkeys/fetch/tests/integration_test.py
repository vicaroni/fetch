import os

import pytest
from django.core.management import call_command
from django.contrib.auth.models import User

from . import missing_test_token
from fetch.models import UserRepository, DeployKey


@pytest.mark.django_db
@missing_test_token
def test_key_download():
    """
    Tests key_download integration with Github using a real token
    and calling get_user(), get_repos(), get_keys()
    """
    user = User.objects.create(username='testuser').username
    call_command('key_download', user, os.environ.get('FETCH_TEST_TOKEN'))
    assert UserRepository.objects.all()
    assert DeployKey.objects.all()
