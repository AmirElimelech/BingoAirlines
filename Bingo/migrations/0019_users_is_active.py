# Generated by Django 4.2.2 on 2023-08-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0018_remove_airport_id_alter_airport_iata_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]