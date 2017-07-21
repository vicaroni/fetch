Tool for managing Deploy Keys for Repositories on Github

Registering a user and a Personal Access Token it lists repositories where the user has admin permissions.
Under every repository there is a list of its deploy keys.

To test, run tox or 'python runtests.py'
Unless environment variable 'FETCH_TEST_TOKEN' is set (it must be set to a valid token), it will skip integration test with Github API
