from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    '''Admin View for User'''
    ordering = ['id']
    list_display = ['email', 'full_name', 'is_active', 'is_staff']
    search_fields = ('email', 'full_name')
    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('full_name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (_('Add new user'), {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'full_name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
    readonly_fields = ['last_login']


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    '''Admin View for Recipe'''
    # ordering = ['id']
    list_display = ['title', 'time_minutes', 'price', 'description', 'link']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin View for Tag'''
    # ordering = ['id']
    list_display = ['name']