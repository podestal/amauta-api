# Generated by Django 5.1.3 on 2025-01-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_alter_student_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='uid',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
