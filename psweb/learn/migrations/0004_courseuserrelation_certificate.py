# Generated by Django 2.0.1 on 2019-03-10 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_courseuserrelation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='certificate',
            field=models.FileField(null=True, upload_to='certs/'),
        ),
    ]