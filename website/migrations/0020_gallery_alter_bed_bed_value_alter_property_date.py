# Generated by Django 4.1.4 on 2023-11-19 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_alter_bed_bed_value_alter_property_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.FileField(upload_to='media/gallery', verbose_name='Image 1')),
                ('image2', models.FileField(upload_to='media/gallery', verbose_name='Image 2')),
                ('image3', models.FileField(upload_to='media/gallery', verbose_name='Image 3')),
                ('image4', models.FileField(upload_to='media/gallery', verbose_name='Image 4')),
                ('image5', models.FileField(upload_to='media/gallery', verbose_name='Image 5')),
                ('image6', models.FileField(upload_to='media/gallery', verbose_name='Image 6')),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.AlterField(
            model_name='bed',
            name='bed_value',
            field=models.TextField(blank=True, default='', max_length=5000, verbose_name='Bedroom Value (Do not put/edit anything here)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 19, 25, 8, 699487, tzinfo=datetime.timezone.utc), verbose_name='Time added'),
        ),
    ]
