# Generated by Django 4.1 on 2024-06-06 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant', '0001_initial'),
        ('calls', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calls',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_calls', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='calls',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant'),
        ),
    ]
