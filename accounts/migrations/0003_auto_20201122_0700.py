# Generated by Django 3.0.5 on 2020-11-22 07:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201122_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^[+]{0,1}[0-9]{10,12}', 'Invalid Mobile Number')]),
        ),
    ]