# Generated by Django 4.2.2 on 2023-08-23 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0021_flights_arrival_terminal_flights_departure_terminal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='itinerary',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='Bingo.itinerary'),
            preserve_default=False,
        ),
    ]
