# Generated by Django 5.1.3 on 2025-02-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0045_health_information_hsndycap_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
