# Generated by Django 3.2.14 on 2022-07-30 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hazard', '0002_auto_20220730_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='risk',
            name='level',
            field=models.CharField(default='Low', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(default='Open', max_length=8, unique=True),
        ),
    ]