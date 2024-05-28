# Generated by Django 4.1 on 2024-05-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='priority',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=6, null=True, verbose_name='Priority of Lead'),
        ),
    ]
