from django.contrib import admin
from .import models
# Register your models here.


class sharedView(admin.StackedInline):
    model = models.share


class ItemView(admin.StackedInline):
    model = models.Item


@admin.register(models.Budget)
class budget(admin.ModelAdmin):
    inlines = [ItemView, sharedView]

    class Meta:
        model = models.Budget


"""
#if needed to see them seperate...
@admin.register(models.share)
class sharedView(admin.ModelAdmin):
    pass


@admin.register(models.Item)
class ItemView(admin.ModelAdmin):
    pass
"""

# admin.site.register(models.Budget)
# admin.site.register(models.Item)
# admin.site.register(models.Shared)
