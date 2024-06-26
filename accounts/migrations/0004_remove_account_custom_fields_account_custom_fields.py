# Generated by Django 4.1 on 2024-06-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_fields', '0005_alter_customfield_entity_id_and_more'),
        ('accounts', '0003_account_custom_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='custom_fields',
        ),
        migrations.AddField(
            model_name='account',
            name='custom_fields',
            field=models.ManyToManyField(blank=True, related_name='account_custom_fields', to='custom_fields.customfield'),
        ),
    ]
