# Generated by Django 5.1.3 on 2024-11-29 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock_quantity',
            new_name='quantity',
        ),
    ]
