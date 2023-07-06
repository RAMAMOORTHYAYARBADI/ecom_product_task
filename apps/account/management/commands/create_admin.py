from django.core.management.base import BaseCommand, CommandError
from apps.users.models import User
from django.contrib.auth.hashers import make_password
from utils.enum import RoleEnum

class Command(BaseCommand):
    help = 'Create a superuser with the specified username and password'

    def handle(self, *args, **options):
        try:
            username = input("Enter the UserName: ")
            password = input("Enter the Password: ")
            email = input("Enter the Email: ")
            if User.objects.filter(email=email).exists():
                raise BaseException("Email already exists")
            role_id = RoleEnum.admin.value
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=make_password(password),
                role_id = role_id
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS("SuperUser created successfully"))
        except Exception as e:
            raise CommandError(e)
    