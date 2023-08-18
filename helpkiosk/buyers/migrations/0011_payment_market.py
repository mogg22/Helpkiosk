# Generated by Django 4.2.3 on 2023-08-18 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0006_option'),
        ('buyers', '0010_paymentitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='market',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sellers.market'),
        ),
    ]
