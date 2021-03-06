# Generated by Django 2.0.1 on 2019-03-06 18:25

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psauth', '0002_auto_20190306_0835'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGoals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_goal', models.CharField(max_length=60)),
                ('difficulty', models.SmallIntegerField(choices=[(core.models.DifficultyChoice(1), 1), (core.models.DifficultyChoice(2), 2), (core.models.DifficultyChoice(3), 3)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
