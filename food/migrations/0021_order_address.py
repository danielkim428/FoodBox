# Generated by Django 3.0.8 on 2020-07-25 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0020_auto_20200725_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]