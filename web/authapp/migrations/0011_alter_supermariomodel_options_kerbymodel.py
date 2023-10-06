# Generated by Django 4.2.4 on 2023-10-01 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0010_alter_dislikemodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supermariomodel',
            options={},
        ),
        migrations.CreateModel(
            name='KerbyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_result', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('allies_saved', models.IntegerField(default=0)),
                ('allies_lost', models.IntegerField(default=0)),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='kerby', to='authapp.profileuser')),
            ],
            options={
                'verbose_name': 'Super Mario',
                'verbose_name_plural': 'Super Mario',
            },
        ),
    ]
