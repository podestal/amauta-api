# Generated by Django 5.1.3 on 2024-12-29 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_remove_instructor_school_instructor_clases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atendance',
            name='hour',
        ),
        migrations.AddField(
            model_name='atendance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='atendance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]