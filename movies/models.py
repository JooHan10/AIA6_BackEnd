from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=300)

class Movie(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    poster_path = models.CharField(max_length=300, null=True, blank=True)
    page = models.IntegerField("페이지")
