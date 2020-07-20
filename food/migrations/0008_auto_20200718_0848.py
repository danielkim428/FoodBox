# Generated by Django 3.0.5 on 2020-07-18 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_auto_20200718_0841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='food.Restaurant'),
            preserve_default=False,
        ),
    ]