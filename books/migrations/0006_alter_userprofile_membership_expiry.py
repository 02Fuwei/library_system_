# Generated by Django 4.2.5 on 2023-12-26 01:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_userprofile_fines_alter_userprofile_loan_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='membership_expiry',
            field=models.DateField(default=datetime.datetime(2024, 12, 25, 1, 52, 40, 822594, tzinfo=datetime.timezone.utc)),
        ),
    ]
