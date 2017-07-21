import os
import pytest


def env_var_exists():
    try:
        os.environ['FETCH_TEST_TOKEN']
        return True
    except KeyError:
        return False


missing_test_token = pytest.mark.skipif(not env_var_exists(), reason='Missing test token')
