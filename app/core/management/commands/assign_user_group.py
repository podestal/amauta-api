from django.core.management.base import BaseCommand
from core.models import User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Assign user group"

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User id')
        parser.add_argument('group_name', type=str, help='Group name')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        group_name = kwargs['group_name']

        try :
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
            return

        created, group = Group.objects.get_or_create(name=group_name)

        user.groups.add(group)
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group {group} created'))
        self.stdout.write(self.style.SUCCESS(f'User {user} added to group {group}'))
