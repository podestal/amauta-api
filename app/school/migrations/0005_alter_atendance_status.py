# Generated by Django 5.1.3 on 2024-12-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_remove_atendance_hour_atendance_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendance',
            name='status',
            field=models.CharField(choices=[('O', 'On Time'), ('L', 'Late'), ('N', 'Not Attended'), ('E', 'Excused'), ('E', 'Left Early')], max_length=1),
        ),
    ]