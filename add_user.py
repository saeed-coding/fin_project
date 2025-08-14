import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fastinn_project.settings")  # change to your settings
django.setup()

from django.contrib.auth.models import User


def add_user(username, password):
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists.")
    else:
        User.objects.create_user(username=username, password=password)
        print("User added successfully!")


if __name__ == "__main__":
    add_user("admin2", "admin1234")
