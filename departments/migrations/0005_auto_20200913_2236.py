# Generated by Django 3.1.1 on 2020-09-14 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0004_auto_20200913_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='services',
            new_name='available_services',
        ),
    ]
