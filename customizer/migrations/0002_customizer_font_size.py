# Generated by Django 3.2.6 on 2021-10-07 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customizer',
            name='font_size',
            field=models.IntegerField(default=12),
        ),
    ]
