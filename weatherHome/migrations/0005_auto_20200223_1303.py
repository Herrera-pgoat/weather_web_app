# Generated by Django 2.2.6 on 2020-02-23 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherHome', '0004_auto_20200222_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passwordSalt',
            field=models.CharField(max_length=32),
        ),
    ]
