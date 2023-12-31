# Generated by Django 4.1.4 on 2023-11-12 19:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_property_options_remove_property_sort_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.TextField(blank=True, default='Offplan', max_length=5000, verbose_name='Property Type'),
        ),
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 19, 44, 47, 816126, tzinfo=datetime.timezone.utc), verbose_name='Time added'),
        ),
    ]
