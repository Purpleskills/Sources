# Generated by Django 2.1.5 on 2019-02-24 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentprovider', '0004_lyndarawdata_udemyrawdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lyndarawdata',
            name='raw_data',
            field=models.BinaryField(),
        ),
    ]
