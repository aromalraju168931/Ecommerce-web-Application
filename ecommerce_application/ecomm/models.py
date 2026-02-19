from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_phone=models.CharField(max_length=15)
    user_address=models.TextField()
    
class Category(models.Model):
    name=models.CharField(max_length=40)

class subCategory(models.Model):
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)

class Products(models.Model):
    products_name=models.CharField(max_length=20)
    product_description=models.TextField()
    product_price=models.IntegerField()
    product_image=models.ImageField(upload_to='products/')
    product_discound=models.CharField(max_length=10)
    subcategory=models.ForeignKey(subCategory,on_delete=models.CASCADE)

class VerifiedUser(models.Model):
    email = models.CharField(max_length=200, unique=True)