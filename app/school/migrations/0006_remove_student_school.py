# Generated by Django 5.1.3 on 2024-12-29 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_alter_atendance_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='school',
        ),
    ]
