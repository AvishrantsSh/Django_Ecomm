from django.db import models
from uuid import uuid4

class Category(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.TextField()
    # properties 
    def __str__(self):
        return self.name

class Product_List(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.TextField()
    brand = models.CharField(max_length=50)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, default=uuid4)
    rating = models.PositiveIntegerField(default=5)
    total_ratings = models.PositiveIntegerField(default=100)
    stock = models.PositiveIntegerField(default=10)
    price_old = models.PositiveIntegerField(default = 100, blank=True)
    price_new = models.PositiveIntegerField(default = 80)
    discount = models.FloatField(default = 20)
    description = models.TextField(max_length=500, default="Hola AMigo")
    def __str__(self):
        return self.name


class Seller(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.TextField()
    rating = models.PositiveIntegerField()
    

# Create your models here.
