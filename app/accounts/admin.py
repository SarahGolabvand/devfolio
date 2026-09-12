from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProfileModel, SkillsModel


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # the fields to be used in dispalying in User model
    # these override the definitions on the base UserAdmin
    # that refrence specific fields on auth.User.
    model = User
    list_display = ('email', 'is_superuser', 'is_active')
    list_filter = ('email', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    # userpannel
    fieldsets = (
        ('Authentication',
            {'fields': ('email', 'password')}),
        ('Permissons',
            {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Groups Permissons',
         {'fields': ('groups', 'user_permissions',)})
    )
    # add user pannel
    add_fieldsets = (
        ('Sign in',
         {
             'classes': 'wide',
             'fields': ('email', 'password1', 'password2', 'is_staff')
         }
         ),
    )


@admin.register(ProfileModel)
class ProfileAdmin(ModelAdmin):

    list_display = ('user', 'first_name', 'last_name',
                    'created_at', 'last_name')
    list_filter = ("created_at", 'updated_at')
    search_fields = ('last_name', 'user')


@admin.register(SkillsModel)
class SkillsAdmin(ModelAdmin):
    list_display = ('title', 'color_theme', 'order', 'is_visible')

    list_filter = ('is_visible',)
    search_fields = ('title', 'abbreviation', 'description')
    ordering = ('order', 'title')
