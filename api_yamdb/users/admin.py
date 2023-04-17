from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Добавление модели пользователя в админку"""
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    list_editable = ('role',)
    list_filter = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
