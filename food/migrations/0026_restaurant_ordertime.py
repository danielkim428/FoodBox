# Generated by Django 3.1 on 2020-08-20 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0025_profile_woodstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='orderTime',
            field=models.TimeField(blank=True, null=True),
        ),
    ]