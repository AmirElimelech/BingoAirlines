# Generated by Django 4.2.2 on 2023-08-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bingo', '0023_rename_itinerary_booking_alter_booking_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='airport',
            name='country_code',
            field=models.CharField(default='ZZ', max_length=2),
            preserve_default=False,
        ),
    ]