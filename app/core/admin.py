from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .models import User, ProfileModel, SkillsModel


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


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'first_name', 'last_name',
                    'created_at', 'last_name')
    list_filter = ("created_at", 'updated_at')
    search_fields = ('last_name', 'user')


admin.site.register(ProfileModel, ProfileAdmin)


class SkillsAdmin(admin.ModelAdmin):
    list_display = ('title', 'color_theme', 'order', 'is_visible')

    list_filter = ('is_visible',)
    search_fields = ('title', 'abbreviation', 'description')
    ordering = ('order', 'title')


admin.site.register(SkillsModel, SkillsAdmin)
