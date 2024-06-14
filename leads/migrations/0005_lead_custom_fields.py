# Generated by Django 4.1 on 2024-06-14 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_fields', '0005_alter_customfield_entity_id_and_more'),
        ('leads', '0004_remove_lead_assigned_to_lead_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='custom_fields',
            field=models.ManyToManyField(blank=True, related_name='lead_custom_fields', to='custom_fields.customfield'),
        ),
    ]
