# Generated by Django 4.0.6 on 2024-10-03 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BestLogMarketPlaceApp', '0010_remove_transaction_proof_of_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tx_ref',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
