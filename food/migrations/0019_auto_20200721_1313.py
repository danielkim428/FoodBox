# Generated by Django 3.0.5 on 2020-07-21 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0018_order_totalprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
