import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

MAT = 'admin'
EMAIL = 'admin@local'
PWD = 'adminpass'

if User.objects.filter(matricula=MAT).exists():
    print(f"Superuser with matricula='{MAT}' already exists")
else:
    User.objects.create_superuser(matricula=MAT, email=EMAIL, password=PWD)
    print(f"Created superuser matricula='{MAT}' email='{EMAIL}'")
