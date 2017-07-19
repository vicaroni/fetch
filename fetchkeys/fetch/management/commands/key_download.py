from django.core.management.base import BaseCommand, CommandError
from github import Github
from django.contrib.auth.models import User
from fetch.models import UserRepository, DeployKey
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('token', type=str)

    def handle(self, *args, **options):
        try:
            git_user = Github(options['token']).get_user()
        except:
            print('Token does not exist on Github')
            return -1
        local_user = User.objects.get(username=options['username'])
        for repo in git_user.get_repos():
            try:
                local_repo = local_user.repos.get(name=repo.full_name)
            except ObjectDoesNotExist:
                local_repo = UserRepository.objects.create(user=local_user, name=repo.full_name)
            for key in repo.get_keys():
                try:
                    local_repo.keys.get(title=key.title)
                except ObjectDoesNotExist:
                    DeployKey.objects.create(repository=local_repo, title=key.title, key=key.key)
