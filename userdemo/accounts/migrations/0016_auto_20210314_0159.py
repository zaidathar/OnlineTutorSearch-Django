# Generated by Django 3.1.5 on 2021-03-13 20:29

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210312_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('m_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.meeting')),
                ('is_active', models.BooleanField(default=True)),
                ('chat', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2000), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('amount', models.IntegerField(default=0)),
                ('history', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='no_of_students',
        ),
        migrations.AddField(
            model_name='tutor',
            name='no_lesson',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='no_rate',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='rating',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutor',
            name='students',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='no_of_hours',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='rate',
            field=models.PositiveIntegerField(default=200),
        ),
    ]