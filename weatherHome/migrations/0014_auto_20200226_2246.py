# Generated by Django 2.2.6 on 2020-02-27 04:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weatherHome', '0013_auto_20200226_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateAccountCreated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 26, 22, 46, 9, 448746)),
        ),
        migrations.AlterField(
            model_name='weatherforusers',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
