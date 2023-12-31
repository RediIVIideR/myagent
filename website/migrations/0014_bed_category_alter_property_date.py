# Generated by Django 4.1.4 on 2023-11-19 16:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_reviews_alter_property_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(blank=True, default='', max_length=5000, verbose_name='Bedrooms')),
            ],
            options={
                'verbose_name': 'Bedroom',
                'verbose_name_plural': 'Bedrooms',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(blank=True, default='', max_length=5000, verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 16, 1, 48, 417096, tzinfo=datetime.timezone.utc), verbose_name='Time added'),
        ),
    ]
