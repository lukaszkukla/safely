# Generated by Django 3.2.14 on 2022-08-06 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hazard', '0009_remove_hazard_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hazard',
            name='description',
        ),
    ]
