# Generated by Django 4.2.10 on 2024-03-15 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-due_date']},
        ),
    ]