from django.db import models


class CustomerLogin(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    customer_email = models.EmailField(max_length=150, null=False, blank=False, unique=True)
    phone_number = models.IntegerField(null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_email
