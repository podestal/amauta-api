# Generated by Django 5.1.3 on 2025-02-20 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0042_assistant_school_clase_school_instructor_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clase',
            name='section',
            field=models.CharField(default='U', max_length=1),
        ),
    ]
