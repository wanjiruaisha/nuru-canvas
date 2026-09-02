import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create a production administrator from environment variables."""

    help = 'Create an administrator if one does not already exist.'

    def handle(self, *args, **options):
        username = os.environ.get(
            'DJANGO_SUPERUSER_USERNAME'
        )
        email = os.environ.get(
            'DJANGO_SUPERUSER_EMAIL'
        )
        password = os.environ.get(
            'DJANGO_SUPERUSER_PASSWORD'
        )

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Admin environment variables are missing. '
                    'Skipping administrator creation.'
                )
            )
            return

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    'Administrator already exists.'
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Administrator created successfully.'
            )
        )