from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(
        verbose_name='Created', auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(verbose_name='modified', auto_now=True)

    class Meta:
        abstract = True


class OrderHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.JSONField()
