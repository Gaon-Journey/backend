# Generated by Django 5.1.2 on 2024-11-14 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_trip_images_trip_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='images',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
