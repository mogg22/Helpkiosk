# Generated by Django 4.2.3 on 2023-08-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0003_market_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]