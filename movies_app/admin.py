from django.contrib import admin
from .models import *

class ActorRoleAdmin(admin.TabularInline):
    model = ActorRole


class MovieRatingAdmin(admin.TabularInline):
    model = MovieRating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_confirmed')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = (ActorRoleAdmin, MovieRatingAdmin, )
    prepopulated_fields = {'slug': ('title', )}
    # list_display = ('')
    # list_filter = ('email', 'is_staff', 'is_active',)
    # fieldsets = (
    #     (None, {'fields': ('username', 'email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
    #      ),
    # )
    # search_fields = ('username', 'email',)
