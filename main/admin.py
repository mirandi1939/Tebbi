from django.contrib import admin

from .models import *


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fieldsets = (
        (
            None,
            {
                'fields': ('image',)
            }
        ),
    )
    max_num = 5
    extra = 0


@admin.register(Traning)
class TraningAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin, ]


admin.site.register(Category)

