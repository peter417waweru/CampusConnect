# Generated by Django 5.0.6 on 2024-07-05 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hostel", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hostel",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="hostel/hostel_images/"
            ),
        ),
    ]
