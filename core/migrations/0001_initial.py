# Generated by Django 3.0.5 on 2020-11-22 05:32

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('customer_id', models.UUIDField()),
                ('product_id', models.UUIDField()),
                ('nos', models.PositiveIntegerField(default=1)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('Cart', 'Cart'), ('Purchased', 'Purchased'), ('Delivered', 'Delivered')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Product_List',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=50)),
                ('seller', models.UUIDField()),
                ('category', models.CharField(max_length=30, null=True)),
                ('rating', models.FloatField(default=0)),
                ('total_ratings', models.PositiveIntegerField(default=0)),
                ('stock', models.PositiveIntegerField(default=10)),
                ('base_price', models.PositiveIntegerField()),
                ('discount', models.FloatField(default=0)),
                ('description', models.TextField(default='Some Product')),
                ('additional', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('bs_name', models.CharField(max_length=50)),
                ('bs_category', models.CharField(choices=[('Literature and Stationary', 'Literature and Stationary')], max_length=30)),
                ('gst_no', models.CharField(max_length=20)),
                ('pan_no', models.CharField(max_length=20)),
                ('bank_ac', models.CharField(max_length=20)),
                ('address', jsonfield.fields.JSONField(default=dict)),
                ('rating', models.FloatField(default=0)),
                ('total_ratings', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Reviewing', 'Reviewing')], default='Reviewing', max_length=20)),
            ],
        ),
    ]
