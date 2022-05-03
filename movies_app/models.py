from django.contrib.auth.models import User
from django.db import models
import uuid
from django.template.defaultfilters import slugify
from django.urls.base import reverse


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=3000)
    poster = models.ImageField(upload_to="images/movies")
    year = models.PositiveSmallIntegerField(default=2021)

    directors = models.ManyToManyField('Director', related_name='director_movies')
    actors = models.ManyToManyField(
        'Actor', through='ActorRole', related_name='actors_movies')
    genres = models.ManyToManyField('Genre', related_name='movies')
    ratings = models.ManyToManyField(
        'Rating', through='MovieRating', related_name='movies')
    # category = models.ForeignKey('Category', related_name='movies', null=True, on_delete=models.CASCADE)

    country = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse("movies:movie", kwargs={"movie_slug": self.slug})

    def __str__(self) -> str:
        return self.title


class MovieShots(models.Model):
    image = models.ImageField(upload_to="images/movie_shots")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField('Category', unique=True, max_length=150)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse("movies:category", kwargs={"category_slug": self.slug})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField('Genre', unique=True, max_length=150)
    slug = models.SlugField(max_length=150, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse("movies:category", kwargs={"category_slug": self.slug})

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    """" Actors """

    image = models.ImageField(upload_to='images/actors')
    fullname = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.fullname


class Director(models.Model):
    """" directors """

    image = models.ImageField(upload_to='images/directors')
    fullname = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.fullname


class Rating(models.Model):
    source = models.CharField(
        max_length=120, blank=False, null=False, unique=True)

    def __str__(self) -> str:
        return self.source


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    point = models.DecimalField('rating', max_digits=3, decimal_places=1)


class ActorRole(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role_name = models.CharField(
        'actor role', max_length=255, null=False, blank=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(unique=True,
                             max_length=25, null=True, blank=False)

    birthdate = models.DateField(null=True)

    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username
