# Generated by Django 5.1.3 on 2025-01-30 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0027_student_insurance'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='main_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.language'),
        ),
    ]
