# Generated by Django 5.1.3 on 2024-11-30 18:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0003_profile_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userpolicy',
            unique_together={('user', 'policy', 'plan')},
        ),
    ]
