from django.core.management.base import BaseCommand
from core.models import User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Assign user group"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('group_name', type=str, help='Group name')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        group_name = kwargs['group_name']

        try :
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
            return

        group, created = Group.objects.get_or_create(name=group_name)

        user.groups.add(group)
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group {group} created'))
        self.stdout.write(self.style.SUCCESS(f'User {user} added to group {group}'))
