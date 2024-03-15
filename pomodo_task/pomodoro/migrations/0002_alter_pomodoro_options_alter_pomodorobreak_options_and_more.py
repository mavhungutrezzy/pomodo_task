# Generated by Django 4.2.10 on 2024-03-15 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pomodoro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pomodoro',
            options={'verbose_name': 'Pomodoro', 'verbose_name_plural': 'Pomodoros'},
        ),
        migrations.AlterModelOptions(
            name='pomodorobreak',
            options={'verbose_name': 'Pomodoro Break', 'verbose_name_plural': 'Pomodoro Breaks'},
        ),
        migrations.RemoveField(
            model_name='pomodoro',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pomodoro',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='pomodoro',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='pomodorobreak',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pomodorobreak',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='pomodorobreak',
            name='is_deleted',
        ),
        migrations.AddField(
            model_name='pomodoro',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pomodoros', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pomodorobreak',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_breaks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pomodoro',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pomodoros_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pomodorobreak',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='breaks_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]