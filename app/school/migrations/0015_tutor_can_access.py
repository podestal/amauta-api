# Generated by Django 5.1.3 on 2025-01-08 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_remove_tutor_school_tutor_address_tutor_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='can_access',
            field=models.BooleanField(default=True),
        ),
    ]
