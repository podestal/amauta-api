# Generated by Django 5.1.3 on 2025-02-01 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0031_remove_health_information_natural_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='insurance',
            field=models.CharField(blank=True, choices=[('E', 'Essalud'), ('P', 'Private'), ('S', 'SIS')], max_length=1, null=True),
        ),
    ]
