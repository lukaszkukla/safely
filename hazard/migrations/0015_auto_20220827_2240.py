# Generated by Django 3.2.14 on 2022-08-27 22:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hazard', '0014_alter_hazard_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=80, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='risk',
            name='level',
            field=models.CharField(max_length=6, unique=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=8, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
