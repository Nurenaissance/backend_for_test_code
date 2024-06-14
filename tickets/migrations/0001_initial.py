# Generated by Django 4.1 on 2024-06-13 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0002_initial'),
        ('accounts', '0003_account_custom_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casenumber', models.CharField(max_length=100, unique=True)),
                ('subject', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('webemail', models.EmailField(max_length=254)),
                ('case_reason', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], max_length=20)),
                ('date', models.DateField()),
                ('owner', models.CharField(max_length=100)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=20)),
                ('type', models.CharField(choices=[('issue', 'Issue'), ('request', 'Request'), ('bug', 'Bug')], max_length=20)),
                ('case_origin', models.CharField(choices=[('phone', 'Phone'), ('email', 'Email'), ('web', 'Web'), ('social_media', 'Social Media')], max_length=20)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Ticket', to='accounts.account')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Ticket', to='contacts.contact')),
            ],
        ),
    ]
