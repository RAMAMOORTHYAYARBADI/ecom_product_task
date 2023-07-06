from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Command to create a User Roles"
    def handle(self, *args, **options):
        try:
            """create user roles in Role master table"""
            roles = ["ADMIN","USER"]
            for i in roles:
                val = Group.objects.update_or_create(name=i)
        except Exception as e:
            raise CommandError(e)