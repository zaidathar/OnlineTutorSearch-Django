# Generated by Django 3.1.5 on 2021-02-23 10:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210222_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='subject',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100, null=True), default=list, size=None),
        ),
    ]
