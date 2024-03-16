# Generated by Django 4.2.10 on 2024-03-16 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomodoro', '0004_pomodorosession_remove_pomodorobreak_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pomodorosession',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=1500)),
        ),
    ]