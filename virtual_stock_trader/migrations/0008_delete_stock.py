# Generated by Django 3.1.4 on 2020-12-31 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_stock_trader', '0007_auto_20201231_0137'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stock',
        ),
    ]