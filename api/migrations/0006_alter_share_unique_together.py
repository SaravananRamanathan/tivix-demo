# Generated by Django 4.0.6 on 2022-07-28 07:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_alter_share_shared_with'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='share',
            unique_together={('budget', 'shared_with')},
        ),
    ]
