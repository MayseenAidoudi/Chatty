# Generated by Django 4.2.4 on 2023-08-19 19:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0003_app_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
