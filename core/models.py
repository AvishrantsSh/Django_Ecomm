from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator, ValidationError
from accounts.models import CustomUser
import jsonfield
from random import randint
from django.utils.timezone import now
def change_name(instance, filename):
    return "User_{0}/{1}".format(instance.id, filename)

def sheet_path(instance, filename):
    return "Sheets/User_{0}/{1}".format(instance.id, filename)

def img_path(instance, filename):
    return "Images/User_{0}/{1}".format(instance.id, filename)

def random_cat():
    lst = ["Scify", "Adventure", "Mystery", "Infotainment"]
    return lst[randint(0,3)]

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')

class Product_List(models.Model):
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    img = models.ImageField(default="/product.svg", upload_to = img_path)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    seller = models.UUIDField(unique=False)
    category = models.CharField(max_length=30, unique=False, null=True)
    rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=10)
    base_price = models.PositiveIntegerField(blank=False)
    discount = models.FloatField(default = 0)
    description = models.TextField(default="Some Product")
    additional = jsonfield.JSONField()
    
    def save(self, *args, **kwargs):
        self.category=random_cat()
        super(Product_List, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Seller(models.Model):
    choice = (
        # ("Electronics","Electronics"),
        ("Literature and Stationary","Literature and Stationary"),
        # ("Groceries","Groceries"),
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
    rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=status, default="Reviewing")
    def __str__(self):
        return self.bs_name

class Cart(models.Model):
    choice=(
        ("Cart", "Cart"),
        ("Purchased", "Purchased"),
        ("Delivered", "Delivered"),
    )
    id = models.UUIDField(default=uuid4, primary_key=True)
    customer_id = models.UUIDField()
    product_id = models.UUIDField()
    nos = models.PositiveIntegerField(default = 1)
    date = models.DateTimeField(default=now, editable=False)
    status = models.CharField(max_length=15, choices=choice)

    def __str__(self):
        return str(self.customer_id) + "-" + str(self.product_id)

# Create your models here.
