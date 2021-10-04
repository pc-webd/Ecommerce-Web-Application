# Generated by Django 3.1.3 on 2020-11-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classyeveryday', '0009_auto_20201112_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='variation',
            name='size',
            field=models.CharField(choices=[('XS', 'Xtra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Xtra Large'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], max_length=120),
        ),
    ]
