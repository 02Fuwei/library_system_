# Generated by Django 4.2.5 on 2023-12-25 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_userprofile_membership_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='library_id',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='membership_expiry',
            field=models.DateField(default=datetime.datetime(2024, 12, 24, 17, 0, 16, 637186, tzinfo=datetime.timezone.utc)),
        ),
    ]