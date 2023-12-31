# Generated by Django 4.2.2 on 2023-08-23 19:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0020_alter_customers_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='flights',
            name='arrival_terminal',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='flights',
            name='departure_terminal',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='flights',
            name='flight_number',
            field=models.CharField(default=111, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tickets',
            name='adult_traveler_count',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)]),
        ),
        migrations.AddField(
            model_name='tickets',
            name='cabin',
            field=models.CharField(choices=[('ECONOMY', 'Economy'), ('BUSINESS', 'Business'), ('FIRST', 'First Class')], default='ECONOMY', max_length=10),
        ),
        migrations.AddField(
            model_name='tickets',
            name='child_traveler_count',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)]),
        ),
        migrations.AddField(
            model_name='tickets',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('ILS', 'ILS')], default='USD', max_length=4),
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bingo.customers')),
            ],
            options={
                'verbose_name_plural': 'Itineraries',
            },
        ),
        migrations.AddField(
            model_name='tickets',
            name='itinerary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Bingo.itinerary'),
        ),
    ]
