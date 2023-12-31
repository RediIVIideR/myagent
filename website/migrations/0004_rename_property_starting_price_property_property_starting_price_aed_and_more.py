# Generated by Django 4.1.4 on 2023-11-03 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_property_property_image1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='property_starting_price',
            new_name='property_starting_price_aed',
        ),
        migrations.RemoveField(
            model_name='property',
            name='property_handover',
        ),
        migrations.RemoveField(
            model_name='property',
            name='property_type',
        ),
        migrations.AddField(
            model_name='property',
            name='date',
            field=models.DateTimeField(default='2023-10-10 10:00', verbose_name='Time added'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_amenities',
            field=models.TextField(blank=True, default='', max_length=50000, verbose_name='Property Amenities'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_starting_price_usd',
            field=models.TextField(blank=True, default='', max_length=5000, verbose_name='Property Starting Price (USD)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_developer',
            field=models.TextField(blank=True, default='', max_length=5000, verbose_name='Property Developer'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_payment_plan',
            field=models.TextField(blank=True, default='', max_length=5000, verbose_name='Property Payment Plan'),
        ),
    ]
