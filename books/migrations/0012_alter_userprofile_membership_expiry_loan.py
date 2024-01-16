# Generated by Django 4.2.5 on 2024-01-12 07:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0011_book_alter_userprofile_membership_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='membership_expiry',
            field=models.DateField(default=datetime.datetime(2025, 1, 11, 7, 1, 12, 946676, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]