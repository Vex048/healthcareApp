# Generated by Django 5.1.6 on 2025-02-21 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_account_name_account_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='second_name',
        ),
    ]
