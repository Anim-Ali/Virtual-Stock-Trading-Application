# Generated by Django 3.1.4 on 2020-12-30 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_stock_trader', '0005_stock_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
