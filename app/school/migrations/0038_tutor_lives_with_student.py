# Generated by Django 5.1.3 on 2025-02-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0037_tutor_city_tutor_civil_status_tutor_county_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='lives_with_student',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
