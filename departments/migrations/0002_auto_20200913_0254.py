# Generated by Django 3.1.1 on 2020-09-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departament',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
