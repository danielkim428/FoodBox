# Generated by Django 3.0.5 on 2020-07-25 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0019_auto_20200721_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='total_count',
            new_name='totalCount',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='phone_number',
            new_name='phoneNumber',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='closeTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='openTime',
            field=models.TimeField(blank=True, null=True),
        ),
    ]