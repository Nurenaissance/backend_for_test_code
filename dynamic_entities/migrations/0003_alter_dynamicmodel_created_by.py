# Generated by Django 4.1 on 2024-06-06 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dynamic_entities', '0002_dynamicmodel_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicmodel',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
