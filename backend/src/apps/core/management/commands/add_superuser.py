from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import environ
class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        env = environ.Env()
        if not User.objects.filter(is_superuser=True).exists():
            username = env('ADMIN_USERNAME', default='admin')
            email = env('ADMIN_EMAIL', default=None)
            password = env('ADMIN_PASSWORD', default='admin')
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
