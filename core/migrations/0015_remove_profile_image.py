# Generated by Django 3.2.14 on 2022-08-06 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_profile_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
