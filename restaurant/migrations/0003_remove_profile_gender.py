# Generated by Django 5.0 on 2024-07-17 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_remove_profile_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
    ]