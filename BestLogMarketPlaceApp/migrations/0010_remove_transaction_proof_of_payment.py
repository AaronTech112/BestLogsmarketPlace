# Generated by Django 5.0.3 on 2024-10-03 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BestLogMarketPlaceApp', '0009_cart_remove_transaction_product_product_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='proof_of_payment',
        ),
    ]
