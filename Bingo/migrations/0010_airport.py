# Generated by Django 4.2.2 on 2023-07-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0009_alter_flights_remaining_tickets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('iata_code', models.CharField(max_length=3)),
            ],
        ),
    ]
