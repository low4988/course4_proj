from django.db import models

# Create your models here.
class SearchTerm(models.Model):
    class Meta:
        ordering = ["id"]

    term = models.TextField(unique=True)
    last_search = models.DateTimeField(auto_now=True)
    '''
    The term that's searched for, term, is unique. 
    The last_search is the date that the search was last performed. 
      -We use this to make sure the search isn't repeated too often.
    '''

class Genre(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.TextField(unique=True)

class Movie(models.Model):
    class Meta:
        ordering = ["title", "year"]

    title = models.TextField()
    year = models.PositiveIntegerField()
    runtime_minutes = models.PositiveIntegerField(null=True)
    imdb_id = models.SlugField(unique=True)
    genres = models.ManyToManyField(Genre, related_name="movies")
    plot = models.TextField(null=True, blank=True)
    is_full_record = models.BooleanField(default=False)

    '''
    It has the fields that you would expect, 
    to match what the API is supplying us. 
    
    We use the is_full_record flag to determine if the 
    Movie contains only the values in the list response, 
    or if it has been supplemented with the full detail response

    Notice how imdb_id (the ID of the movie from the Internet Movie DataBase) 
    has been defined. 
    It's a unique SlugField. kind of like a primary key. 
    In the movie detail URL, we'll use this, and then query 
    the database on it. 
    It will also allow us to create a mapping 
    between the record in our local DB and the data provided by OMDb. 
    OMDb in turn uses this ID to map back to IMDb.
    '''