# Generated by Django 5.0.3 on 2024-04-03 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_billingaddress_street_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='company',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
