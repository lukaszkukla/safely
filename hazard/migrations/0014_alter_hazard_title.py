# Generated by Django 3.2.14 on 2022-08-27 22:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hazard', '0013_alter_hazard_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='title',
            field=models.CharField(max_length=80, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]