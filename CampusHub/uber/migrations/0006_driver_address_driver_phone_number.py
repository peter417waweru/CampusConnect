# Generated by Django 5.0.6 on 2024-07-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("uber", "0005_trip"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="address",
            field=models.CharField(default="Default Address", max_length=255),
        ),
        migrations.AddField(
            model_name="driver",
            name="phone_number",
            field=models.CharField(default="Default Address", max_length=15),
            preserve_default=False,
        ),
    ]
