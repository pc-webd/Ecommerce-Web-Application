# Generated by Django 3.1.3 on 2020-11-10 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classyeveryday', '0002_auto_20201110_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
