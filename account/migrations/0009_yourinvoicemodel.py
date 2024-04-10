# Generated by Django 5.0.3 on 2024-04-09 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_rename_first_name_billingaddress_firstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='YourInvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=100)),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
            ],
        ),
    ]