# Generated by Django 4.2.3 on 2023-08-15 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0006_remove_cart_menu_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='option',
        ),
    ]
