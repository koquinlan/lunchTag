# Generated by Django 3.2.14 on 2022-07-31 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20220731_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tag_pairing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pairing', to=settings.AUTH_USER_MODEL),
        ),
    ]