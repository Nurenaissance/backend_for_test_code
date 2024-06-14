# Generated by Django 4.1 on 2024-06-14 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_fields', '0004_customfield_entity_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfield',
            name='entity_id',
            field=models.IntegerField(default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='customfield',
            name='model_name',
            field=models.CharField(choices=[('account', 'Account'), ('calls', 'calls'), ('lead', 'Lead'), ('interaction', 'Interaction'), ('conatact', 'Contact')], max_length=20),
        ),
    ]
