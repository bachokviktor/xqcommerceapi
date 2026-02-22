from django.contrib import admin

from . import models


# Register your models here.
class ItemPhotoInline(admin.TabularInline):
    model = models.ItemPhoto
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemPhotoInline]


admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemReview)
admin.site.register(models.Cart)
