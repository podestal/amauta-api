# Generated by Django 5.1.3 on 2025-01-31 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0030_alter_student_insurance_alter_student_main_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='health_information',
            name='natural_birth',
        ),
        migrations.AddField(
            model_name='birth_info',
            name='natural_birth',
            field=models.BooleanField(default=True),
        ),
    ]
