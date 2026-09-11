from django.contrib import admin
from django.utils.html import format_html
from .models import (Project,
                     Tag,
                     Screenshots,
                     KeyOutcome,
                     StackItem,
                     Service)

# Register your models here.
# =====================================================>>> new method >>> Inline
# >>>>>  admin.TabularInline , admin.stackedInline


class ScreenshotInline(admin.TabularInline):
    model = Screenshots
    extra = 1
    fields = ('image_preview', 'image', 'alt_text',
              'is_primary', 'display_order')
    readonly_fields = ('image_preview',)
    ordering = ('display_order',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;" />',
                obj.image.url,
            )
            return 'no image'
    image_preview.short_description = 'preview'




class KeyOutcomeInline(admin.TabularInline):
    model = KeyOutcome
    extra = 1
    fields = ('key_outcomes', 'display_order')
    ordering = ('display_order',)


class StackItemInline(admin.TabularInline):
    model = StackItem
    extra = 1
    fields = ('name', 'display_order',)
    ordering = ('display_order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'name',
                    'is_published', 'created_at', 'display_order')
    list_display_links = ('thumbnail_preview', 'name')
    list_editable = ('is_published', 'display_order')
    list_filter = ('created_at', 'is_published', 'timeline')
    search_fields = ('name', 'short_description', 'article_title')
    readonly_fields = ('created_at', 'updated_at')

    inlines = [
        
        ScreenshotInline,
        StackItemInline,
        KeyOutcomeInline,
        
    ]

    fieldsets = (
        ('basic information',
         {
             'fields':
                 (
                     'name',
                     'tags',
                     'slug',
                     'thumbnail',
                     'short_description',
                     'services',
                     'is_published',
                     'display_order',
                 )
         }),
        (
            'article content',
            {
                'fields': (
                    'article_title',
                    'article',

                )

            }
        ),
        (
            'metadata',
            {
                'fields': (
                    'role',
                    'timeline',
                    'demo_url',
                )
            }
        ),
        (
            'date',
            {
                'fields':
                    (
                        'created_at',
                        'updated_at',
                    ),
                    'classes': ('collapse',),
            }
        )
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 45px; height: 35px; object-fit: cover; border-radius: 4px;" />',
                obj.thumbnail.url,
            )
        return "_"

        thumbnail_preview.short_description = 'thumbnail'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    
# ===================================================>>>> old method
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_published',)
#     list_filter = ('timeline', 'stack_items')
#     search_fields = ('name',)


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name',)


# @admin.register(ProjectStackItem)
# class StacksAdmin(admin.ModelAdmin):
#     list_display = ['name']


# @admin.register(ProjectScreenshots)
# class ScreenshotsAdmin(admin.ModelAdmin):
#     list_display = ['alt_text', 'is_primary']


# @admin.register(ProjectKeyOutcome)
# class KeyOutAdmin(admin.ModelAdmin):
#     list_display = ['key_outcomes']
