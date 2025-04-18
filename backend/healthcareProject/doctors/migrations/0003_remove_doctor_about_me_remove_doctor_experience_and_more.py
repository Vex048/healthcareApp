# Generated by Django 5.1.6 on 2025-02-20 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_alter_doctor_about_me_alter_doctor_second_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='about_me',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='graduation',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='specialization',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_me', models.TextField(blank=True, null=True)),
                ('experience', models.TextField(null=True)),
                ('graduation', models.TextField(null=True)),
                ('specialization', models.TextField(null=True)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
            ],
        ),
    ]
