# Generated by Django 5.1.6 on 2025-03-09 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_dlmodels'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('date', models.DateField()),
                ('model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.dlmodels')),
            ],
        ),
    ]
