from github import Github
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fetch.models import UserRepository, DeployKey


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('token', type=str)

    def handle(self, *args, **options):
        """Fetches user repositories with admininstrator permissions and lists them with their deploy keys"""
        try:
            git_user = Github(options['token']).get_user()
        except:
            return 'not_found'  # User not found on Github
        local_user = User.objects.get(username=options['username'])
        for repo in git_user.get_repos():
            if repo.permissions.admin:
                local_repo = UserRepository.objects.get_or_create(user=local_user, name=repo.full_name)[0]
                for key in repo.get_keys():
                    DeployKey.objects.get_or_create(repository=local_repo, title=key.title, key=key.key)
