# Generated by Django 5.1.3 on 2025-01-29 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_alter_atendance_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Health_Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('natural_birth', models.BooleanField(default=True)),
                ('illness', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='tutor_phone',
        ),
        migrations.CreateModel(
            name='Birth_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('state', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='birth_info', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Emergency_Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contacts', to='school.student')),
            ],
        ),
    ]
