# Generated by Django 4.2.5 on 2023-12-25 16:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='membership_expiry',
            field=models.DateField(default=datetime.datetime(2024, 12, 24, 16, 45, 58, 273781, tzinfo=datetime.timezone.utc)),
        ),
    ]
