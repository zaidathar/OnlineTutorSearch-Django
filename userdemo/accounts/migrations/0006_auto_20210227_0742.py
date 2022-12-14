# Generated by Django 3.1.5 on 2021-02-27 02:12

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_tutor_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='contact',
            field=models.CharField(default='Enter Phone Number', max_length=16),
        ),
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(default=datetime.date(1985, 10, 12), null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(default='Your Gender', max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='location',
            field=models.CharField(default='Enter City', max_length=100),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='contact',
            field=models.CharField(default='Enter Phone Number', max_length=16),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='day_availability',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, null=True), default=['Enter Days seperated by , '], size=None),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='dob',
            field=models.DateField(default=datetime.date(1985, 10, 12), null=True),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='gender',
            field=models.CharField(default='Your Gender', max_length=10),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='location',
            field=models.CharField(default='Enter City Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='subject',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, null=True), default=['Enter Subjects seperated by , '], size=None),
        ),
    ]
