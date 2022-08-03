# Generated by Django 3.2.14 on 2022-08-02 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paired1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paired2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
