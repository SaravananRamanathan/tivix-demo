# Generated by Django 4.0.6 on 2022-07-28 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_remove_share_shared_with_share_shared_with'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share',
            name='shared_with',
        ),
        migrations.AddField(
            model_name='share',
            name='shared_with',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
