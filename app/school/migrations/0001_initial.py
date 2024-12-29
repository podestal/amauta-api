# Generated by Django 5.1.3 on 2024-12-01 16:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('weight', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(blank=True, choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth')], max_length=1, null=True)),
                ('level', models.CharField(choices=[('P', 'Primary'), ('S', 'Secondary')], max_length=1)),
                ('section', models.CharField(default='A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Assignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.area')),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assignatures', to=settings.AUTH_USER_MODEL)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignatures', to='school.clase')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('quarter', models.CharField(choices=[('Q1', 'First Quarter'), ('Q2', 'Second Quarter'), ('Q3', 'Third Quarter'), ('Q4', 'Fourth Quarter')], max_length=2)),
                ('competences', models.CharField(max_length=255)),
                ('capacities', models.CharField(max_length=255)),
                ('assignature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.assignature')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.category')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to=settings.AUTH_USER_MODEL)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='school.clase')),
            ],
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.area')),
            ],
        ),
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.competence')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='instructor', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='school.school')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='school.instructor'),
        ),
        migrations.AddField(
            model_name='clase',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='school.clase')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.school')),
            ],
        ),
        migrations.CreateModel(
            name='QuarterGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calification', models.CharField(choices=[('AD', 'AD'), ('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=2)),
                ('quarter', models.CharField(choices=[('Q1', 'First Quarter'), ('Q2', 'Second Quarter'), ('Q3', 'Third Quarter'), ('Q4', 'Fourth Quarter')], max_length=2)),
                ('competence', models.CharField(max_length=255)),
                ('conclusion', models.TextField(blank=True, null=True)),
                ('assignature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.assignature')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='averages', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calification', models.CharField(choices=[('NA', 'NA'), ('AD', 'AD'), ('A', 'A'), ('B', 'B'), ('C', 'C')], default='NA', max_length=2)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('observations', models.TextField(blank=True, null=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='school.activity')),
                ('assignature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='school.assignature')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Atendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('L', 'Late'), ('N', 'Not Attended')], max_length=1)),
                ('hour', models.TimeField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='atendances', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutors', to='school.school')),
                ('students', models.ManyToManyField(related_name='tutors', to='school.student')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]