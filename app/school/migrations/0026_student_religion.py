# Generated by Django 5.1.3 on 2025-01-30 15:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_student_address_student_celphone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='religion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='school.religion'),
        ),
    ]
