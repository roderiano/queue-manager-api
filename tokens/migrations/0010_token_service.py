# Generated by Django 3.1.1 on 2020-09-13 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_remove_service_description'),
        ('tokens', '0009_remove_token_actived'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
    ]
