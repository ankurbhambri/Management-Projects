from django.db import models
from booking.models import Query
from django.contrib.auth.models import User


class OrderTable(models.Model):
    user = models.ForeignKey(
        User, null=True, default=None, on_delete=models.CASCADE)
    query = models.ForeignKey(
        Query, null=True, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
