# Generated by Django 4.2.4 on 2023-10-05 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_alter_kerbymodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duckhuntmodel',
            name='profile_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='duck_hunt', to='authapp.profileuser'),
        ),
        migrations.AlterField(
            model_name='kerbymodel',
            name='profile_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kerby', to='authapp.profileuser'),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='user_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supermariomodel',
            name='profile_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='super_mario', to='authapp.profileuser'),
        ),
        migrations.CreateModel(
            name='BombermanModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_win', models.IntegerField(default=0)),
                ('total_kills', models.IntegerField(default=0)),
                ('kill_npc_best', models.IntegerField(default=0)),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bomberman', to='authapp.profileuser')),
            ],
            options={
                'verbose_name': 'Bomberman',
                'verbose_name_plural': 'Bomberman',
            },
        ),
    ]
