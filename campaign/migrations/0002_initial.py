# Generated by Django 4.1 on 2024-06-04 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaign', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='campaign_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaign_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='tenant',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant'),
        ),
    ]