import random
import string
from django.db import models


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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


class UserProfile(TimeStampedModel):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    real_name = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.id = 'W' + id_generator()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.id


class UsersActivity(TimeStampedModel):
    user = models.ForeignKey(
        UserProfile, null=False, on_delete=models.CASCADE)
    extra_feild = models.JSONField()
