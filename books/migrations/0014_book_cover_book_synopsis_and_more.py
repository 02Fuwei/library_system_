# Generated by Django 4.2.5 on 2024-01-22 13:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_alter_userprofile_membership_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers', verbose_name='封面'),
        ),
        migrations.AddField(
            model_name='book',
            name='synopsis',
            field=models.TextField(blank=True, null=True, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='membership_expiry',
            field=models.DateField(default=datetime.datetime(2025, 1, 21, 13, 12, 15, 551263, tzinfo=datetime.timezone.utc)),
        ),
    ]
