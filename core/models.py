from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator, ValidationError
from accounts.models import CustomUser
import jsonfield

def change_name(instance, filename):
    return "User_{0}/{1}".format(instance.id, filename)

def sheet_path(instance, filename):
    return "Sheets/User_{0}/{1}".format(instance.id, filename)

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')

class Sub_Category(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    main_cat = models.CharField(max_length=30, unique=False)
    sub_cat = models.CharField(max_length=30, unique=False)
    # properties 
    def __str__(self):
        return self.main_cat + " - " + self.sub_cat

class Product_List(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    # img = models.ImageField()
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    seller = models.UUIDField(unique=False)
    # category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=10)
    base_price = models.PositiveIntegerField(blank=False)
    discount = models.FloatField(default = 0)
    description = models.TextField(default="Some Product")
    def __str__(self):
        return self.name

class Seller(models.Model):
    choice = (
        ("-","-"),
        ("Electronics","Electronics"),
        ("Stationary","Stationary"),
        ("Art and Craft","Art and Craft"),
        ("Grocery","Grocery"),
    )
    status = (
        ("Active","Active"),
        ("Reviewing","Reviewing"),
        
    )
    reg = RegexValidator(r'^[0-9]*$','Only Numbers are Allowed')
    id = models.UUIDField(primary_key=True)
    bs_name = models.CharField(max_length=50)
    bs_category = models.CharField(max_length=30, choices=choice)
    gst_no = models.CharField(max_length=20)
    pan_no = models.CharField(max_length=20)
    pan_card = models.FileField(upload_to=change_name)
    bank_ac = models.CharField(max_length=20)
    address = jsonfield.JSONField()
    rating = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=status, default="Reviewing")
    def __str__(self):
        return self.bs_name

class Orders(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    customer_id = models.UUIDField()
    seller_id = models.UUIDField()
    product_id = models.UUIDField()
    date = models.DateTimeField()
    order_type = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    user_xp = models.PositiveIntegerField(default=8)


# Create your models here.
