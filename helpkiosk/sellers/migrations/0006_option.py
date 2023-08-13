# Generated by Django 4.2.3 on 2023-08-13 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0005_market_close_market_start_market_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=8)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.menu')),
            ],
        ),
    ]
