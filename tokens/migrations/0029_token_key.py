# Generated by Django 3.1.1 on 2020-11-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0028_auto_20201102_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='key',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
