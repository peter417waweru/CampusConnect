# Generated by Django 5.0.6 on 2024-07-10 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shoptreat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="items",
            field=models.ManyToManyField(
                through="shoptreat.OrderItem", to="shoptreat.shopitem"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shoptreat.order"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="shop_item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shoptreat.shopitem"
            ),
        ),
    ]