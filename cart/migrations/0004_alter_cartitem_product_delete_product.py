# Generated by Django 5.0.3 on 2024-03-21 00:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_product_description_product_image_alter_cart_user'),
        ('product', '0002_product_quantity_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
