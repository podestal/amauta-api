
from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Add tutor profile for every user for tutor'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            if user.email and '@' in user.email and user.email.split('@')[1]:
                user.profile = 'tutor'
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Added tutor profile for user: {user.username}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Skipping user {user.username} with email {user.email} as it is not a tutor'
                ))
        self.stdout.write(self.style.SUCCESS('Successfully added tutor profiles for all users.'))
