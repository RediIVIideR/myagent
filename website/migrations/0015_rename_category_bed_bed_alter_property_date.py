# Generated by Django 4.1.4 on 2023-11-19 16:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_bed_category_alter_property_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bed',
            old_name='category',
            new_name='bed',
        ),
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 16, 3, 20, 819752, tzinfo=datetime.timezone.utc), verbose_name='Time added'),
        ),
    ]
