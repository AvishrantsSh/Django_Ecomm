from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator, ValidationError

def change_name(instance, filename):
    return "User_{0}/{1}".format(instance.id, filename)

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
    img = models.ImageField()
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    seller = models.UUIDField(unique=False)
    category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    total_ratings = models.PositiveIntegerField(default=100)
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
    reg = RegexValidator(r'^[0-9]*$','Only Numbers are Allowed')
    id = models.UUIDField(default=uuid4, primary_key=True)
    bs_name = models.CharField(max_length=50)
    bs_category = models.CharField(max_length=30, choices=choice)
    reg_no = models.CharField(max_length=15)
    id_card = models.FileField(upload_to=change_name)
    bank_ac = models.CharField(max_length=20)
    # gmap_loc
    # pincode
    # district
    # state
    # country
    # category
    rating = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    
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
