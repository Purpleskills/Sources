# Generated by Django 2.1.5 on 2019-02-25 06:24

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_auto_20190212_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='Active', max_length=100, no_check_for_status=True),
        ),
    ]
