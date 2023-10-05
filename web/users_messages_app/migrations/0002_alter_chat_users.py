# Generated by Django 4.2.4 on 2023-10-01 14:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users_messages_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
