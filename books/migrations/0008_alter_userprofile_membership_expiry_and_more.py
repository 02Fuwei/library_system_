# Generated by Django 4.2.5 on 2023-12-28 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_userprofile_membership_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='membership_expiry',
            field=models.DateField(default=datetime.datetime(2024, 12, 27, 15, 41, 24, 942047, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='membership_type',
            field=models.IntegerField(default=0),
        ),
    ]
