# Generated by Django 3.1.3 on 2020-11-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classyeveryday', '0003_order_order_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
    ]