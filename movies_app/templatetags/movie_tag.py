from django import template
from django.db.models import *

from movies_app.models import *

register = template.Library()

genre_queryset = Genre.objects.all()

@register.simple_tag()
def get_categories():
    return [genre.name.capitalize() for genre in genre_queryset]


@register.inclusion_tag('inclusions/movie_list.html')
def show_movies(category):
    movies = Movie.objects.only('genres', 'poster', 'title', 'year',
                                'description', 'slug').prefetch_related('genres')
    if category:
        movies = movies.filter(genres__name=category)

    return {
        'category_name': category,
        'movies': movies
    }


DESCRIPTION_MAX_LEN = 260


@register.simple_tag()
def format_discription(description):
    if len(description) > DESCRIPTION_MAX_LEN:
        return str(description[:DESCRIPTION_MAX_LEN]) + '...'
    return description[:DESCRIPTION_MAX_LEN]
