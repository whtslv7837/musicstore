# Generated by Django 5.1.3 on 2024-11-29 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_quantity_cartitem_stock_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='stock_quantity',
            new_name='quantity',
        ),
    ]
