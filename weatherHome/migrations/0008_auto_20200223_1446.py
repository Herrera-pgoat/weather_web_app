# Generated by Django 2.2.6 on 2020-02-23 20:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherHome', '0007_auto_20200223_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateAccountCreated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 23, 14, 46, 11, 957748)),
        ),
        migrations.AlterField(
            model_name='user',
            name='passwordHashed',
            field=models.CharField(max_length=128),
        ),
    ]
