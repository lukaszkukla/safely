# Generated by Django 3.2.14 on 2022-08-06 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hazard', '0006_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
    ]