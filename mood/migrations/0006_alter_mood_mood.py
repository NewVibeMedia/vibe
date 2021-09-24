# Generated by Django 3.2.5 on 2021-09-24 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0005_alter_mood_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mood',
            name='mood',
            field=models.CharField(choices=[('0', 'Very Negative'), ('1', 'Negative'), ('2', 'Neutral'), ('3', 'Positive'), ('4', 'Very Positive')], max_length=50),
        ),
    ]