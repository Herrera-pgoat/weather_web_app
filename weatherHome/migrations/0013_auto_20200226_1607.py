# Generated by Django 2.2.6 on 2020-02-26 22:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weatherHome', '0012_auto_20200223_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='location',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='weatherStation',
        ),
        migrations.RemoveField(
            model_name='weatherforusers',
            name='weatherStation',
        ),
        migrations.AddField(
            model_name='weather',
            name='cityCode',
            field=models.CharField(default='hellocityfcode', max_length=30, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='cityName',
            field=models.CharField(default='hellocityname', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='countryName',
            field=models.CharField(default='hellocoutnry', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='snow',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='weather',
            name='stateName',
            field=models.CharField(default='hellostatename', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='zipcode',
            field=models.CharField(default='zipcode', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weatherforusers',
            name='cityCode',
            field=models.ForeignKey(default='hellocitycode', on_delete=django.db.models.deletion.CASCADE, to='weatherHome.weather'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='dateAccountCreated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 26, 16, 7, 20, 437756)),
        ),
    ]
