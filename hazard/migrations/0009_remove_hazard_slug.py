# Generated by Django 3.2.14 on 2022-08-06 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hazard', '0008_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hazard',
            name='slug',
        ),
    ]