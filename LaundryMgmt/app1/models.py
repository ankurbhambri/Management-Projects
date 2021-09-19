from django.db import models
from django.contrib.postgres.fields import JSONField


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=255, null=True)
    mobile = models.CharField( max_length=12, null=True)
    landmark = models.CharField(max_length=180, null=True)
    address = models.CharField(max_length=1024, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=True)

    
class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=True)


class Order(models.Model):
    customer_name = models.CharField(max_length=200, null=True)
    customer_email = models.CharField(max_length=250, null=True)
    query_json = JSONField()
    total_quantity = models.IntegerField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=True)
