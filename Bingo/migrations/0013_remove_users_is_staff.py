# Generated by Django 4.2.2 on 2023-07-31 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0012_users_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='is_staff',
        ),
    ]
