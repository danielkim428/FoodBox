# Generated by Django 3.0.8 on 2020-07-18 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(default='', max_length=50),
        ),
    ]