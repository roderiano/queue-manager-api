# Generated by Django 3.1.1 on 2020-09-13 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0003_auto_20200913_0239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='archived_date',
        ),
        migrations.RemoveField(
            model_name='token',
            name='attendence_date',
        ),
        migrations.RemoveField(
            model_name='token',
            name='issue_date',
        ),
    ]
