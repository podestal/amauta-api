# Generated by Django 5.1.3 on 2025-03-20 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0061_remove_announcement_clase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
