# Generated by Django 4.2.2 on 2023-06-23 14:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0008_alter_airline_companies_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flights',
            name='remaining_tickets',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
