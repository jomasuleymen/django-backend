from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from rest_framework.exceptions import ValidationError
from http import HTTPStatus
from django.contrib.auth.models import User
from . import serializers
from .models import Genre, Profile, Movie
import json
from django.contrib.auth import authenticate, login, logout as logout_user
from pprint import pprint


class MovieListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'movies/movie_list.html', {'category': None})


class MovieCategoriesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'movies/categories.html')


class CategoryMoviesView(View):
    def get(self, request, category_slug):
        return render(request, 'movies/movie_list.html', {'category_slug': category_slug})


class MovieDetailView(View):
    def get(self, request, movie_slug):
        movie = Movie.objects.prefetch_related(
            'movierating_set__rating', 'actorrole_set__actor').get(slug=movie_slug)
        return render(request, 'movies/movie.html', {'movie': movie})


class UsersSignUpView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'movies/signup.html')

    def post(self, request, *args, **kwargs):
        try:
            serializer = serializers.UserSignUpSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            phone = data['phone']
            birthdate = data['birthdate']

            if 'birthdate' in data:
                del data['birthdate']
            if 'phone' in data:
                del data['phone']

            user = User.objects.create_user(**data)

            user.profile.phone = phone
            user.profile.birthdate = birthdate

            user.profile.save()

            return render(request, 'movies/signup.html', {'success': True})
        except ValidationError:
            print(serializer.errors)
            return render(request, 'movies/signup.html', {'errors': serializer.errors, 'data': request.POST}, status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse({'detail': 'some error occured on the server'}, status=HTTPStatus.BAD_REQUEST)


class UsersSignInView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'movies/signin.html')

    def post(self, request, *args, **kwargs):
        try:
            serializer = serializers.UserSignInSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.validated_data['email'])

            if not user.check_password(serializer.validated_data['password']):
                return render(request, 'movies/signin.html', {'errors': {'password': ['wrong password']}, 'data': request.POST}, status=HTTPStatus.BAD_REQUEST)

            login(request, user)

            return render(request, 'movies/index.html')
        except ValidationError:
            return render(request, 'movies/signin.html', {'errors': serializer.errors, 'data': request.POST}, status=HTTPStatus.BAD_REQUEST)
        except User.DoesNotExist:
            return render(request, 'movies/signin.html', {'errors': {'email': ['user with this email not found']}, 'data': request.POST}, status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'detail': 'some error occured on the server'}, status=HTTPStatus.BAD_REQUEST)


def logout(request):
    try:
        logout_user(request)
        return redirect('/')
    except Exception as e:
        print(e)
        return JsonResponse({'detail': 'some error occured on the server'}, status=HTTPStatus.BAD_REQUEST)


def user_confirmation(request, user_id, code):
    try:
        user_profile = Profile.objects.get(user_id=user_id)
        if (user_profile.confirmation_code == code):
            user_profile.is_confirmed = True
            user_profile.save()
            return JsonResponse({'detail': 'Confirmed'}, status=HTTPStatus.ACCEPTED)

        return JsonResponse({'detail': 'wrong confirmation code'}, status=HTTPStatus.BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({'detail': 'wrong confirmation link'}, status=HTTPStatus.BAD_REQUEST)
