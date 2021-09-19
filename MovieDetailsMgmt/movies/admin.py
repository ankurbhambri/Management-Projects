from django.contrib import admin
from movies.models import Movie

# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'year', 'rating', 'extra_feild',
                    'created_at', 'modified_at',)
    search_fields = ('tittle', 'year', 'rating')
