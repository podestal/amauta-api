# Generated by Django 5.1.3 on 2025-01-07 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0013_atendance_attendance_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='school',
        ),
        migrations.AddField(
            model_name='tutor',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tutor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='tutor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
