# Generated by Django 5.0.6 on 2024-12-04 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_remove_order_p_buyer_remove_order_p_supplier_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_p',
            name='shipped',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
