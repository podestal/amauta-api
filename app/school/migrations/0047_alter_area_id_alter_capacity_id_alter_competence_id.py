# Generated by Django 5.1.3 on 2025-02-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0046_student_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='capacity',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='competence',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
