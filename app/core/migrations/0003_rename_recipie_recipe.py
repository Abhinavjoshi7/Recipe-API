# Generated by Django 4.0.10 on 2024-04-11 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recipie',
            new_name='Recipe',
        ),
    ]
