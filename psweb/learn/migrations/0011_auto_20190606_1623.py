# Generated by Django 2.1.5 on 2019-06-06 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0010_auto_20190526_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='objective',
            name='timeline',
            field=models.PositiveSmallIntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='keyresult',
            name='progressinpercent',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]