# Generated by Django 3.1.3 on 2020-11-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.JSONField(null=True),
        ),
    ]