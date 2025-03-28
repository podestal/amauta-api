# Generated by Django 5.1.3 on 2025-03-19 12:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0056_instructor_email_instructor_phone_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(choices=[('I', 'Informative'), ('A', 'Attention'), ('E', 'Emergency')], default='I', max_length=1),
        ),
        migrations.AddField(
            model_name='announcement',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='school.school'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
