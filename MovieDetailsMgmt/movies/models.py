from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


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


class Movie(TimeStampedModel):
    tittle = models.CharField(max_length=255, null=True, default=None)
    image_url = models.URLField(max_length=200)
    year = models.IntegerField()
    rating = models.FloatField()
    extra_feild = JSONField()

    def __str__(self):
        return self.tittle


class UserMovie(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched = models.IntegerField(default=0)
