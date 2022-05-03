from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('users/signup', views.UsersSignUpView.as_view(), name='signup'),
    path('users/signin', views.UsersSignInView.as_view(), name='signin'),
    path('users/logout', views.logout, name='logout'),
    path('users/confirm/<int:user_id>/<uuid:code>', views.user_confirmation, name='confirmation'),

    path('movies/categories', views.MovieCategoriesView.as_view(), name='categories'),
    path('movies/categories/<str:category_slug>', views.CategoryMoviesView.as_view(), name='category'),
    path('movies/<slug:movie_slug>', views.MovieDetailView.as_view(), name='movie'),
    path('', views.MovieListView.as_view(), name='home'),
]


# handler404="app_name.views.function_name"