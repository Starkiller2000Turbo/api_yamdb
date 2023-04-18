from django.contrib import admin

from compositions.models import Category, Genre, Title


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = (
        'slug',
        'name',
    )
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    search_fields = ('name',)
    list_filter = (
        'category',
        'year',
    )
    empty_value_display = '-пусто-'


class Genre_TitleInline(admin.TabularInline):
    model = Title.genre.through


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
