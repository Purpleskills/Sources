# Generated by Django 2.0.1 on 2019-05-03 18:06

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psauth', '0005_organization_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0008_usergoals_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('difficulty', models.SmallIntegerField(choices=[(core.models.DifficultyChoice(1), 1), (core.models.DifficultyChoice(2), 2), (core.models.DifficultyChoice(3), 3)])),
                ('progressinpercent', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='psauth.Company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='usergoals',
            name='company',
        ),
        migrations.RemoveField(
            model_name='usergoals',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserGoals',
        ),
        migrations.AddField(
            model_name='keyresult',
            name='objective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='learn.Objective'),
        ),
    ]
