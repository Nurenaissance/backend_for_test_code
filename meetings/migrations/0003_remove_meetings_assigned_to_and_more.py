# Generated by Django 4.1 on 2024-05-16 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0003_contact_tenant"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meetings", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="meetings",
            name="assigned_to",
        ),
        migrations.AlterField(
            model_name="meetings",
            name="contact_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meeting_contacts",
                to="contacts.contact",
                verbose_name="Contact Name",
            ),
        ),
        migrations.RemoveField(
            model_name="meetings",
            name="participants",
        ),
        migrations.AddField(
            model_name="meetings",
            name="assigned_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="meeting_assigned_users",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="meetings",
            name="participants",
            field=models.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meeting_participants",
                to="contacts.contact",
            ),
            preserve_default=False,
        ),
    ]