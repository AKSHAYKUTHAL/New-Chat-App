# Generated by Django 5.0.1 on 2024-02-09 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='registered',
            new_name='is_registered',
        ),
    ]
