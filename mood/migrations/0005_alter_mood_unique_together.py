# Generated by Django 3.2.5 on 2021-09-24 00:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mood', '0004_alter_mood_mood'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mood',
            unique_together={('date_posted', 'author')},
        ),
    ]
