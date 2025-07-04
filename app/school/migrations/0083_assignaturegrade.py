# Generated by Django 5.1.3 on 2025-06-07 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0082_areagrade'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignatureGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calification', models.CharField(choices=[('AD', 'AD'), ('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=2)),
                ('quarter', models.CharField(choices=[('Q1', 'First Quarter'), ('Q2', 'Second Quarter'), ('Q3', 'Third Quarter'), ('Q4', 'Fourth Quarter')], max_length=2)),
                ('assignature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignature_averages', to='school.assignature')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignature_averages', to='school.student')),
            ],
        ),
    ]
