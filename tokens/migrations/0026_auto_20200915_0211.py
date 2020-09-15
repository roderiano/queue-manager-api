# Generated by Django 3.1.1 on 2020-09-15 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0025_auto_20200914_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='status',
            field=models.CharField(choices=[('TIS', 'TOKEN ISSUED'), ('IAT', 'IN ATTENDENCE'), ('TAR', 'TOKEN ARCHIVED')], default='TIS', max_length=3),
        ),
    ]
