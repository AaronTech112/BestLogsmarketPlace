# Generated by Django 5.1.2 on 2024-10-22 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BestLogMarketPlaceApp", "0012_cart_session_key_alter_cart_user_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["order"],
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AddField(
            model_name="category",
            name="order",
            field=models.PositiveIntegerField(
                default=0, help_text="Category display order"
            ),
        ),
    ]
